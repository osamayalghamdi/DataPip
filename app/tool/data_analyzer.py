from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from loguru import logger

from app.schema import Tool, ToolCall, ToolResult
from app.tool.base import BaseTool


class DataAnalyzer(BaseTool):
    """Tool for analyzing data and generating insights."""

    def __init__(self):
        super().__init__(
            name="DataAnalyzer",
            description="Analyzes data to generate insights and statistical summaries",
            parameters={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "The DataFrame to analyze",
                    },
                    "target_column": {
                        "type": "string",
                        "description": "Optional target column for correlation analysis",
                    },
                },
                "required": ["data"],
            },
        )

    async def _call(self, tool_call: ToolCall) -> ToolResult:
        """Analyze the data and generate insights."""
        try:
            data = tool_call.arguments["data"]
            target_column = tool_call.arguments.get("target_column")

            # Generate basic statistics
            basic_stats = self._generate_basic_stats(data)
            
            # Generate correlation analysis
            correlations = self._generate_correlations(data, target_column)
            
            # Generate distribution analysis
            distributions = self._analyze_distributions(data)
            
            # Generate insights
            insights = self._generate_insights(data, basic_stats, correlations, distributions)

            return ToolResult(
                success=True,
                data={
                    "data": data,
                    "basic_stats": basic_stats,
                    "correlations": correlations,
                    "distributions": distributions,
                    "insights": insights,
                },
            )

        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            return ToolResult(success=False, error=str(e))

    def _generate_basic_stats(self, data: pd.DataFrame) -> Dict:
        """Generate basic statistical summaries."""
        stats_dict = {}
        
        # Numerical columns statistics
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            stats_dict[col] = {
                "mean": float(data[col].mean()),
                "median": float(data[col].median()),
                "std": float(data[col].std()),
                "min": float(data[col].min()),
                "max": float(data[col].max()),
                "skew": float(data[col].skew()),
                "kurtosis": float(data[col].kurtosis()),
            }
        
        # Categorical columns statistics
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = data[col].value_counts()
            stats_dict[col] = {
                "unique_values": int(data[col].nunique()),
                "most_common": value_counts.head(5).to_dict(),
                "missing_values": int(data[col].isnull().sum()),
            }
        
        return stats_dict

    def _generate_correlations(self, data: pd.DataFrame, target_column: Optional[str] = None) -> Dict:
        """Generate correlation analysis."""
        correlations = {}
        
        # Calculate correlations between numerical columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            correlations["matrix"] = corr_matrix.to_dict()
            
            # If target column is specified, calculate correlations with target
            if target_column and target_column in numeric_cols:
                target_correlations = corr_matrix[target_column].drop(target_column)
                correlations["target_correlations"] = target_correlations.to_dict()
        
        return correlations

    def _analyze_distributions(self, data: pd.DataFrame) -> Dict:
        """Analyze distributions of numerical columns."""
        distributions = {}
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            # Perform normality test
            _, p_value = stats.normaltest(data[col].dropna())
            
            # Calculate quartiles
            quartiles = data[col].quantile([0.25, 0.5, 0.75]).to_dict()
            
            distributions[col] = {
                "is_normal": p_value > 0.05,
                "p_value": float(p_value),
                "quartiles": quartiles,
            }
        
        return distributions

    def _generate_insights(self, data: pd.DataFrame, basic_stats: Dict, 
                         correlations: Dict, distributions: Dict) -> List[str]:
        """Generate human-readable insights from the analysis."""
        insights = []
        
        # Analyze numerical columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            stats = basic_stats[col]
            
            # Distribution insights
            if distributions[col]["is_normal"]:
                insights.append(f"{col} follows a normal distribution")
            else:
                insights.append(f"{col} does not follow a normal distribution")
            
            # Skewness insights
            if abs(stats["skew"]) > 1:
                direction = "right" if stats["skew"] > 0 else "left"
                insights.append(f"{col} is {direction}-skewed")
            
            # Outlier insights
            q1 = distributions[col]["quartiles"][0.25]
            q3 = distributions[col]["quartiles"][0.75]
            iqr = q3 - q1
            outliers = data[col][(data[col] < q1 - 1.5 * iqr) | (data[col] > q3 + 1.5 * iqr)]
            if len(outliers) > 0:
                insights.append(f"{col} has {len(outliers)} potential outliers")
        
        # Correlation insights
        if "target_correlations" in correlations:
            target_corr = correlations["target_correlations"]
            strong_correlations = {k: v for k, v in target_corr.items() if abs(v) > 0.5}
            if strong_correlations:
                insights.append("Strong correlations found with target variable:")
                for col, corr in strong_correlations.items():
                    direction = "positive" if corr > 0 else "negative"
                    insights.append(f"- {col} has a {direction} correlation of {abs(corr):.2f}")
        
        return insights 