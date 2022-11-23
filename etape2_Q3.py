from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Creates a logistic regression instance, trains it on the provided training set et labels and returns the prediction (score) and probability
#Of every test point, as well as the logistic regression instance
def logistic_regression(X_train, y_train, X_test: np.array):
    clf = LogisticRegression()
    try:
        dim = len(X_train.axes[1])
    except:
        X_test = np.array(X_test)
        X_train = np.array(X_train)
        X_test = X_test.reshape(-1, 1)
        X_train = X_train.reshape(-1, 1)
    clf.fit(X_train,y_train)
    y_score = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)
    return y_score, y_prob, clf

#For an array of probability (y_prob) and the corresponding labels (y_test), returns the fpr, tpr and auc
def get_roc_data(y_test, y_prob: np.array):
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, roc_auc

#For an array of probability (y_prob) and the corresponding labels (y_test), assigns a probability for every percentile (fromm 100 to 0 in that order)
#and returns an array with the percentile (perc), an array with the values of each percentile (perc_values) and the number of goals scored in each percentile
def get_percentile_goal_chance(y_prob, y_test: np.array):
    perc = range(1,101)
    perc = np.array(perc)
    perc = np.sort(perc)[::-1]
    perc_values = []
    num_goals = []
    for i in perc:
        perc_values.append(np.percentile(y_prob, i))
    for i in range(100):
        count = 0
        for j, ex in enumerate(y_test):
            if i == 99:
                if y_prob[j] < perc_values[i]:
                    if ex == 1:
                        count += 1
            else:
                if (y_prob[j] > perc_values[i + 1]) and (y_prob[j] <= perc_values[i]):
                    if ex == 1:
                        count += 1
        num_goals.append(count)

    return perc, perc_values, num_goals


if __name__ == "__main__":
    pass