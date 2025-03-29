# DataPip

A powerful data preprocessing and visualization tool that helps you analyze and understand your data through automated processing and visualization generation.

## Features

- CSV file processing and analysis
- Automated data cleaning and preprocessing
- Statistical analysis and insights generation
- Multiple visualization types:
  - Histograms
  - Box plots
  - Scatter plots
  - Correlation heatmaps
  - Bar charts
  - Pie charts
- Output saved in CSV format with analysis reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/datapip.git
cd datapip
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your CSV files in the `data` directory.

2. Run the program:
```bash
python main.py
```

3. Select a file to process or choose to process all files.

4. The processed data and analysis reports will be saved in the `Output` directory.

## Project Structure

```
datapip/
├── app/
│   ├── agent/
│   │   ├── base.py
│   │   └── datapip.py
│   ├── tool/
│   │   ├── base.py
│   │   ├── data_collector.py
│   │   ├── data_cleaner.py
│   │   ├── data_analyzer.py
│   │   ├── visualization_generator.py
│   │   └── file_saver.py
│   ├── schema.py
│   └── llm.py
├── data/
├── Output/
├── logs/
├── main.py
├── requirements.txt
└── setup.py
```

## Dependencies

- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scikit-learn >= 1.3.0
- pydantic >= 2.0.0
- loguru >= 0.7.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

