from operator import index
from hockey_rink import NHLRink
import pandas as pd

def rink_print(x, y):
    rink = NHLRink(x_shift=50, y_shift=21.25, nzone={"length": 50})
    ax = rink.draw()
    rink.scatter(x+50, y+21.25)

def get_coords(df):
    x = df["X_Coordinate"].abs()
    y = df["Y_Coordinate"]

    return x, y

def league_avg_shot_hour(df, print_rink=True):
    avg_shot_hour = df.shape[0]/df["Game_ID"].nunique()

    

    if print_rink:
        x, y = get_coords(df)   
        x_avg = x.sum()/x.shape[0]
        y_avg = y.sum()/x.shape[0]
        print("x:",x_avg, "y:", y_avg)

        rink_print(x_avg, y_avg)

    return avg_shot_hour

def excess_shot_rate_hour(df):
    #Copy only the elements we want
    df = df[["Team_of_Shooter", "Shot_or_Goal", "Game_ID"]].copy()

    #Count how many shots/goals a team has made in the season
    shot_df = df.groupby(["Team_of_Shooter"])["Shot_or_Goal"].count()

    #Count how many game a team has played
    game_df = df[["Team_of_Shooter","Game_ID"]].drop_duplicates().groupby(["Team_of_Shooter"])["Game_ID"].count()

    #Compute the average of shot per game (Multiply by 2 to compensate the 2 teams)
    excess_hour = (shot_df/game_df)*2

    return excess_hour
        