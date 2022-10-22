import pandas as pd
import json
import tqdm
import os
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns
from question4 import *
import matplotlib.colors as mcolors

#The function create_full_df can now create a DF with all files in a directory


def plot_shots_as_bubble_chart(shots: pd.Series, goals: pd.Series)->pd.DataFrame:
    """
    Function that takes a directory of json game files, iterates through all of them to create a pd.Dataframe
    where each event of every match of every season in te directory represent one row.
    Only the events of type "Shot" and "Goal" are added to the dataframe
    """

    # Make some labels.
    labels = goals.tolist()
    labels = [round(l, 1) for l in labels]
    """ax = plt.subplot(projection='polar')
    rects = ax.patches
    width=0.5
    ax.bar(goals.index, shots, width, label='Shots')
    plt.gca().legend(('Shots','Goal %'))
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        width = rect.get_x() + rect.get_width() / 2
        ax.annotate(
            label,                      # Use `label` as label
            (width, height),         # Place label at end of the bar
            xytext=(0, 1),              # Vertically shift label by 1
            color='red',
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va='bottom')                # Vertically align label differently for
                                        # positive and negative values.
    ax.barh(shots.index.values, np.radians(goals.tolist()),
    color = plt.rcParams['axes.prop_cycle'].by_key()['color'])
    ax.set_ylabel('Scores')
    ax.set_title('Shots and Goals per type')
    ax.legend()

    plt.show()"""
    sns.set(rc = {'figure.figsize':(15,8)})
    data = pd.DataFrame({'shots':shots.values, 'goals %':goals.values, 'Shot type': shots.index})
    # use the scatterplot function
    sns.scatterplot(data=data, x="Shot type", y="shots", size="goals %", palette="viridis", edgecolors="black", alpha=0.5, sizes=(10, 1000))
        # Add titles (main and on axis)
    plt.ylabel("Number of shots")
    plt.show()

def plot_shot_placements_as_bubble_chart(shots: pd.Series, goals: pd.Series)->pd.DataFrame:

    # Make some labels.
    labels = goals.tolist()
    labels = [round(l, 1) for l in labels]
    sns.set(rc = {'figure.figsize':(15,8)})
    goals = goals.reset_index()
    goals.rename({0:'goal_percent'},axis='columns',inplace=True)

    print(goals.columns.values)
    print(goals)
    data = pd.DataFrame({'range':goals.range*5, 'goals %':goals.goal_percent, 'Shot type': goals.Shot_Type})
    # use the scatterplot function
    sns.scatterplot(data=data, x="range", y="goals %", hue="Shot type", cmap="viridis", edgecolors="black", alpha=0.5, sizes=(10, 1000))
        # Add titles (main and on axis)
    plt.ylabel("Goal %")
    plt.xlabel("Distance from the net (in feet)")
    plt.show()

def aggregate_over_shot_types(df: pd.DataFrame, include_range=False)->(pd.Series, pd.Series):
    groups=['Shot_Type']
    level = [0]
    if include_range:
         groups.append('range')
         level = [0, 1]
    shots = df.groupby(groups).size()
    goals = df[df['Shot_or_Goal']=='Goal'].groupby(groups).size().groupby(level=level).max()
    no_goal_shots = shots[~shots.index.isin(goals.index)]
    no_goal_shots.iloc[:] = 0
    goals = pd.concat([goals, no_goal_shots])
    shots = shots.sort_values(ascending=True)
    goals = goals.reindex(shots.index.values)
    goals = goals.divide(shots)*100
    return (shots, goals)

def split_DF_by_Distances(df: pd.DataFrame):
    metaDF = []
    df['range'] = df['Distance'] // 5
    df = df[~df['range'].isna()]
    df['range'] = df['range'].astype(int)
    return df

def get_Chances_Goal(df: pd.DataFrame):
    chances = []
    for i in range(40):
        count = 0
        for event in df.iterrows():
            if event[1][5]=="Goal" and event[1][15] == i:
                count += 1
        print(df[df['range']==i].shape[0])
        try:
            chances.append(count/df[df['range']==i].shape[0])
        except Exception as e:
            chances.append(0.0)
    return(chances)

if __name__ == "__main__":
    directory = r'data_saved'
    df = create_full_df(directory=directory)
    splitDF = split_DF_by_Distances(df)
    #get_Chances_Goal(splitDF)
    splitDF = aggregate_over_shot_types(splitDF)
