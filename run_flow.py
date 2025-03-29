from typing import Dict, Any
from loguru import logger

from app.agent.datapip import Datapip

async def run_workflow(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Run the data preprocessing workflow."""
    try:
        agent = Datapip()
        result = await agent.run(arguments)
        
        if result.success:
            logger.info("Workflow completed successfully")
            return result.data
        else:
            logger.error(f"Workflow failed: {result.error}")
            return {"error": result.error}
            
    except Exception as e:
        logger.error(f"Error in workflow: {str(e)}")
        return {"error": str(e)}
