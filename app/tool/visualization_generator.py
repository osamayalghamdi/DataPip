from typing import Dict, List, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from loguru import logger

from app.schema import Tool, ToolCall, ToolResult
from app.tool.base import BaseTool


class VisualizationGenerator(BaseTool):
    """Tool for generating various types of visualizations from data."""

    def __init__(self):
        super().__init__(
            name="VisualizationGenerator",
            description="Generates various types of visualizations from data",
            parameters={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "The DataFrame to visualize",
                    },
                    "plot_type": {
                        "type": "string",
                        "enum": ["histogram", "boxplot", "scatter", "correlation", "bar", "pie"],
                        "description": "Type of visualization to generate",
                    },
                    "x_column": {
                        "type": "string",
                        "description": "Column to use for x-axis",
                    },
                    "y_column": {
                        "type": "string",
                        "description": "Column to use for y-axis (if applicable)",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the visualization",
                    },
                },
                "required": ["data", "plot_type", "x_column"],
            },
        )

    async def _call(self, tool_call: ToolCall) -> ToolResult:
        """Generate the requested visualization."""
        try:
            data = tool_call.arguments["data"]
            plot_type = tool_call.arguments["plot_type"]
            x_column = tool_call.arguments["x_column"]
            y_column = tool_call.arguments.get("y_column")
            title = tool_call.arguments.get("title", f"{plot_type.title()} Plot")

            # Set the style
            plt.style.use('default')
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Generate the visualization based on plot type
            if plot_type == "histogram":
                self._create_histogram(data, x_column, ax)
            elif plot_type == "boxplot":
                self._create_boxplot(data, x_column, ax)
            elif plot_type == "scatter":
                if not y_column:
                    raise ValueError("y_column is required for scatter plots")
                self._create_scatter(data, x_column, y_column, ax)
            elif plot_type == "correlation":
                self._create_correlation_heatmap(data, ax)
            elif plot_type == "bar":
                self._create_bar_plot(data, x_column, ax)
            elif plot_type == "pie":
                self._create_pie_chart(data, x_column, ax)
            
            # Set title and labels
            ax.set_title(title)
            
            # Convert plot to base64 string
            img_data = self._fig_to_base64(fig)
            plt.close(fig)
            
            return ToolResult(
                success=True,
                data={
                    "image": img_data,
                    "plot_type": plot_type,
                    "title": title,
                },
            )

        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            return ToolResult(success=False, error=str(e))

    def _create_histogram(self, data: pd.DataFrame, column: str, ax: plt.Axes):
        """Create a histogram plot."""
        sns.histplot(data=data, x=column, ax=ax)
        ax.set_xlabel(column)
        ax.set_ylabel("Count")

    def _create_boxplot(self, data: pd.DataFrame, column: str, ax: plt.Axes):
        """Create a box plot."""
        sns.boxplot(data=data, y=column, ax=ax)
        ax.set_ylabel(column)

    def _create_scatter(self, data: pd.DataFrame, x_column: str, y_column: str, ax: plt.Axes):
        """Create a scatter plot."""
        sns.scatterplot(data=data, x=x_column, y=y_column, ax=ax)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

    def _create_correlation_heatmap(self, data: pd.DataFrame, ax: plt.Axes):
        """Create a correlation heatmap."""
        numeric_data = data.select_dtypes(include=[np.number])
        corr_matrix = numeric_data.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)

    def _create_bar_plot(self, data: pd.DataFrame, column: str, ax: plt.Axes):
        """Create a bar plot."""
        value_counts = data[column].value_counts()
        value_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)

    def _create_pie_chart(self, data: pd.DataFrame, column: str, ax: plt.Axes):
        """Create a pie chart."""
        value_counts = data[column].value_counts()
        value_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")

    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Convert matplotlib figure to base64 string."""
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8') 