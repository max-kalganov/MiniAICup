import json
import numpy as np
with open('visio','r') as f:
    json_data = f.read()



# [ ticknum,     , deadlineposition]
def getparams_TypeTick(params):
    l = []
    l.append(params['tick_num'])
    for car in params['cars']:
        for coordinate in params['cars'][car]:
            l.append(coordinate)
    l.append(params['deadline_position'])
    return l


def getparams_NewMatch(data):
    l = []
    for item in data:
        for seq in data[item]:
            # l.append(data[item][seq])
            if seq == 'button_poly' or seq == 'car_body_poly':
                for pos in data[item][seq]:
                    l.append(pos)
            if seq == 'front_wheel_position' or seq == 'rear_wheel_position' or seq == 'rear_wheel_joint':
                l.append(data[item][seq])
            if seq == 'rear_wheel_damp_position' or seq == 'front_wheel_damp_position':
                l.append(data[item][seq])
            if seq == 'segments':
                for pos in data[item][seq]:
                        l.append(np.hstack(pos))
    return l



parsed_data = json.loads(json_data)
ticks = []
new_match_info=[]

for data in parsed_data['visio_info']:
    if data['type'] == 'tick':
            ticks.append(np.hstack(getparams_TypeTick(data['params'])))
    if data['type'] == 'new_match':
            new_match_info.append(np.hstack(getparams_NewMatch(data['params'])))

print(new_match_info[0])