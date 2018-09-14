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
import time
from keras.utils import plot_model

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
testSet = np.array([[1., 0.2, 0.4],
                    [1., 0.6, 0.8],
                    [1., 0.1, 0.8],
                    [1., 0.8, 0.8],
                    [1., 0., 0.2],
                    [1., 0.6, 1.]])
answerSet_test = np.array([[1], [0], [1], [0], [1], [0]])

answerSet = np.array([[1], [1], [1], [1], [0], [0], [0], [0], [1], [1], [0], [0], [0], [1], [1]])

fig = plt.gcf()

#ax = fig.add_subplot(111)
fig.show()
fig.canvas.draw()

def realDraw(trainSet, answerSet):
    #print(trainSet)
    #print(answerSet)
    #return

    temp = []
    # print(self.answerSet_train)
    for r in answerSet:
        temp.append(r[0])
    temp = np.asarray(temp)

    dataSet_1 = trainSet[1:].transpose()[temp[:] == 1]
    dataSet_0 = trainSet[1:].transpose()[temp[:] == 0]
    dataSet_1 = dataSet_1.transpose()
    dataSet_0 = dataSet_0.transpose()
    print(dataSet_1.shape)

    plt.plot(dataSet_0[0], dataSet_0[1], "ob")
    plt.plot(dataSet_1[0], dataSet_1[1], "xr")
    y = []
    x = []
    time.sleep(0.9)
    fig.canvas.draw()
    #fig.canvas.flush_events()
    #.draw()







np.random.seed(2)

def train(trainSet, answerSet):
    model = Sequential()
    set_size, num_of_params = trainSet.shape
    model.add(Dense(num_of_params, input_dim=num_of_params, activation='linear'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
    model.fit(trainSet, answerSet,epochs=1000,batch_size=1)

    scores = model.evaluate(trainSet,answerSet)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    return model


weights = list()


def y_func(x, i):
    return float(-(weights[i][0] + weights[i][1] * x) / weights[i][2])


def main():
    realDraw(dataSet.transpose(), answerSet)

    model = train(dataSet, answerSet)
    global weights
    weights = model.layers[0].get_weights()[0]
    print("layer 0 : ", model.layers[0].get_weights()[0])
    print("layer 1 : ", model.layers[1].get_weights()[0])

    print("type weights: ", type(weights))
    print("weights: ", weights)
    print("model.weights: ", model.weights)
    print("model.output: ",model.output)

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

        plt.plot(x, y)
'''

    #plot_model(model,'model.png')   - это рисует схематичный график модели
    scores = model.evaluate(testSet, answerSet_test)
    print("checking accurance of the testSet:")
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    print("\npredicting ... \n")
    print(testSet)
    print(model.predict(testSet))

    plt.show()



main()


