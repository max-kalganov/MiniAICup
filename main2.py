import json
match_params = None
commands = ['left', 'right', 'stop']

tick =1
while True:
    input_string = input()
    cmd = 'stop'
    if tick%30 == 0:
        cmd = commands[1]
    print(json.dumps({"command": cmd, 'debug': cmd}))
    tick+=1