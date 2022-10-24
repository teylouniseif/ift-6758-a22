
from cmath import nan
import random
import pandas as pd
import numpy as np
from question1 import get_play_by_play
class DataCleaner:

    def __init__(self):
      pass

    def get_clean_data(self, data_dirty : dict) -> pd.DataFrame:
        """
        A method to extract shot and goal events from the raw data (json) and store them in a dataframe
        """

        df_shot_goal = pd.DataFrame(columns=('periodTime', 'eventTypeId', 'team' , 'indicator_shotOrgoal', 'coordinate_x' , 'coordinate_y',
        'shooter', 'goalie', 'iSemptyNet', 'strength'))

        #All events are in the module "all play" of the original data 
        allplays = data_dirty["liveData"]["plays"]["allPlays"]

        count = 0 
   
        for i in range(len(allplays)):        
            if(allplays[i]["result"]["event"] == "Shot"):
                df_shot_goal.loc[count] = [ 
                    allplays[i]["about"]["periodTime"],
                    allplays[i]["result"]["eventTypeId"],
                    allplays[i]["team"]["name"],
                    allplays[i]["result"]["event"],
                    allplays[i]["coordinates"]["x"],    
                    allplays[i]["coordinates"]["y"],    
                    self.getShooter(allplays[i]["players"]), 
                    self.getGoalie(allplays[i]["players"]), 
                    None,
                    None
                 ]
                count = count+1


            elif(allplays[i]["result"]["event"] == "Goal"):
                df_shot_goal.loc[count] = [ 
                    allplays[i]["about"]["periodTime"],
                    allplays[i]["result"]["eventTypeId"],
                    allplays[i]["team"]["name"],
                    allplays[i]["result"]["event"],
                    allplays[i]["coordinates"]["x"],    
                    allplays[i]["coordinates"]["y"],    
                    self.getShooter(allplays[i]["players"]), 
                    self.getGoalie(allplays[i]["players"]),
                    allplays[i]["result"]["emptyNet"],  
                    allplays[i]["result"]["strength"]["name"]  
                 ]
                count = count+1
             

        return df_shot_goal


    def getShooter(self,players):
        for i in range(len(players)):
            if(players[i]["playerType"]=="Shooter" or players[i]["playerType"]=="Scorer"):
                return players[i]["player"]["fullName"]
        return None

    def getGoalie(self, players):
        for i in range(len(players)):
            if(players[i]["playerType"]=="Goalie"):
                return players[i]["player"]["fullName"]
        return None

   






if __name__ == "__main__":
    play_by_play = get_play_by_play("2017020001","data_saved/play_by_play/2017/regular")
    dataCleaner  = DataCleaner()
    print(dataCleaner.get_clean_data(play_by_play))

   
