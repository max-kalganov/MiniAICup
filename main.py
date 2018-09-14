import json
from keras.models import load_model
import numpy as np

def format_new_match_params(params):
    pass

def format_tick_params(params):
    pass

def get_params(input_string):
    params = None
    input_dict = json.loads(input_string)
    input_list = list(input_dict.items())
    # shape should be 1xNumOfParams
    if (input_list[0][1] == "new_match"):
        match_params = format_new_match_params(input_list[1][1])
    else:
        tick_params = format_tick_params(input_list[1][1])
        params = 0



    #TODO: get params  = match_params + tick_params + all_other_params
    return params

match_params = None
commands = ['left', 'right', 'stop']
model = load_model('my_model.h5')

while True:
    input_string = input()
    params = get_params(input_string)
    pred = np.argmax(model.predict(params))
    cmd = commands[pred]
    print(json.dumps({"command": cmd, 'debug': cmd}))