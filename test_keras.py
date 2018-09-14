'''
import numpy as np
a = [1,3,4,5]
b = 2
c = np.array(a)
c = np.reshape(c,(2,2))
d = a,b,c
print(d[2])

'''
'''
import json

json_data = '{"round1":{"type1": "new match", "params1":{"a":1}, "type2": "tick", "params2":{"b":1}, "type3": "tick", "params3":{"b":1}}}'
y = json.loads(json_data)
l = list(y.items())
print(l[0][1])
'''




from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

dataSet = np.array([[1., 0.08518521,0.45985378],
                    [1., 0.13851827, 0.9419858 ],
                    [1., 0.30878526, 0.20883611],
                    [1., 0.0160247,  0.92335785],
                    [1., 0.74256369, 0.3699414 ],
                    [1., 0.54611513, 0.81464114],
                    [1., 0.8134179,  0.59915756],
                    [1., 0.76095869, 0.95217406],
                    [1., 0.05084209, 0.3055774 ],
                    [1., 0.02228888, 0.62681387],
                    [1., 0.51587439, 0.7808052 ],
                    [1., 0.72270179, 0.48777485],
                    [1., 0.81538251, 0.89336511],
                    [1., 0.21282806, 0.08611013],
                    [1., 0.22962954, 0.19158838]])
testSet = np.array([[1., 0.2, 0.5],
                    [1., 0.6, 0.8],
                    [1., 0.1, 0.8],
                    [1., 0.8, 0.8],
                    [1., 0., 0.2],
                    [1., 0.6, 1.],
                    [1., 0.4, 0.2]])
answerSet_test = np.array([[1], [0], [1], [0], [2], [0], [2]])
answerSet = np.array([[1], [1], [2], [1], [0], [0], [0], [0], [2], [1], [0], [0], [0], [2], [2]])

fig = plt.gcf()
fig.show()
fig.canvas.draw()


def realDraw(trainSet, answerSet):
    temp = []
    for r in answerSet:
        temp.append(r[0])
    temp = np.asarray(temp)

    dataSet_2 = trainSet[1:].transpose()[temp[:] == 2]
    dataSet_1 = trainSet[1:].transpose()[temp[:] == 1]
    dataSet_0 = trainSet[1:].transpose()[temp[:] == 0]

    dataSet_2 = dataSet_2.transpose()
    dataSet_1 = dataSet_1.transpose()
    dataSet_0 = dataSet_0.transpose()
    print(dataSet_1.shape)

    plt.plot(dataSet_0[0], dataSet_0[1], "ob")
    plt.plot(dataSet_1[0], dataSet_1[1], "xr")
    plt.plot(dataSet_2[0], dataSet_2[1], "xg")

    fig.canvas.draw()

seed = 2
np.random.seed(seed)


def format_answerSet(answerSet):
    encoder = LabelEncoder()
    encoder.fit(answerSet)
    encoded_y = encoder.transform(answerSet)
    dummy_y = np_utils.to_categorical(encoded_y)
    print("encoded answerSet = ", dummy_y)
    return dummy_y

def train(trainSet, answerSet):

    dummy_y = format_answerSet(answerSet)

    model = Sequential()
    set_size, num_of_params = trainSet.shape
    model.add(Dense(num_of_params, input_dim=num_of_params, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    model.fit(trainSet, dummy_y,epochs=500,batch_size=2)
    return model



def main():
    realDraw(dataSet.transpose(), answerSet)

    model = train(dataSet, answerSet)
    print("layer 0 : ", model.layers[0].get_weights()[0])
    print("layer 1 : ", model.layers[1].get_weights()[0])
    print("model.weights: ", model.weights)
    print("model.output: ",model.output)
    # plot_model(model,'model.png')   - это рисует схематичный график модели

    dummy_y = format_answerSet(answerSet_test)

    scores = model.evaluate(testSet, dummy_y)
    print("checking accurance of the testSet:")
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    print("\npredicting ... \n")
    print(testSet)
    print(model.predict(testSet))

    pred = model.predict(np.array([[1., 0., 0.2]]))
    print("should be [0 0 1]: " , pred)
    print("type of the prediction: ", type(pred))
    print("real answer: ", np.argmax(pred))
    plt.show()

#TODO: эта херь не работает, а точнее: я не знаю, какие параметры нужно брать, чтобы правильно отобразить то, что там получилось
    # поэтому рисуется какая-то чушь. дальше я проверил, насколько правильно работает модель, но с ней вроде все норм.
    # значения по крайней мере выдает правильные.
    '''for j in range (0,2):
        x, y = [], []
        for i in range(0, 10):
            x.append(i / 10)
            # y.append(i/10)
            y.append(y_func(i / 10, j))
        print("x = ", x)
        print("y = ", y)

        plt.plot(x, y)'''



main()
