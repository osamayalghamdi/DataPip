class Coordinator:
    def __init__(self):
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)

    def orchestrate_workflow(self):
        for agent in self.agents:
            agent.perform_task()