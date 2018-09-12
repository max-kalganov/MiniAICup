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

def train(match_params):



def main():
    filename = "train.json"
    match_params_dict = reading_json(filename)
    match_params_train, match_params_test = makeTrainAndTestSets(match_params_dict)
    model = train(match_params_train)

