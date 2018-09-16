from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model

from jsonnumpy import parser

np.random.seed(2)

def makeTrainAndTestSets(match_params, match_moves):
    match_params, match_moves = parser()
    # TODO: а здесь перевод их в numpy. формат такой : match_params_train, match_params_test - (количество тиков, количество параметров)
    # TODO: а формат match_moves_train, match_moves_test - столбец ходов.(не меняй названия движений на цифры. у меня эот есть)
    train_set_size = int(0.7 * match_moves.shape[0])

    match_params_train = match_params[:,:train_set_size]
    match_params_test = match_params[:, train_set_size:]
    match_moves_train = match_moves[:,:train_set_size]
    match_moves_test = match_moves[:, train_set_size:]
    return match_params_train, match_params_test, match_moves_train, match_moves_test


def format_answerSet(answerSet):
    encoder = LabelEncoder()
    encoder.fit(answerSet)
    encoded_y = encoder.transform(answerSet)
    dummy_y = np_utils.to_categorical(encoded_y)
    print("encoded answerSet = ", dummy_y)
    return dummy_y


def train(match_params, correct_decision):
    # format answerSet
    dummy_y = format_answerSet(correct_decision)

    model = Sequential()
    set_size, num_of_params = match_params.shape

    model.add(Dense(num_of_params, input_dim=num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(num_of_params, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    model.fit(match_params, dummy_y, epochs=1500, batch_size=2)

    scores = model.evaluate()
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    return model


filename = "train.json"

def main():
    match_params_train, match_params_test, match_moves_train, match_moves_test = makeTrainAndTestSets()

    # TODO: нужно ещё нормализовать данные
    model = train(match_params_train, match_moves_train)
    # TODO: нужно проследить, что при предсказании мы получаем 0='left' 1='right' 2='stop'
    dummy_y = format_answerSet(match_moves_test)
    scores = model.evaluate(match_params_test, dummy_y)
    print("checking accurance of the testSet:")
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    #model.predict(...)
    model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
    del model

def upload_model_and_fit_new_trainSet():
    match_params_train, match_params_test, match_moves_train, match_moves_test = makeTrainAndTestSets()
    # TODO: check the file you are loading....
    model = load_model('my_model.h5')
    dummy_y = format_answerSet(match_moves_test)
    scores = model.evaluate(match_params_test, dummy_y)
    print("checking accurance of the testSet:")
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    dummy_y_fit = format_answerSet(match_moves_train)
    model.fit(match_params_train, dummy_y_fit, epochs=1500, batch_size=2)

    scores = model.evaluate(match_params_test, dummy_y)
    print("checking accurance of the testSet:")
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    print("did you check the file name? is that file correct one? Y/N")
    ans = input()
    if(ans == "Y" or ans == "y"):
        model.save('my_model_new.h5')

main()