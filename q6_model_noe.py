import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np


class SVM:
    def __init__(self, df):
        self.raw_df = df
        self.df = self.preprocess(df)
        
    
    def preprocess(self, df):
        df = df.sample(frac=1).reset_index(drop=True).dropna(axis = 1)
        df = df.head(int(df.shape[0]*0.20))

        X = df[["Filet_vide","Last_event_type","Rebond"]]
        y = df["Est_un_but"]

        last_type = pd.get_dummies(X.Last_event_type)
        X = X.drop(["Last_event_type"], axis = 1)
        X = X.join(pd.DataFrame(last_type))
        X["Rebond"] *=1

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.10, random_state=42)
        return df
    
    def train(self):
        clf = SVC(probability=True)
        clf.fit(self.X_train, self.y_train)
        self.svm = clf
        return clf
    
    def predict(self):
        self.y_test_pred = self.svm.predict(self.X_test)
        return self.y_test_pred

    def roc_auc_curve(self):
        self.y_train_pred_proba = self.svm.decision_function(self.X_train)
        self.y_test_pred_proba = self.svm.decision_function(self.X_test)

        train_fpr, train_tpr, _ = metrics.roc_curve(self.y_train, self.y_train_pred_proba)
        test_fpr, test_tpr, _ = metrics.roc_curve(self.y_test, self.y_test_pred_proba)

        auc_train = metrics.auc(train_fpr, train_tpr)
        auc_test = metrics.auc(test_fpr, test_tpr)

        plt.grid()

        plt.plot(train_fpr, train_tpr, label=" AUC TRAIN ="+str(auc_train))
        plt.plot(test_fpr, test_tpr, label=" AUC TEST ="+str(auc_test))
        plt.plot([0,1],[0,1],'g--')
        plt.legend()
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("AUC(ROC curve)")
        plt.grid(color='black', linestyle='-', linewidth=0.5)
        plt.show()

    def goals_rate_percentile(self):
        goal_rates = list()
        for _ in range(10):
            self.preprocess(self.raw_df)
            self.train()

            y_test_pred = self.predict().tolist()
            goals = y_test_pred.count(1)
            non_goals = y_test_pred.count(0)

            goal_rates.append(goals/(non_goals+goals))

        return np.percentile(goal_rates, 70)