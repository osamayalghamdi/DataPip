import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from loguru import logger

from app.schema import Tool, ToolCall, ToolResult
from app.tool.base import BaseTool


class DataCleaner(BaseTool):
    """Tool for cleaning and preprocessing data."""

    def __init__(self):
        super().__init__(
            name="DataCleaner",
            description="Cleans and preprocesses data",
            parameters={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "The DataFrame to clean",
                    },
                },
                "required": ["data"],
            },
        )

    async def _call(self, tool_call: ToolCall) -> ToolResult:
        """Clean and preprocess the data."""
        try:
            data = tool_call.arguments["data"]
            
            # Handle missing values
            data = self._handle_missing_values(data)
            
            # Handle outliers
            data = self._handle_outliers(data)
            
            # Create derived features
            data = self._create_derived_features(data)
            
            # Scale numerical features
            data = self._scale_features(data)
            
            logger.info("Data cleaning completed successfully")
            return ToolResult(
                success=True,
                data={"data": data},
            )

        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            return ToolResult(success=False, error=str(e))

    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # For numerical columns, use mean imputation
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isnull().any():
                data[col] = data[col].fillna(data[col].mean())
        
        # For categorical columns, use mode imputation
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            if data[col].isnull().any():
                data[col] = data[col].fillna(data[col].mode()[0])
        
        return data

    def _handle_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using IQR method."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers at bounds
            data[col] = data[col].clip(lower=lower_bound, upper=upper_bound)
        
        return data

    def _create_derived_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create derived features from existing ones."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        # Create interaction features
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                data[f"{col1}_times_{col2}"] = data[col1] * data[col2]
                if data[col2].min() != 0:  # Avoid division by zero
                    data[f"{col1}_per_{col2}"] = data[col1] / data[col2]
        
        # Create binned features
        for col in numeric_cols:
            data[f"{col}_binned"] = pd.qcut(data[col], q=5, labels=False, duplicates='drop')
        
        return data

    def _scale_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Scale numerical features using StandardScaler."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
        
        return data 