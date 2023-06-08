import pandas as pd
import numpy as np
from math import sqrt
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# read in the data from car.data
df = pd.read_csv('car.data', names=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class'])

# define a mapping for each categorical attribute
buying_map = {'vhigh': 4, 'high': 3, 'med': 2, 'low': 1}
maint_map = {'vhigh': 4, 'high': 3, 'med': 2, 'low': 1}
doors_map = {'2': 1, '3': 2, '4': 3, '5more': 4}
persons_map = {'2': 1, '4': 2, 'more': 3}
lug_boot_map = {'small': 1, 'med': 2, 'big': 3}
safety_map = {'low': 1, 'med': 2, 'high': 3}
class_map = {'unacc': 1, 'acc': 2, 'good': 3, 'vgood': 4}

# apply the mapping to the categorical attributes
df['buying'] = df['buying'].map(buying_map)
df['maint'] = df['maint'].map(maint_map)
df['doors'] = df['doors'].map(doors_map)
df['persons'] = df['persons'].map(persons_map)
df['lug_boot'] = df['lug_boot'].map(lug_boot_map)
df['safety'] = df['safety'].map(safety_map)
df['class'] = df['class'].map(class_map)

X = df.iloc[:, :-1]  # select all columns except the last one
values = df.iloc[:, -1]   # select only the last column

#convert dataframe to array
X = X.to_numpy()
values = values.to_numpy()

#weights w1, w2, ... respectively, w0 is bias
w = np.random.rand(7)
#learning rate
alpha = 0.001
#number of iterations
iter = 1500
#keep track for printing out order
c = 0

#split up data for training and testing
train_samples, test_samples, train_values, test_values = train_test_split(X, values, test_size=0.2, random_state=42)

MSE = []
#-----------------------------------------------

with open('LROutput.txt', 'w') as f:
    for k in range (1, iter + 1):
        #delta w
        _w = np.zeros(7) #add bias
        mse = 0
        y_hat = []
        
        for i in range(0, len(train_samples)):
            sum = 0
            
            #make a prediction
            for j in range (1, len(w)): 
                sum += train_samples[i][j-1] * w[j]    
            y = (w[0] + sum) 
            y_hat.append(y)
            
            #MSE
            error = (values[i] - y)**2
            mse += error
            
            #gradient
            for j in range (1, len(w)):
               _w[j] += (y - values[i]) * train_samples[i][j-1]           
            _w[0] += (y - values[i])  #assume x0 = 1
            
        mse = (mse / len(train_samples))
        MSE.append(mse)
    
        partial_w = (1/len(train_samples)) * (2 * _w[1:])
        partial_d = (1/len(train_samples)) * (2 * _w[0])
        
        #update weights
        for i in range (1, len(w)):
            w[i] -= alpha * partial_w[i-1]
        w[0] -= alpha * partial_d
                
    print(w)   
    o = []
    #get predicted values for 1727 data rows
    for a in range (0, len(test_samples)):
        sum = 0
        for b in range (1, len(w)): sum += test_samples[a][b-1] * w[b]
        t = (w[0] + sum) 
        t = round(t, 0)
        o.append(t)
        print(str(t))
        c += 1
        f.write(str(c) + ", " + str(t) + "\n")
    
    
    accuracies = []
    num_correct = 0

    for i in range(len(o)):
        if o[i] == test_values[i]:
            num_correct += 1
        accuracies.append(num_correct / (i + 1))

    plt.plot(range(1, len(o) + 1), accuracies)
    plt.title("Accuracy over Number of Predictions")
    plt.legend(["Accuracy"], loc = 'upper right')
    plt.xlabel("Number of Predictions")
    plt.ylabel("Accuracy")
    plt.show()
    