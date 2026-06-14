import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "Iris.csv"

df = pd.read_csv(file)

da = df.to_numpy()[:, 1:]

np.random.shuffle(da)

train = da[:100]
test = da[100:]

x_train = train[:, :4]/10
y_train = train[:, 4].astype("int")


x_test = test[:, :4]/10
y_test = test[:, 4]

print(y_test[:1])

def init_params():
    W1 = np.random.rand(4, 8) * np.sqrt(2 / 4)
    B1 = np.zeros((1,8))

    W2 = np.random.rand(8, 6) * np.sqrt(2 / 8)
    B2 = np.zeros((1,6))

    W3 = np.random.rand(6, 3) * np.sqrt(2 / 6)
    B3 = np.zeros((1,3))

    return W1, B1, W2, B2, W3, B3

def ReLU(Z):
    return np.maximum(0, Z)

def SoftMax(Z):
    exp = np.exp(Z - np.max(Z, keepdims=True, axis=1))
    return exp / np.sum(exp, keepdims=True, axis=1)

def forwardProp(X, W1, B1, W2, B2, W3, B3):
    Z1 = np.dot(X, W1) + B1
    A1 = ReLU(Z1)

    Z2 = np.dot(A1, W2) + B2
    A2 = ReLU(Z2)

    Z3 = np.dot(A2, W3) + B3
    A3 = SoftMax(Z3)

    return Z1, A1, Z2, A2, Z3, A3

def accuracy(A3, Y):
    predictions = np.argmax(A3, axis=1)
    return np.mean(predictions == Y)

def loss(A3, Y):
    m = Y.shape[0]
    return -np.sum(Y * np.log(A3 + 1e-8)) / m

def OneHotEncode(Y):
    return np.eye(3)[Y]

def ReLU_Derivative(Z):
    return (Z>0).astype("float")

def backProp(X, Y, W2, W3, Z1, A1, Z2, A2, A3):
    m = Y.shape[0]
    dZ3 = A3-Y
    dW3 = (1/m) * np.dot(A2.T, dZ3)
    dB3 = (1/m) * np.sum(dZ3,axis=0, keepdims=True)
    dA2 = np.dot(dZ3, W3.T)
    dZ2 = dA2 * ReLU_Derivative(Z2)
    dW2 = (1/m) * np.dot(A1.T, dZ2)
    dB2 = (1/m) * np.sum(dZ2,axis=0, keepdims=True)
    dA1 = np.dot(dZ2, W2.T)
    dZ1 = dA1 * ReLU_Derivative(Z1)
    dW1 = (1/m) * np.dot(X.T, dZ1)
    dB1 = (1/m) * np.sum(dZ1,axis=0, keepdims=True)

    return dW1, dB1, dW2, dB2, dW3, dB3

def updateParams(a, W1, B1, W2, B2, W3, B3, dW1, dB1, dW2, dB2, dW3, dB3):
    W1 -= a * dW1
    B1 -= a * dB1
    W2 -= a * dW2
    B2 -= a * dB2
    W3 -= a * dW3
    B3 -= a * dB3

    return W1, B1, W2, B2, W3, B3


Y = OneHotEncode(y_train)

W1,B1,W2,B2,W3,B3 = init_params()

for i in range(10000):

    Z1,A1,Z2,A2,Z3,A3 = forwardProp(
        x_train,W1,B1,W2,B2,W3,B3
    )

    dW1,dB1,dW2,dB2,dW3,dB3 = backProp(
        x_train,Y,W2,W3,
        Z1,A1,Z2,A2,A3
    )

    W1,B1,W2,B2,W3,B3 = updateParams(0.1,
        W1,B1,W2,B2,W3,B3,
        dW1,dB1,dW2,dB2,dW3,dB3
    )

    if i % 100 == 0:
        print(loss(A3, Y), "   ", accuracy(A3, y_train))
_, _, _, _, _, A3_test = forwardProp(
    x_test,
    W1, B1, W2, B2, W3, B3
)

print("Test accuracy:", accuracy(A3_test, y_test))