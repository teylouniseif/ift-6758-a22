import pandas as pd
import json
import tqdm


#ONLY DOING ONE GAME FOR NOW, BUT SEEMS TO BE WORKING WELL -RAPH


filePath = r"C:\Users\raph_\PycharmProjects\DS-GroupProject\data_saved\play_by_play\2017\regular\2017020017.json"
def get_df_from_game(filePath: str)->pd.DataFrame:
    """
    Function that takes a parameter filePath that corresponds to a json file with all the events of a hockey game
    The function then turns that json file into a pd.Dataframe with only the desired information about the game
    """
    gameDF = pd.DataFrame()
    try:
        with open(filePath,'r') as f:
             data = json.loads(f.read())
        gameID = data['gamePk']
        rawDF = pd.json_normalize(data['liveData']['plays']['allPlays'])
        rawDF = rawDF[rawDF['result.event'].isin(["Goal","Shot"])]
        gameIDs = [gameID]*len(rawDF)
        eventID = []
        periodNum = []
        periodTime= []
        gameTime = []
        shotGoal = []
        shotType= []
        shooters = []
        teamsShot = []
        goalies = []
        emptyNet = []
        goalStrength = []
        xCoord = []
        yCoord = []

        for (i, ex) in (rawDF.iterrows()):
            #Making sure the shooter and goalie name are accessed properly and that any "assist" is ignored
            shooter = ex['players'][0]['player']['fullName']
            if ex['players'][1]["playerType"]!="Assist":
                goalie = ex['players'][1]['player']['fullName']
            elif ex['players'][2]["playerType"]=="Goalie":
                goalie = ex['players'][2]['player']['fullName']
            else:
                goalie = "None"
            eventID.append(ex["about.eventIdx"])
            periodNum.append(ex["about.period"])
            periodTime.append(ex["about.periodTime"])
            #Computing the time of the game with max value at 60min
            time = ex["about.periodTime"].split(":")
            if ex["about.period"]<=3:
                time[0] = int(time[0])+20*(ex["about.period"]-1)
                time[1] = int(int(time[1]) * 100 / 60)
            #Assuming the games last no more than 60min
            else:
                time[0] = 60
                time[1] = 00
            gameTime.append(float(str(time[0])+'.'+str(time[1])))
            shotGoal.append(ex["result.event"])
            shotType.append(ex["result.secondaryType"])
            shooters.append(shooter)
            teamsShot.append(ex["team.triCode"])
            goalies.append(goalie)
            emptyNet.append(ex["result.emptyNet"])
            goalStrength.append(ex["result.strength.name"])
            xCoord.append(ex['coordinates.x'])
            yCoord.append(ex['coordinates.y'])
        gameDF = pd.DataFrame(gameIDs, columns= ["Game_ID"])
        gameDF = gameDF.assign(Event_ID=eventID, Period_Number=periodNum, Period_Time=periodTime, Game_Time=gameTime,
                               Shot_or_Goal=shotGoal, Shot_Type=shotType, Shooter=shooters, Team_of_Shooter=teamsShot,
                               Goalie=goalies, Empty_Net=emptyNet, Goal_Strength=goalStrength, X_Coordinate=xCoord,
                               Y_Coordinate=yCoord)
    except Exception as e:
        print(e)
    return gameDF

if __name__ == "__main__":
    df = get_df_from_game(filePath)
    print(df)

