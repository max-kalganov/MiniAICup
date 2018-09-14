import json
from keras.models import Sequential
from keras.layers import Dense
import numpy

numpy.random.seed(2)

def reading_json(filename):
    fileobj = open(filename, "r")
    json_string = ""
    if fileobj.mode == "r":
        json_string = fileobj.read()
    match_params = json.loads(json_string)
    return match_params

def makeTrainAndTestSets(match_params_dict):
    match_params_train = []
    match_params_test = []
    return match_params_train, match_params_test

# сюда нужно подавать в параметры сет в котором столбцы - каждый тик и параметры для него: все параметры, кото
# рые даются в начале этого матча и все параметры за данный тик.

def train(match_params, correct_decision):
    model = Sequential()
    num_of_params, num_of_ticks = match_params.shape
    model.add(Dense(num_of_params, input_dim=num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(3, activation='sigmoid'))
    model.compile()
    model.fit()

    scores = model.evaluate()
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    return model


def main():
    filename = "train.json"
    match_params_dict = reading_json(filename)
    match_params_train, match_params_test = makeTrainAndTestSets(match_params_dict)

    # TODO: нужно ещё нормализовать данные
    model = train(match_params_train)

    #model.predict(...)
