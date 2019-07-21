import random


class MainStrategy:
    def __init__(self):
        self.steps = ['up', 'right', 'down', 'left']
        self.cur_index = 0

    def get_index(self, cur_index: int):
        new_index = cur_index+1
        if len(self.steps) >= new_index:
            new_index = 0
        return new_index

    def get_step(self):
        pass

    def get_command(self, state):
        commands = ['left', 'right', 'up', 'down']
        cmd = random.choice(commands)
        return cmd
