import torch

class Brain:
    def __init__(self, model):
        self.brain = model

    def action(self, state):
        return torch.argmax(self.brain(torch.tensor(state, dtype=torch.float32))).item()

    def save(self, path):
        torch.save(self.brain.state_dict(), path)

    def load(self, path):
        self.brain.load_state_dict(torch.load(path))
