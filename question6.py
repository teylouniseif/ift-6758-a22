from hockey_rink import NHLRink

def rink_print(df, game_id):
    df = df.loc[df["Game_ID"]==game_id]
    x = df["X_Coordinate"].abs()
    y = df["Y_Coordinate"]

    rink = NHLRink(x_shift=50, y_shift=21.25, nzone={"length": 50})
    ax = rink.draw()
    rink.scatter(x+50, y+21.25)

def league_avg_shot_hour(df):
    x = df["X_Coordinate"].abs()
    y = df["Y_Coordinate"]
    x_avg = x.sum()/x.shape[0]
    y_avg = y.sum()/x.shape[0]
    print(x_avg, y_avg)

    rink = NHLRink(x_shift=50, y_shift=21.25, nzone={"length": 50})
    ax = rink.draw()
    rink.scatter(x_avg+50, y_avg+21.25)

def excess_shot_rate_hour(df):
    