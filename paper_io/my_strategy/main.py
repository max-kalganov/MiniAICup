import json

from my_strategy.main_strategy import get_command

while True:
    state = input()
    cmd = get_command(state)
    print(json.dumps({"command": cmd, 'debug': str(state)}))