import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from testDT import DecisionTreeClassifier

# load the data and preprocess it
df = pd.read_csv('car.data', names=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class'])
df['buying'] = df['buying'].map({'vhigh': 4, 'high': 3, 'med': 2, 'low': 1})
df['maint'] = df['maint'].map({'vhigh': 4, 'high': 3, 'med': 2, 'low': 1})
df['doors'] = df['doors'].map({'2': 1, '3': 2, '4': 3, '5more': 4})
df['persons'] = df['persons'].map({'2': 1, '4': 2, 'more': 3})
df['lug_boot'] = df['lug_boot'].map({'small': 1, 'med': 2, 'big': 3})
df['safety'] = df['safety'].map({'low': 1, 'med': 2, 'high': 3})
df['class'] = df['class'].map({'unacc': 1, 'acc': 2, 'good': 3, 'vgood': 4})

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values.reshape(-1,1)

# split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# initialize the decision tree classifier
dt = DecisionTreeClassifier(min_samples_split=2, max_depth=5)

# build the tree
dataset = np.concatenate((X_train, y_train), axis=1)
dt.root = dt.build_tree(dataset)

# make predictions on the test data
y_pred = dt.predict(X_test)

# calculate and print the accuracy score
accuracy = accuracy_score(y_test, y_pred)

# plot accuracy over number of predictions
accuracies = []
num_correct = 0

for i in range(len(y_pred)):
    if y_pred[i] == y_test[i]:
        num_correct += 1
    accuracies.append(num_correct / (i + 1))

plt.plot(range(1, len(y_pred) + 1), accuracies)
plt.title("Accuracy over Number of Predictions, test sample's accuracy = {:.2f}%".format(accuracy * 100))
plt.xlabel("Number of Predictions")
plt.ylabel("Accuracy")
plt.legend(["Accuracy"], loc='upper right')
plt.show()
