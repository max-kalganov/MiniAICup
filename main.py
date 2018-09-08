import json
import random

while True:
    z = input()
    commands = ['left', 'right', 'stop']
    cmd = random.choice(commands)
    cmd = 'right'
    print(json.dumps({"command": cmd, 'debug': cmd}))