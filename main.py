import json
import random

while True:
    input_string = input()
    input_dict = json.loads(input_string)
    
    commands = ['left', 'right', 'stop']
    cmd = random.choice(commands)
    cmd = 'right'
    print(json.dumps({"command": cmd, 'debug': cmd}))