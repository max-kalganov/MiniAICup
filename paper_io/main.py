import json

from my_strategy.main_strategy import MainStrategy

ms = MainStrategy()
while True:
    state = input()
    cmd = ms.get_command(state)
    print(json.dumps({"command": cmd, 'debug': str(state)}))