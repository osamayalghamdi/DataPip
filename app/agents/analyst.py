import autogen
from app.tools.data_analyzer import analyze_data

def analyze_data_function(data_path, analysis_type="descriptive"):
    """
    Function wrapper for data analyzer tool
    
    Args:
        data_path: Path to the data file
        analysis_type: Type of analysis to perform
        
    Returns:
        Analysis results
    """
    return analyze_data(data_path, analysis_type)

def create_analyst(config_list):
    """
    Create the data analyst agent
    
    Args:
        config_list: LLM configuration
        
    Returns:
        Data analyst agent
    """
    # Register the tools
    tools = [
        {
            "name": "analyze_data",
            "description": "Analyzes data to generate insights and statistical summaries",
            "function": analyze_data_function,
            "parameters": {
                "type": "object",
                "properties": {
                    "data_path": {
                        "type": "string",
                        "description": "Path to the data file"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["descriptive", "correlation", "outliers"],
                        "description": "Type of analysis to perform"
                    }
                },
                "required": ["data_path"]
            }
        }
    ]
    
    # Create the analyst agent
    return autogen.AssistantAgent(
        name="DataAnalyst",
        system_message="You are a data analysis expert. Your role is to analyze data and provide insights. "
                       "You can perform descriptive analysis, correlation analysis, and outlier detection.",
        llm_config={
            "config_list": config_list,
            "tools": tools
        }
    )