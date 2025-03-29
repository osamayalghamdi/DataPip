import os
import asyncio
from loguru import logger

from app.agent.datapip import Datapip

async def process_csv_file(file_path: str):
    """Process a single CSV file."""
    try:
        agent = Datapip()
        result = await agent.run({"file_path": file_path})
        
        if result.success:
            logger.info(f"Successfully processed {file_path}")
            logger.info(f"Output saved to Output/processed_{os.path.basename(file_path)}")
            logger.info(f"Analysis report saved to Output/analysis_{os.path.basename(file_path).replace('.csv', '.txt')}")
        else:
            logger.error(f"Failed to process {file_path}: {result.error}")
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")

async def main():
    """Main entry point."""
    print("\nDataPip - Data Analysis and Visualization System")
    print("===============================================\n")
    
    # Get list of CSV files in data directory
    data_dir = "data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the data directory.")
        return
    
    print("Available CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
    choice = input("\nEnter a number to process a specific file or 'a' to process all files: ")
    
    if choice.lower() == 'a':
        logger.info("Processing all CSV files...")
        for file in csv_files:
            await process_csv_file(os.path.join(data_dir, file))
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(csv_files):
                await process_csv_file(os.path.join(data_dir, csv_files[index]))
            else:
                print("Invalid choice. Exiting.")
        except ValueError:
            print("Invalid input. Please enter a number or 'a'. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
