import random


def get_command(state):
    commands = ['left', 'right', 'up', 'down']
    cmd = random.choice(commands)
    return cmd
