import numpy as np
import matplotlib.pyplot as plt

X = np.array(([0, 0], [0, 1], [1, 0], [1, 1]),)
#Y = np.array(([0], [1], [1], [0]),)
Y = np.array([0, 1, 1, 0])

import warnings
warnings.filterwarnings('ignore')

class NeuralNet():
    def __init__(self, network_architecture, switch=None):
        # create seed for random number generation
        np.random.seed(0)
        self.switch = switch
        self.num_layers = len(network_architecture)
        self.architecture = network_architecture
        self.weights = []

        # initialize weight values
        for layer in range(self.num_layers - 1):
            weight = 2*np.random.rand(network_architecture[layer] + 1, network_architecture[layer+1]) - 1
            self.weights.append(weight)

    def relu(self, x):
        return np.where(x < 0, 0.01 * x, x)

    def relu_d(self, x):
        return np.where(x < 0, 0.01, 1)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_d(self, x):
        return x * (1.0 - x)

    def tanh(self, x):
        return (1.0 - np.exp(-2 * x)) / (1.0 + np.exp(-2 * x))

    def tanh_d(self, x):
        return (1 + self.tanh(x)) * (1 - self.tanh(x))

    def act(self, x):
        if self.switch == "relu":
            return self.relu(x)
        elif self.switch == "tanh":
            return self.tanh(x)
        else:
            return self.sigmoid(x)

    def act_d(self, x):
        if self.switch == "relu":
            return self.relu_d(x)
        elif self.switch == "tanh":
            return self.tanh(x)
        else:
            return self.sigmoid_d(x)

    def forward(self, x):
        y = x
        for i in range(len(self.weights)-1):
            weighted_sum = np.dot(y[i], self.weights[i])
            layer_output = self.act(weighted_sum)

            # add bias - always on neuron
            layer_output = np.concatenate((np.ones(1), np.array(layer_output)))
            y.append(layer_output)
        weighted_sum = np.dot(y[-1], self.weights[-1])
        layer_output = self.act(weighted_sum)
        y.append(layer_output)
        return y

        # old code
        '''
        #forward propagation through our network
        self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
        self.z2 = self.act(self.z) # activation function
        self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.act(self.z3) # final activation function
        return o
        '''

    def backward(self, y, known, learning_rate):
        error = known - y[-1]
        error_delta = [error * self.act_d(y[-1])]

        # starting from 2nd to last layer
        for i in range(self.num_layers-2, 0, -1):
            error = error_delta[-1].dot(self.weights[i][1:].T)
            error = error*self.act_d(y[i][1:])
            error_delta.append(error)
        # we reverse the list of layer deltas to match the order of our weights
        error_delta.reverse()
        # now we update our weights using the delta from each layer
        for i in range(len(self.weights)):
            layer = y[i].reshape(1, self.architecture[i]+1)
            delta = error_delta[i].reshape(1, self.architecture[i+1])
            self.weights[i] += learning_rate*layer.T.dot(delta)

        # old code
        '''
        # backward propagate through the network
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error*self.act_d(o)  # applying derivative of sigmoid to error

        self.z2_error = self.o_delta@self.W2.T  # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error*self.act_d(self.z2)  # applying derivative of sigmoid to z2 error

        self.W1 += X.T@self.z2_delta  # adjusting first set (input --> hidden) weights
        self.W2 += self.z2.T@self.o_delta  # adjusting second set (hidden --> output) weights
        '''

    def train(self, data, labels, learning_rate=0.1, epochs=10000):
        # add bias to input layer - always on
        ones = np.ones((1, data.shape[0]))
        z = np.concatenate((ones.T, data), axis=1)
        for k in range(epochs):
            if (k+1) % 10000 == 0:
                print('epochs: {}'.format(k+1))

            sample = np.random.randint(X.shape[0])
            # feed data forward through our network
            x = [z[sample]]
            y = self.forward(x)

            known = labels[sample]
            self.backward(y, known, learning_rate)

        # old code
        '''
        o = self.forward(X)
        self.backward(X, y, o)
        return self.o_error
        '''

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

    def predict(self, x):
        result = np.concatenate((np.ones(1).T, np.array(x)))
        for i in range(0, len(self.weights)):
            result = self.act(np.dot(result, self.weights[i]))
            result = np.concatenate((np.ones(1).T, np.array(result)))
        return result[1]

        # old code
        '''
        print("Predicted data based on trained weights, 5000 training iterations: ")
        print("Input: \n" + str(X))
        print("Output: \n" + str(self.forward(X)))
        '''

np.random.seed(0)

NN = NeuralNet([2, 2, 1], "relu")
NN.train(X, Y, learning_rate=0.1, epochs=350)

print("Final prediction")
for s in X:
    print(s, NN.predict(s))