import json
from keras.models import load_model
import numpy as np


def format_new_match_params(data):
    l = []
    for item in sorted(data):
        for seq in sorted(data[item]):
            if seq == 'button_poly' or seq == 'car_body_poly':
                for pos in sorted(data[item][seq]):
                    l.append(pos)
            elif seq == 'front_wheel_position' or seq == 'rear_wheel_position' or seq == 'rear_wheel_joint':
                l.append(data[item][seq])
            elif seq == 'rear_wheel_damp_position' or seq == 'front_wheel_damp_position':
                l.append(data[item][seq])
            elif seq == 'segments':
                for pos in sorted(data[item][seq]):
                    l.append(np.hstack(pos))
            else:
                l.append(data[item][seq])
    return l


def format_tick_params(params):
    l = []
    l.append(params['tick_num'])
    for car in params['cars']:
        for coordinate in params['cars'][car]:
            l.append(coordinate)
    l.append(params['deadline_position'])
    return l


def get_params(input_string):
    params = None
    input_dict = json.loads(input_string)

    for data in input_dict['visio_info']:
        if data['type'] == 'tick':
            params.append(np.hstack(format_tick_params(data['params'])))
        if data['type'] == 'new_match':
            new_match = np.hstack(format_new_match_params(data['params']))



    # TODO: get params  = match_params + tick_params + all_other_params
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