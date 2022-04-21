from keras.utils.np_utils import to_categorical
from matplotlib import pyplot as plt
import numpy as np
import joblib
from sklearn.datasets import fetch_openml
import argparse
import pandas as pd
import seaborn as sn

# GetData ( Storing it in cache to save on time )

def fetchData(NoD: int) -> None:
    memo = joblib.Memory('./tmp')
    fetch_openml_cached = memo.cache(fetch_openml)
    mnist = fetch_openml_cached('mnist_784')
    
    images = np.array(mnist.data, dtype='float64') /255
    expected = to_categorical(mnist.target, dtype=int)
    xTrain = images[:NoD]
    yTrain = expected[:NoD]
    xTest = images[NoD:]
    yTest = expected[NoD:]
    return [xTrain, yTrain, xTest, yTest]

#helper functions

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoidDerivative(x: float) -> float:
    return x * (1 - x)

def costDerivative(x: float, y: float) -> float:
    return x - y

#Network

class Network:
    def __init__(self, hidden_layers: list):
        """
        Creates the network object according to given hidden layers
        """
        #init layers
        self.layers = [784]
        self.layers.extend(hidden_layers)
        self.layers.append(10)
        # init weights, biases
        self.init_weights_and_biases()
    
    def init_weights_and_biases(self) -> None:
        """
        Initializes weights and biases for the network
        """
        weights = []
        biases = []
        
        for layer_nr, neuron_nr in enumerate(self.layers[1:]):
            weights.append(np.random.uniform(-1, 1, (neuron_nr, self.layers[layer_nr])))
            biases.append(np.zeros((neuron_nr, 1)))
        
        self.weights = weights
        self.biases = biases

    def propagate_forward(self, input: list) -> list:
        """
        Get the activations and z_vectors for given input
        """
        activations = [input]
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, input) + b
            input = sigmoid(z)
            activations.append(input)
        return activations
    
    def propagate_backward(self, expected: list, activations: list, learning_rate: float) -> None:
        """
        BackPropagation alghoritm, updates both the weights and biases
        """
        input = activations[0]
        # Reverse the activations, weights and biases to iterate backward
        activations.reverse()
        activations.pop(-1)

        nabla_w = []
        nabla_b = []
        
        for layer_nr, neuron_nr in enumerate(self.layers[1:]):
            nabla_w.append(np.zeros((neuron_nr, self.layers[layer_nr])))
            nabla_b.append(np.zeros((neuron_nr, 1)))

        self.weights.reverse()
        nabla_w.reverse()
        nabla_b.reverse()

        #for last layer
        deltas = [costDerivative(activations[0], expected)]

        if len(activations) > 1: #If any hidden layers
            for index, layer in enumerate(activations[1:]):
                nabla_w[index] -= learning_rate * np.dot(deltas[index], layer.T)
                nabla_b[index] -= learning_rate * deltas[index]
                deltas.append(np.dot(self.weights[index].T, deltas[index]) * sigmoidDerivative(layer))

        nabla_w[-1] += -learning_rate * np.dot(deltas[-1], input.T)
        nabla_b[-1] += -learning_rate * deltas[-1]

        self.weights.reverse()
        nabla_w.reverse()
        nabla_b.reverse()

        return (nabla_w, nabla_b)

    def gradient_descent(self, input: list, output: list, learning_rate: float, epochs: int) -> None:
        """
        Gradient Descent alghoritm, updates weights and biases for every data test object, epochs times
        """
        for _ in range(epochs):
            index = 0
            correctPredictions = 0
            for inputLayer, expected in zip(input, output):
                inputLayer.shape += (1,)
                expected.shape += (1,)
                # Forward Prop
                activations = self.propagate_forward(inputLayer)
                # If correct
                if np.argmax(activations[-1]) == np.argmax(expected):
                    correctPredictions += 1
                # Back Prop
                nabla_w, nabla_b = self.propagate_backward(expected, activations, learning_rate)

                self.weights = [np.add(a, b) for a, b in zip(self.weights, nabla_w)]
                self.biases = [np.add(a, b) for a, b in zip(self.biases, nabla_b)]
                
                if index % 100 == 0:
                    print("Iteration: ", index)
                index += 1
            print(f"Accuracy for {_+1}. epoch: {round(correctPredictions / output.shape[0], 2)}")


    def stochastic_gradient_descent(self, input: list, output: list, test_input: list, test_output: list, learning_rate: float, batch_size: int, epochs: int) -> None:
        """
        Stochastic Gradient Descent alghoritm, updates weights and biases for every batch from testData
        """
        import random
        input.shape += (1,)
        output.shape += (1,)
        
        data = [[x, y] for x, y in zip(input, output)]
        
        test_input.shape += (1,)
        test_output.shape += (1,)
        test_data = [[x, y] for x, y in zip(test_input, test_output)]
        
        xData = []
        yData = []
        for _ in range(epochs):
            xData.append(_)
            random.shuffle(test_data)
            random.shuffle(data)
            batch = data[0:batch_size]
            self.update_batch(batch, learning_rate)
            
            good = 0
            for input, expected in test_data[:100]:
                if np.argmax(self.propagate_forward(input)[-1]) == np.argmax(expected):
                    good += 1
            
            print(f"Epoch: {_+1}: {good} / 100")
            yData.append(good/100)
        
        plt.grid(True, color='gray') 
        plt.plot(xData, yData)
        plt.title("Accuracy in Stochastic Gradient Descent")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        ax = plt.gca()
        ax.set_xlim([0, epochs])
        ax.set_ylim([0, 1])
        plt.show()
            

    def update_batch(self, data: list, learning_rate: float) -> None:
        nabla_w = []
        nabla_b = []
        for layer_nr, neuron_nr in enumerate(self.layers[1:]):
            nabla_w.append(np.zeros((neuron_nr, self.layers[layer_nr])))
            nabla_b.append(np.zeros((neuron_nr, 1)))
        
        for input, expected in data:
            activations = self.propagate_forward(input)
            delta_nabla_w, delta_nabla_b = self.propagate_backward(expected, activations, learning_rate)
            nabla_w = [np.add(a, b) for a, b in zip(nabla_w, delta_nabla_w)]
            nabla_b = [np.add(a, b) for a, b in zip(nabla_b, delta_nabla_b)]
        
        self.weights = [np.add(a, b) for a, b in zip(self.weights, nabla_w)]
        self.biases = [np.add(a, b) for a, b in zip(self.biases, nabla_b)]


def confusion_matrix(preds, ans, file_name):
    data = {'y_Actual':    ans,
            'y_Predicted': preds}
    df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
    confusion_matrix = pd.crosstab(df['y_Predicted'], df['y_Actual'], rownames=['Predicted'], colnames=['Actual'])
    sn.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='g')
    plt.savefig(file_name)
    plt.show()


def main(hiddenLayers: int, numberOfData: int, learning_rate: float, epochs: int, stochastic: int = 0):
    dataset = fetchData(numberOfData)
    hidden_layers = []
    for _ in range(0, hiddenLayers):
        nr = "th"
        if _ == 0:
            nr = "st"
        elif _ == 1:
            nr = "nd"
        elif _ == 2:
            nr = "rd"
        
        print(f"Insert the neurons in {_+1}{nr} hidden layer: ")
        
        x = input()
        hidden_layers.append(int(x))
    
    n = Network(hidden_layers)
    
    if not stochastic:
        n.gradient_descent(dataset[0], dataset[1], learning_rate, epochs)
    else:
        n.stochastic_gradient_descent(dataset[0], dataset[1], dataset[2], dataset[3], learning_rate, stochastic, epochs)
        for_matrix = [[x, y] for x, y in zip(dataset[0], dataset[1])]
        predictions = []
        actuals = []
        for inp, output in for_matrix[:10000]:
            predicted = np.argmax(n.propagate_forward(inp)[-1])
            actual = np.argmax(output)
            predictions.append(predicted)
            actuals.append(actual)
        confusion_matrix(predictions, actuals, "hi")

    input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-HL', '--HiddenLayers', type=int, required=True, help='number of Hidden Layers')
    parser.add_argument('-NoD', '--NumberOfData', type=int, required=True, help='number of Data in learning dataset')
    parser.add_argument('-LearningRate', '--LearningRate', type=float, required=True, help='Learning rate parameter')
    parser.add_argument('-Epochs', '--Epochs', type=int, required=True, help='Nr Of epochs parameter')
    parser.add_argument('-Bsize', '--Stochastic', type=int, required=False, help='Stochastic Gradient Descent Batch Size')
    args = parser.parse_args()
    main(args.HiddenLayers, args.NumberOfData, args.LearningRate, args.Epochs, args.Stochastic)
