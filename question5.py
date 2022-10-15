import pandas as pd
import json
import tqdm
import os
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns

#The function create_full_df can now create a DF with all files in a directory


def plot_shots_as_stacked_bars(shots: pd.Series, goals: pd.Series)->pd.DataFrame:
    """
    Function that takes a directory of json game files, iterates through all of them to create a pd.Dataframe
    where each event of every match of every season in te directory represent one row.
    Only the events of type "Shot" and "Goal" are added to the dataframe
    """

    
    shots = shots.sort_values(ascending=True)
    goals = goals.reindex(shots.index.values)
    goals = goals.divide(shots)*100
    print(goals.index.values)
    print(goals.tolist())
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


def aggregate_over_shot_types(df: pd.DataFrame)->(pd.Series, pd.Series):
    shots = df.groupby(['Shot_Type']).size()
    goals = df[df['Shot_or_Goal']=='Goal'].groupby(['Shot_Type']).size().groupby(level=0).max()
    no_goal_shots = shots[~shots.index.isin(goals.index)]
    no_goal_shots.iloc[:] = 0
    goals = pd.concat([goals, no_goal_shots])
    print('hello')
    print(no_goal_shots)
    print(shots)
    print(goals)
    return (shots, goals)