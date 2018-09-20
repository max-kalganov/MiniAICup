import json
import numpy as np


def matchInfo_parser(matchDump):
    matchInfo = []
    proto_map = parse_one_dump(matchDump['proto_map'])
    proto_map = np.delete(proto_map,-1)
    proto_map = np.reshape(proto_map,(proto_map.shape[0],1))

    proto_car = parse_one_dump(matchDump['proto_car'])
    proto_car = np.delete(proto_car, -1)
    proto_car = np.reshape(proto_car, (proto_car.shape[0], 1))

    matchInfo = np.concatenate((proto_map, proto_car))
    print("matchInfo shape: ", matchInfo.shape)
    # matchInfo should be a numpy.array column, with shape = (num of params, 1)
    return matchInfo


def parse_one_dump(dump):
    info_list = []
    dump_list = list(dump.items())
    for d in dump_list:
        if type(d[1])  == type([]):
            info_list = info_list + appendList(d[1])
        else:
            info_list.append(d[1])
    if dump_list[-1][0] != 'squared_wheels':
        info_list.append(False)
    info = np.array(info_list)
    info = np.reshape(info, (len(info_list), 1))
    print("info shape = ", info.shape)
    print("info = ",info)
    return info

def appendList(list):
    res = []
    for i in list:
        if type(i) == type([]):
            res += appendList(i)
        else:
            res.append(i)
    return res


# order = 0 : first goes player 1, then player 2; order = 1: vice versa
def parse_cars_for_train(dump_cars, order=0):
    carsInfo = parse_one_dump(dump_cars['1'])
    if order == 0:
        carsInfo += parse_one_dump(dump_cars['2'])
    elif order == 1:
        carsInfo = parse_one_dump(dump_cars['2']) + carsInfo
    print(carsInfo)
    return carsInfo


def parse_ticks_for_train(tickDump):
    carsInfo = parse_cars_for_train(tickDump['cars'])
    tick_num_numpy = np.array([[tickDump['tick_num']]])
    deadline_pos_numpy = np.array([[tickDump['deadline_position']]])
    tickForTrain = np.concatenate((tick_num_numpy, carsInfo, deadline_pos_numpy))
    return tickForTrain


def parse_cars_for_play(dump_cars):
    carsInfo = parse_one_dump(dump_cars['my_car']) + parse_one_dump('enemy_car')
    return carsInfo


# TODO: you can combine parse_ticks_for_play and parse_ticks_for_train in one method
def parse_ticks_for_play(tickDump):
    carsInfo = parse_cars_for_train(tickDump['cars'])
    deadline_pos_numpy = np.array([[tickDump['deadline_position']]])
    tickForTrain = np.concatenate((carsInfo, deadline_pos_numpy))
    return tickForTrain


#args == 't' - it means 'train', 'p' - 'play'
def ticksInfo_parser(tickDump, args='p'):
    tickInfo = None
    if args == 'p':
        tickInfo = parse_ticks_for_play(tickDump)
    elif args == 't':
        tickInfo = parse_ticks_for_train(tickDump)

    # tickInfo should be a numpy.array column, with shape = (num of params, 1)
    return tickInfo


def mainInfo_parser(filenameDump='visio'):
    resultSet = None

    with open(filenameDump, 'r') as f:
        Dump_data = f.read()
    parsed_data = json.loads(Dump_data)

    for data in parsed_data['visio_info']:
        if data['type'] == 'new_match':
            current_match_info = np.array(matchInfo_parser(data['params']))
        elif data['type'] == 'tick':
            current_tick_info = ticksInfo_parser(data['params'],'t')
            new_result_column_of_data = np.concatenate((current_tick_info, current_match_info))
            if resultSet == None:
                resultSet = new_result_column_of_data
                continue
            resultSet = np.concatenate((resultSet, new_result_column_of_data), axis=1)
    #resultSet should be np.array with shape = (num_of params, num of ticks)
    return resultSet


def moves_parser(keyboardfilename='KeyboardDebug'):
    with open(keyboardfilename, 'r') as f:
        answer_data = np.asarray(list(map(int, f.read().split()))).reshape(-1, 1)
    return answer_data


def ticks_parser(name):
    with open(name, 'r') as f:
        tick_log = f.read()
    tick_log = json.loads(tick_log)
    good_ticks = []
    for tick in tick_log:
        good_ticks.append(tick['tick'])
    return good_ticks


def removeBadTicks(dump, name='1.log'):
    good_ticks = ticks_parser(name)
    # 1: - without first string (tick_num)
    resDump = dump
    return resDump


def getDataSet_and_AnswerSet():
    matchAndTickInfo = mainInfo_parser()
    movesInfo = moves_parser()
    matchAndTickInfo = removeBadTicks(matchAndTickInfo)
    return matchAndTickInfo, movesInfo

#getDataSet_and_AnswerSet()
z = input()
a = json.loads(z)
print(matchInfo_parser(a))
''' -----------------------------------------------------------------------------------'''


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

def temp_for_bad_position():
    good_ticks = []
    dump = []
    resDump = []
    l = []
    for j in good_ticks:
       resDump.append(dump[j])

    dump = np.array(resDump)
    for i,r in enumerate(dump):
        if len(dump[i]) != 74:
            print(len(dump[i]))

    print(dump.shape)
    return dump[1:, l]


