import json
import numpy as np

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
    for item in sorted(data):
        if item == 'proto_map':
                l.append(data[item].get('squared_wheels', False))

        for seq in sorted(data[item]):
                if seq == 'button_poly' or seq == 'car_body_poly':
                    for pos in data[item][seq]:
                        l.append(pos)
                elif seq == 'front_wheel_position' or seq == 'rear_wheel_position' or seq == 'rear_wheel_joint':
                    l.append(data[item][seq])
                elif seq == 'rear_wheel_damp_position' or seq == 'front_wheel_damp_position':
                    l.append(data[item][seq])
                elif seq == 'segments' or seq == 'squared_wheels':
                    pass
                else:
                    l.append(data[item][seq])
    return l


def parser(filenameDump='visio', keyboardfilename='KeyboardDebug', logfilename='1.log'):
    ticks = []
    with open(filenameDump, 'r') as f:
        Dump_data = f.read()
    with open(keyboardfilename, 'r') as f:
        answer_data = np.asarray(list(map(int, f.read().split()))).reshape(-1, 1)
    parsed_data = json.loads(Dump_data)

    for data in parsed_data['visio_info']:
        if data['type'] == 'tick':
                ticks.append(np.concatenate((np.hstack(getparams_TypeTick(data['params'])), new_match_info)))
        if data['type'] == 'new_match':
            new_match_info = np.hstack(getparams_NewMatch(data['params']))
    ticks = removeBadTicks(np.array(ticks).T, logfilename)

    return ticks, answer_data


def removeBadTicks(dump, name='1.log'):
    with open(name, 'r') as f:
        Log = f.read()
    Log = json.loads(Log)
    c = 0
    l = []
    for tick in Log:
        if c != tick['tick']:
            c = tick['tick']
        l.append(c)
        c += 1
    print(dump[:, l])
    return dump[:, l]


p = parser()
print(p[0].shape)
print(p[1].shape)
