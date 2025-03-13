# Coordinator Agent System

## Overview
The Coordinator Agent System is designed to facilitate the orchestration of workflows among various agents responsible for data collection, analysis, and visualization. This modular architecture allows for easy extension and integration of new functionalities.

## Project Structure
```
engcoordinator_agent_system
├── src
│   ├── core
│   │   ├── agent.py              # Base class for all agents.
│   │   ├── coordinator.py        # Base coordinator with workflow orchestration.
│   │   └── message.py            # Basic message structure for agent communication.
│   │
│   ├── agents
│   │   ├── master_coordinator.py # Top-level coordinator delegating tasks.
│   │   ├── data_agent.py         # Handles data collection and cleaning.
│   │   ├── analysis_agent.py     # Manages data analysis and modeling.
│   │   └── visualization_agent.py # Generates charts and reports.
│   │
│   ├── tools
│   │   ├── data_tools.py         # Integrates pyjanitor, cleanlab, and LLM cleaning.
│   │   ├── analysis_tools.py     # Provides analysis utilities.
│   │   └── viz_tools.py          # Wraps visualization libraries (Plotly, Altair).
│   │
│   └── system
│       ├── workflow_manager.py   # Controls the overall task execution and flow.
│       └── config_manager.py     # Loads configuration settings.
├── config
│   └── agent_config.yaml         # Defines agent roles, relationships, and tool settings.
└── requirements.txt              # Lists project dependencies.
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd engcoordinator_agent_system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the system, you can initiate the `MasterCoordinator` which will manage the workflow among the various agents. Each agent can be customized through the configuration file located at `config/agent_config.yaml`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.