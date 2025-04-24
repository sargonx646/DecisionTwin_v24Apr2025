class Moderator:
    def __init__(self, mode):
        self.mode = mode
        self.stage = 0

    def prompt(self, agent, state):
        stages = ["Define the issue", "Present proposals", "Debate pros/cons", "Summarize and propose consensus"]
        current_stage = stages[self.stage % len(stages)]
        self.stage += 1
        return f"[{current_stage}] {agent['name']}, based on your role and bias, respond accordingly."