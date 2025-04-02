import os
import autogen
from app.agents.user_proxy import create_user_proxy
from app.agents.assistant import create_assistant
from app.agents.collector import create_collector
from app.agents.analyst import create_analyst
from app.agents.visualizer import create_visualizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Create the agent group
    config_list = [
        {
            "model": "gpt-4o",
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    ]
    
    # Create the agents
    user_proxy = create_user_proxy()
    assistant = create_assistant(config_list)
    collector = create_collector(config_list)
    analyst = create_analyst(config_list)
    visualizer = create_visualizer(config_list)
    
    # Connect agents in a group chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, assistant, collector, analyst, visualizer],
        messages=[],
        max_round=50
    )
    manager = autogen.GroupChatManager(groupchat=groupchat)
    
    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message="I have a CSV file in the data directory called sample_employees.csv. "
                "Can you analyze it and create some visualizations to understand the data better?"
    )

if __name__ == "__main__":
    main()