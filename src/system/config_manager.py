class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        import yaml
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get_agent_config(self, agent_name):
        return self.config_data.get(agent_name, {})

    def update_config(self, agent_name, new_config):
        self.config_data[agent_name] = new_config
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as file:
            yaml.dump(self.config_data, file)