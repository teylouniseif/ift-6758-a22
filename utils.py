import os
import pandas as pd
import numpy as np
from etape2_Q3 import *
from matplotlib.gridspec import GridSpec
from sklearn.calibration import CalibrationDisplay

def get_current_dir():
    return os.path.dirname(os.path.abspath(__file__))

def replace_nans(df):
    for c in df.columns.values:
        if pd.api.types.is_categorical_dtype(df[c]):
            print(df[c].mode())
            print(c)
            df[c]=df[c].fillna(df[c].mode())
        elif pd.api.types.is_numeric_dtype(df[c]):
            df[c]=df[c].fillna(df[c].mean())
        elif  pd.api.types.is_string_dtype(df[c]):
            df[c]=df[c].fillna("")
    return df


def replace_infs(df):
    for c in df.columns.values:
        if pd.api.types.is_categorical_dtype(df[c]):
            print(df[c].mode())
            print(c)
            df[c]=df[c].replace([np.inf], df[c].mode())
            df[c]=df[c].replace([-np.inf], df[c].mode())
        elif pd.api.types.is_numeric_dtype(df[c]):
            df[c]=df[c].replace([np.inf], df[c].mean())
            df[c]=df[c].replace([-np.inf], df[c].mean())
        elif  pd.api.types.is_string_dtype(df[c]):
            df[c]=df[c].fillna("")
    return df


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

def grid_search(X, Y, model):
    p = {
            'min_child_weight': [1, 5, 8, 10, 12, 15],
            'gamma': [0.5, 1, 1.5, 2, 5, 8],
            'subsample': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'max_depth': [3, 4, 5, 6, 7, 8],
            'tree_method':['approx', 'hist']
            }

    folds = 3
    param_comb = 6

    skf = StratifiedKFold(n_splits=folds, shuffle = True, random_state = 10)

    random_search = RandomizedSearchCV(model, param_distributions=p, n_iter=param_comb, scoring='roc_auc', n_jobs=4, cv=skf.split(X,Y), verbose=3, random_state=10 )
    random_search.fit(X,Y)
    return random_search.best_params_


#ytest = y_test['Est_un_but']

def create_plots(X_test, ytest, y_pred, scenario_title, experiment):

    lw = 2
    fpr_d, tpr_d, roc_auc_d = get_roc_data(ytest, y_pred)
    fig = plt.figure()
    line = plt.plot(fpr_d,tpr_d,color="red",lw=lw,alpha=0.5,label=f"ROC curve {scenario_title} (area = %0.2f)" % roc_auc_d)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver operating characteristic example")
    plt.legend(loc="lower right")
    plt.show()
    
    experiment.log_figure(figure=fig)
    experiment.log_metric('roc', roc_auc_d)

    perc_d, perc_values_d, num_goals_d = get_percentile_goal_chance(y_pred, ytest)
    goal_rate_d = [i*100 for i in perc_values_d]
    fig = plt.figure()
    line = plt.plot(perc_d,goal_rate_d,color="red",alpha=0.5,lw=lw,label=f"{scenario_title}")
    plt.xlim([100, 0])
    #plt.ylim([0, 100])
    plt.xlabel("Shot probability model percentile")
    plt.ylabel("Goals/(Shots+Goals)")
    plt.title("Goal Rate")
    plt.legend(loc="upper right")
    plt.show()
    
    experiment.log_figure(figure=fig)
    
    
    cum_values_d = np.cumsum(num_goals_d)
    sum = np.sum(num_goals_d)/100
    cum_values_d = [i/sum for i in cum_values_d]
    cum_values_d = cum_values_d[::-1]
    fig = plt.figure()
    line = plt.plot(perc_d,cum_values_d,color="red",alpha=0.5,lw=lw,label=f"{scenario_title}")
    plt.xlim([-5, 105])
    plt.ylim([0, 105])
    plt.xlabel("Shot probability model percentile")
    plt.ylabel("Proportion (%)")
    plt.title("Cumulative % of goals")
    plt.legend(loc="lower right")
    plt.show()
    
    experiment.log_figure(figure=fig)

    X_val_d = np.array(X_test)
    X_val_d = X_val_d.reshape(-1, 1)
    fig = plt.figure(figsize=(10,10))
    ax_calibration_curve = fig.add_subplot(GridSpec(4,2)[:2,:2])
    disp = CalibrationDisplay.from_predictions(ytest, y_pred, color="red", name=f"{scenario_title}", alpha=0.5, ax=ax_calibration_curve, n_bins=10)
    
    experiment.log_figure(figure=fig)
