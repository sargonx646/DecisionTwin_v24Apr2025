class StateTracker:
    def __init__(self, agents):
        self.agents = agents
        self.turn = 0
        self.history = []
        self.max_turns = 12

    def next_speaker(self):
        return self.agents[self.turn % len(self.agents)]

    def record_response(self, speaker, content):
        self.history.append((speaker['name'], content))
        self.turn += 1

    def finished(self):
        return self.turn >= self.max_turns