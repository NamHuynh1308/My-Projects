from testDT import DecisionTreeClassifier
import numpy as np
from collections import Counter

class RandomForest:
    def __init__(self, n_trees, max_depth=5, min_samples_split=2):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []
        
    def build_trees(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
           tree = DecisionTreeClassifier(min_samples_split=2, max_depth=5)
           X_sample, y_sample = self.random_samples(X, y)
           dataset = np.concatenate((X_sample, y_sample), axis=1) 
           tree.root = tree.build_tree(dataset)
           self.trees.append(tree)
           
    def random_samples(self, X, y):
        n_samples = X.shape[0] #number of samples
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def mostCommon(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common
                
    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(predictions, 0, 1)
        predictions = np.array([self.mostCommon(pred) for pred in tree_preds])
        return predictions