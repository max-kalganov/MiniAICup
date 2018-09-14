from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder




np.random.seed(2)

def reading_json(filename):
    # TODO: напиши здесь плиз часть про чтение json файла
    match_params = []
    match_moves = []
    return match_params, match_moves

def makeTrainAndTestSets(match_params, match_moves):
    # TODO: а здесь перевод их в numpy. формат такой : match_params_train, match_params_test - (количество тиков, количество параметров)
    # TODO: а формат match_moves_train, match_moves_test - столбец ходов.(не меняй названия движений на цифры. у меня эот есть)
    match_params_train = []
    match_params_test = []
    match_moves_train = []
    match_moves_test = []
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
    model.add(Dense(3, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    model.fit(match_params, dummy_y, epochs=500, batch_size=2)

    scores = model.evaluate()
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    return model


def main():
    filename = "train.json"
    match_params, match_moves = reading_json(filename)
    match_params_train, match_params_test, match_moves_train, match_moves_test = makeTrainAndTestSets(match_params, match_moves)

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