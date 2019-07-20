import json
import random


def here():
    print("here")


while True:
    z = input()
    commands = ['left', 'right', 'up', 'down']
    cmd = random.choice(commands)
    print(json.dumps({"command": cmd, 'debug': str(z)}))