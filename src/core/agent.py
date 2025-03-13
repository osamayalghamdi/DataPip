class Agent:
    def __init__(self, name):
        self.name = name

    def start(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def stop(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def send_message(self, message):
        raise NotImplementedError("Subclasses should implement this method.")

    def receive_message(self, message):
        raise NotImplementedError("Subclasses should implement this method.")