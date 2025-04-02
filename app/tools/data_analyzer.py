import pandas as pd
import numpy as np
from loguru import logger
import json
import os

def analyze_data(data_path, analysis_type="descriptive"):
    """
    Analyze data to generate insights and statistical summaries.
    
    Args:
        data_path: Path to the data file
        analysis_type: Type of analysis to perform
        
    Returns:
        Analysis results
    """
    try:
        # Load the data
        data = pd.read_csv(data_path)
        
        # Determine the analysis function
        if analysis_type == "descriptive":
            results = _descriptive_analysis(data)
        elif analysis_type == "correlation":
            results = _correlation_analysis(data)
        elif analysis_type == "outliers":
            results = _outlier_detection(data)
        else:
            results = _descriptive_analysis(data)
        
        # Save results to a file
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"{analysis_type}_analysis.json")
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Analysis results saved to {output_path}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")
        return {"error": str(e)}

def _descriptive_analysis(data):
    """Generate basic statistical summaries"""
    return {
        "shape": data.shape,
        "describe": data.describe().to_dict(),
        "missing": data.isna().sum().to_dict(),
        "dtypes": data.dtypes.astype(str).to_dict()
    }

def _correlation_analysis(data):
    """Generate correlation analysis"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    corr_matrix = data[numeric_cols].corr()
    
    return {
        "correlation_matrix": corr_matrix.to_dict()
    }

def _outlier_detection(data, threshold=3):
    """Detect outliers using z-score method"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    results = {}
    
    for col in numeric_cols:
        z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
        outliers = np.where(z_scores > threshold)[0].tolist()
        results[col] = {"outlier_indices": outliers, "count": len(outliers)}
    
    return results