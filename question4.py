import os
import json
from milestone1.question4 import *
from datetime import timedelta, datetime

def add_power_play(df, path):
    df["pwplay_RemainingTime"] = [0]*df.shape[0]
    df["pwplay_fplayer"] = [5]*df.shape[0]
    df["pwplay_eplayer"] = [5]*df.shape[0]
    for pos_json in os.listdir(os.path.dirname(os.path.abspath(__file__))+"\\"+path.replace("/", "\\" )):
        with open(os.path.dirname(os.path.abspath(__file__))+"\\"+path.replace("/", "\\" )+'\\'+pos_json, 'r') as j:
            contents = json.loads(j.read())
        #Checks whether the game has been recorded
        if "message" in contents:
            print("Game not available")
            return
        else:
            for event in contents["liveData"]['plays']['allPlays']:
                if event["result"]["event"] == "Penalty":
                    time_start = datetime.strptime(event["about"]["periodTime"], '%M:%S')
                    time_period = event["result"]["penaltyMinutes"]
                    time_end = time_start + timedelta(minutes=int(time_period))
                    id = int(pos_json[:-5])
                    nperiod = event["about"]["ordinalNum"][0]
                    if nperiod == "O":
                        continue
                    nperiod = int(nperiod)

                    for idx, row in df.iterrows():
                        if row["Game_ID"]==id:
                            if row["Period_Number"] == nperiod:
                                current_time = datetime.strptime(row["Period_Time"], '%M:%S')
                                if (max((time_start,current_time)) == current_time and min((current_time, time_end)) == current_time):
                                    remaining_time = str(datetime.strptime(row["Period_Time"], '%M:%S') - time_start)
                                    df.at[idx, "pwplay_RemainingTime"] = remaining_time[2:]
                                    df.at[idx, "pwplay_fplayer"] -= 1  
    return df
