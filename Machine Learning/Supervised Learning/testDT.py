import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None): 
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        self.value = value
        
       
class DecisionTreeClassifier():
    # Constructor 
    def __init__(self, min_samples_split, max_depth):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.root = None
        
        
    def build_tree(self, dataset, curr_depth=0):
        X, y = dataset[:, :-1], dataset[:, -1]
        num_samples, num_features = X.shape

        if num_samples < self.min_samples_split or curr_depth >= self.max_depth:
            return Node(value=self.calculate_leaf_value(y))

        best_split = self.get_best_split(dataset, num_samples, num_features)
        if best_split["info_gain"] == 0:
            return Node(value=self.calculate_leaf_value(y))

        left_subtree = self.build_tree(best_split["dataset_left"], curr_depth + 1)
        right_subtree = self.build_tree(best_split["dataset_right"], curr_depth + 1)

        return Node(best_split["feature_index"], best_split["threshold"],
                    left_subtree, right_subtree, best_split["info_gain"])

    def get_best_split(self, dataset, num_samples, num_features):
        best_split = {}
        max_info_gain = -float("inf")

        for feature_index in range(num_features):
            feature_values = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_values)

            for threshold in possible_thresholds:
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                if len(dataset_left) > 0 and len(dataset_right) > 0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    curr_info_gain = self.information_gain(y, left_y, right_y)
                    if curr_info_gain > max_info_gain:
                        best_split = {"feature_index": feature_index,
                                      "threshold": threshold,
                                      "dataset_left": dataset_left,
                                      "dataset_right": dataset_right,
                                      "info_gain": curr_info_gain}
                        max_info_gain = curr_info_gain

        return best_split
    
    def split(self, dataset, feature_index, threshold):
        
        dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])
        return dataset_left, dataset_right
    
    def information_gain(self, parent, l_child, r_child, mode="entropy"):
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        if mode=="gini":
            gain = self.gini_index(parent) - (weight_l*self.gini_index(l_child) + weight_r*self.gini_index(r_child))
        else:
            gain = self.entropy(parent) - (weight_l*self.entropy(l_child) + weight_r*self.entropy(r_child))
        return gain
    
    def entropy(self, y):
        
        proportions = np.bincount(y) / len(y)
        entropy = -np.sum([p * np.log2(p) for p in proportions if p > 0])
        return entropy
    
    def gini_index(self, y):
        
        class_labels = np.unique(y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
        return 1 - gini
    
    def calculate_leaf_value(self, Y):
        
        Y = list(Y)
        return max(Y, key=Y.count)
    
    def predict(self, X, tree=None):
        if tree is None:
            tree = self.root
        predictions = []
        for x in X:
            if tree.value is not None:
                predictions.append(tree.value)
            else:
                feature_val = x[tree.feature_index]
                if feature_val <= tree.threshold:
                    predictions.append(self.predict([x], tree.left)[0])
                else:
                    predictions.append(self.predict([x], tree.right)[0])
        return predictions