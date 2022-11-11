import pandas as pd
import json
import tqdm
import os
import numpy as np
import math

#The function create_full_df can now create a DF with all files in a directory



def create_full_df(directory: str)->pd.DataFrame:
    """
    Function that takes a directory of json game files, iterates through all of them to create a pd.Dataframe
    where each event of every match of every season in te directory represent one row.
    The function is recursive: If there is a directory inside the directory originally called, the function will call
    itself on the sub-directory
    Only the events of type "Shot" and "Goal" are added to the dataframe
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, directory)
    dfs = []
    for fileName in os.listdir(directory):
        f = os.path.join(directory, fileName)
        if os.path.isfile(f):
            dfs.append(get_df_from_game(f))
        if os.path.isdir(f):
            dfs.append(create_full_df(f))
    df_merged = pd.concat(dfs, ignore_index=True)
    return df_merged

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
        home = data['gameData']['teams']['home']['triCode']
        away = data['gameData']['teams']['away']['triCode']
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
        distances = []
        angles = []
        est_un_buts = []
        filet_vides = []

        for (i, ex) in (rawDF.iterrows()):
            #Making sure the shooter and goalie name are accessed properly and that any "assist" is ignored
            for i in range(len(ex['players'])):
                if (ex['players'][i]["playerType"] == "Shooter" or ex['players'][i]["playerType"] == "Scorer"):
                    shooters.append(ex['players'][i]["player"]["fullName"])
            goalie = ""
            goalieSide = ""
            for i in range(len(ex['players'])):
                if (ex['players'][i]["playerType"] == "Goalie"):
                    goalie = ex['players'][i]["player"]["fullName"]
                    goalies.append(goalie)
            if goalie == "":
                goalies.append("None")
            if ex["team.triCode"]==home:
                try:
                    goalieSide = data["liveData"]["linescore"]["periods"][ex["about.period"]+1]["away"]["rinkSide"]
                except:
                    pass
            elif ex["team.triCode"]==away:
                try:
                    goalieSide = data["liveData"]["linescore"]["periods"][ex["about.period"] + 1]["home"]["rinkSide"]
                except:
                    pass
            dis,angle = get_distance_angle(ex['coordinates.x'], ex['coordinates.y'], goalieSide)
            distances.append(dis)
            angles.append(angle)
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
            est_un_but = 1 if ex["result.event"] == 'Goal' else 0
            est_un_buts.append(est_un_but)
            is_empty_net = 1 if ex["result.emptyNet"] and not math.isnan(ex["result.emptyNet"]) else 0           
            filet_vides.append(is_empty_net)
            shotType.append(ex["result.secondaryType"])
            teamsShot.append(ex["team.triCode"])
            try:
                emptyNet.append(ex["result.emptyNet"])
            except Exception as e:
                emptyNet.append("NaN")
            goalStrength.append(ex["result.strength.name"])
            xCoord.append(ex['coordinates.x'])
            yCoord.append(ex['coordinates.y'])
        gameDF = pd.DataFrame(gameIDs, columns= ["Game_ID"])
        gameDF = gameDF.assign(Event_ID=eventID, Period_Number=periodNum, Period_Time=periodTime, Game_Time=gameTime,
                                   Shot_or_Goal=shotGoal, Shot_Type=shotType, Shooter=shooters, Team_of_Shooter=teamsShot,
                                   Goalie=goalies, Empty_Net=emptyNet, Goal_Strength=goalStrength, X_Coordinate=xCoord,
                                   Y_Coordinate=yCoord, Distance=distances, Angle = angles , Est_un_but = est_un_buts, Filet_vide = filet_vides)
    except Exception as e:
        pass
    return gameDF

def get_distance(XCoord: int, YCoord: int, goalSide: str) -> object:
    distance = -1
    if goalSide == "":
        distance = min(get_distance(XCoord, YCoord, "left"),get_distance(XCoord, YCoord, "right"))
    elif goalSide == "left":
        distance = np.sqrt((XCoord+90)**2+(YCoord)**2)
    elif goalSide == "right":
        distance = np.sqrt((XCoord-90)**2+(YCoord)**2)
    return distance

"""
fonction ajouter par Hanrui:
une fonction qui calculer le distance et le angle d'un tir/but,
la calculation des distance se base sur le methode get_distance
"""
def get_distance_angle(XCoord: int, YCoord: int, goalSide: str) -> object:
    distance = -1
    angle = 0
    dis_horizontale = 0
    if goalSide == "":
        distance_left,angle_left = get_distance_angle(XCoord, YCoord, "left")
        distance_right,angle_right = get_distance_angle(XCoord, YCoord, "right")
        distance = min(distance_left,distance_right)
        angle = angle_left if distance == distance_left else angle_right
    elif goalSide == "left":
        dis_horizontale = 90 + XCoord        
        distance = np.sqrt((dis_horizontale)**2+(YCoord)**2)

        #Cela représente un tir à l'avant du filet.
        if YCoord == 0:
            angle = 0
        #L'angle entre le joueur et le filet est de 90 degrés, ce qui signifie que le joueur tire du côté du filet et qu'il est presque impossible de marquer.
        elif dis_horizontale==0:
            angle = 90
        else:
            angle = math.degrees(math.acos((YCoord**2-dis_horizontale**2-distance**2)/(-2*np.abs(dis_horizontale)*distance)))
        if YCoord<0:
            angle = -angle
    elif goalSide == "right":
        dis_horizontale = 90 - XCoord    
        distance = np.sqrt((dis_horizontale)**2+(YCoord)**2)  
        #Cela représente un tir à l'avant du filet.     
        if YCoord == 0:
            angle = 0
         #L'angle entre le joueur et le filet est de 90 degrés, ce qui signifie que le joueur tire du côté du filet et qu'il est presque impossible de marquer.
        elif dis_horizontale==0:
            angle = 90
        else:
            angle = math.degrees(math.acos((YCoord**2-dis_horizontale**2-distance**2)/(-2*np.abs(dis_horizontale)*distance)))
        if YCoord>0:
            angle = -angle
   
    return distance,angle
    
    

if __name__ == "__main__":
        #df = get_df_from_game(r"C:\Users\raph_\PycharmProjects\DS-GroupProject\data_saved\play_by_play\2017\regular\2017020462.json")
        #with pd.option_context('display.max_rows', None,
#                               'display.max_columns', None,
#                               'display.precision', 3,
#                               ):
    directory = r'data_saved'
    df = create_full_df(directory=directory)
    print(df)

