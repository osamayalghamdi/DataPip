# 👋 DataPip: Smart Data Workflows

Welcome to **DataPip**! This project leverages the powerful **Manus** AI assistant to create an intelligent data pipeline system that collects data, analyzes it, and generates visualizations—all orchestrated by AI. Built to be smart, flexible, and simple to use.

## Features

- **AI-Driven Data Collection**: Automatically gather data from files, APIs, and databases
- **Intelligent Analysis**: Leverage ML techniques for insights and pattern recognition
- **Dynamic Visualization**: Create charts and graphs optimized for your data
- **OpenManus Integration**: Uses Manus AI's planning capabilities to orchestrate complex workflows

## Installation

### Setting Up DataPip

Follow these steps to get DataPip up and running on your system:

### Step 1: Clone the Project

1. Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux).
2. Go to where you want the project:
   ```bash
   cd ~/projects  # Pick any folder you like
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/mannaandpoem/OpenManus.git
   ```
4. Enter the project folder:
   ```bash
   cd OpenManus
   ```

### Step 2: Set Up a Virtual Environment

1. Create a virtual environment with Python 3.12:

   ```bash
   python3 -m venv .venv  # On macOS/Linux
   # Or on Windows:
   # python -m venv .venv
   ```

   - This makes a `.venv` folder in your project directory.

2. Activate the virtual environment:
   - On **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - You’ll see `(.venv)` in your terminal prompt, showing it’s active.

### Step 3: Install Dependencies

1. Install the project’s requirements:
   ```bash
   pip install -r requirements.txt
   ```
   - This grabs all the tools and libraries OpenManus needs.

### Step 4: Configure the Project

1. Copy the example config file:
   ```bash
   cp config/config.example.toml config/config.toml
   ```
2. Open `config/config.toml` in a text editor and add your API key:
   ```toml
   [llm]
   model = "gpt-4o"
   base_url = "https://api.openai.com/v1"
   api_key = "sk-..."  # Replace with your API key
   max_tokens = 4096
   temperature = 0.0
   ```
3. Save the file.

### Step 5: Run It!

1. Start the project:
   ```bash
   python main.py
   ```
2. Type something like “collect data and make a chart” to test it.

### Step 6: Exit When Done

To leave the virtual environment:

```bash
deactivate
```

