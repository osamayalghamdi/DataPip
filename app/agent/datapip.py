from typing import Dict, Any
from loguru import logger
import numpy as np
import os

from app.agent.base import BaseAgent
from app.schema import AgentCall, AgentResult, ToolCall, ToolResult
from app.tool.data_collector import DataCollector
from app.tool.data_cleaner import DataCleaner
from app.tool.data_analyzer import DataAnalyzer
from app.tool.visualization_generator import VisualizationGenerator
from app.tool.file_saver import FileSaver


class Datapip(BaseAgent):
    """DataPip agent specialized for data collection and preprocessing.
    
    This agent focuses on:
    1. Data collection from various sources
    2. Data cleaning and preprocessing
    3. Basic data analysis
    4. Visualization generation
    5. Saving results to files
    
    The agent stops after the preprocessing phase and does not proceed to analysis or visualization.
    """

    def __init__(self):
        super().__init__(
            name="Datapip",
            description="Data collection and preprocessing agent with CSV output",
            system_prompt="""You are DataPip, an expert data scientist specializing in analyzing, cleaning, and preprocessing data.
            Your primary goal is to intelligently analyze data, detect data types, and identify issues like outliers and missing values.
            You should save your results as clean CSV files.""",
            next_step_prompt="""Available tools:
            - DataCollector: Collect data from CSV files
            - DataCleaner: Clean and preprocess the data
            - DataAnalyzer: Analyze the data and generate insights
            - VisualizationGenerator: Create visualizations
            - FileSaver: Save results to files
            
            Analyze the data, apply appropriate preprocessing techniques, and save cleaned data as CSV files in the Output directory.""",
            max_steps=10  # Limit steps to focus on collection and preprocessing
        )
        self.available_tools = [
            DataCollector(),
            DataCleaner(),
            DataAnalyzer(),
            VisualizationGenerator(),
            FileSaver()
        ]

    async def _call(self, agent_call: AgentCall) -> AgentResult:
        """Execute the data preprocessing workflow."""
        try:
            logger.info("Starting data analysis and visualization workflow")
            
            # Step 1: Collect data
            result = await self._execute_tool("DataCollector", agent_call.arguments)
            if not result.success:
                return AgentResult(success=False, error=result.error)
            logger.info(f"Data collected successfully: {result.data['data'].shape[0]} rows, {result.data['data'].shape[1]} columns")
            
            # Step 2: Clean data
            result = await self._execute_tool("DataCleaner", {"data": result.data["data"]})
            if not result.success:
                return AgentResult(success=False, error=result.error)
            logger.info("Data cleaning completed successfully")
            
            # Step 3: Analyze data
            result = await self._execute_tool("DataAnalyzer", {"data": result.data["data"]})
            if not result.success:
                return AgentResult(success=False, error=result.error)
            logger.info("Data analysis completed successfully")
            
            # Step 4: Generate visualizations
            visualization_count = 0
            failed_visualizations = []
            numeric_cols = result.data["data"].select_dtypes(include=[np.number]).columns
            categorical_cols = result.data["data"].select_dtypes(exclude=[np.number]).columns
            
            logger.info(f"Found {len(numeric_cols)} numeric columns and {len(categorical_cols)} categorical columns")
            
            try:
                # Generate correlation heatmap for numeric columns (only if we have more than 2 numeric columns)
                if len(numeric_cols) > 2:
                    logger.info("Generating correlation heatmap...")
                    viz_result = await self._execute_tool(
                        "VisualizationGenerator",
                        {
                            "data": result.data["data"],
                            "plot_type": "correlation",
                            "x_column": numeric_cols[0],  # Not used for correlation plots
                            "title": "Correlation Heatmap"
                        }
                    )
                    if viz_result.success:
                        visualization_count += 1
                    else:
                        failed_visualizations.append(("correlation", "all numeric columns", viz_result.error))
                
                # Generate histograms and boxplots for numeric columns (limit to first 5)
                if len(numeric_cols) > 0:
                    logger.info("Generating plots for numeric columns...")
                    for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
                        for plot_type in ["histogram", "boxplot"]:
                            try:
                                viz_result = await self._execute_tool(
                                    "VisualizationGenerator",
                                    {
                                        "data": result.data["data"],
                                        "plot_type": plot_type,
                                        "x_column": col,
                                        "title": f"{plot_type.title()} of {col}"
                                    }
                                )
                                if viz_result.success:
                                    visualization_count += 1
                                else:
                                    failed_visualizations.append((plot_type, col, viz_result.error))
                            except Exception as e:
                                failed_visualizations.append((plot_type, col, str(e)))
                
                # Generate bar plots for categorical columns (limit to first 3, skip pie charts)
                if len(categorical_cols) > 0:
                    logger.info("Generating plots for categorical columns...")
                    for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                        try:
                            viz_result = await self._execute_tool(
                                "VisualizationGenerator",
                                {
                                    "data": result.data["data"],
                                    "plot_type": "bar",
                                    "x_column": col,
                                    "title": f"Bar Plot of {col}"
                                }
                            )
                            if viz_result.success:
                                visualization_count += 1
                            else:
                                failed_visualizations.append(("bar", col, viz_result.error))
                        except Exception as e:
                            failed_visualizations.append(("bar", col, str(e)))
                
                # Generate scatter plots for pairs of numeric columns (limit to first 3 columns)
                if len(numeric_cols) > 1:
                    logger.info("Generating scatter plots for numeric column pairs...")
                    for i, col1 in enumerate(numeric_cols[:3]):  # Limit to first 3 numeric columns
                        for col2 in numeric_cols[i+1:3]:  # Only pair with subsequent columns up to 3rd
                            try:
                                viz_result = await self._execute_tool(
                                    "VisualizationGenerator",
                                    {
                                        "data": result.data["data"],
                                        "plot_type": "scatter",
                                        "x_column": col1,
                                        "y_column": col2,
                                        "title": f"Scatter of {col1} vs {col2}"
                                    }
                                )
                                if viz_result.success:
                                    visualization_count += 1
                                else:
                                    failed_visualizations.append(("scatter", f"{col1} vs {col2}", viz_result.error))
                            except Exception as e:
                                failed_visualizations.append(("scatter", f"{col1} vs {col2}", str(e)))
                
                logger.info(f"Successfully generated {visualization_count} visualizations")
                if failed_visualizations:
                    logger.warning(f"Failed to generate {len(failed_visualizations)} visualizations:")
                    for plot_type, cols, error in failed_visualizations:
                        logger.warning(f"- {plot_type} plot for {cols}: {error}")
            
            except Exception as e:
                logger.error(f"Error during visualization generation: {str(e)}")
                return AgentResult(success=False, error=f"Visualization generation failed: {str(e)}")
            
            # Step 5: Save results
            output_file = os.path.join("Output", f"processed_{os.path.basename(agent_call.arguments['file_path'])}")
            result = await self._execute_tool("FileSaver", {
                "data": result.data["data"],
                "file_path": output_file
            })
            if not result.success:
                return AgentResult(success=False, error=result.error)
            logger.info("Results saved successfully")
            
            return AgentResult(success=True, data=result.data)
            
        except Exception as e:
            logger.error(f"Error in data preprocessing workflow: {str(e)}")
            return AgentResult(success=False, error=str(e))
