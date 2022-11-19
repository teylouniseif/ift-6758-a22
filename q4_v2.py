import pandas as pd
import numpy as np

def get_info_last_event(current_event :pd.DataFrame,last_event:pd.DataFrame):
    last_event_type =last_event['result.event'].values[0]
    
    rebond = (last_event_type == "Goal" or last_event_type == "Shot")
    
    xCoord_lastEvent =last_event['coordinates.x'].values[0]

    yCoord_lastEvent =last_event['coordinates.y'].values[0]



    x_current = current_event['coordinates.x']
    y_current = current_event['coordinates.y']

    time_last = get_time_sec(last_event["about.periodTime"].values[0],last_event["about.period"].values[0])
    time_current = get_time_sec(current_event["about.periodTime"],current_event["about.period"])
    sec_from_lastEvent = time_current - time_last
    inter = (time_current,time_last)


    dis_from_lastEvent= np.sqrt((x_current - xCoord_lastEvent) ** 2 + (y_current - yCoord_lastEvent) ** 2)

    
    vitesse = dis_from_lastEvent/sec_from_lastEvent if sec_from_lastEvent!=0 else 0
    
    


    return last_event_type,rebond,xCoord_lastEvent,yCoord_lastEvent,sec_from_lastEvent,dis_from_lastEvent,vitesse,inter


def get_time_sec(periodTime :str,period: int):
    # Computing the time of the game with max value at 60min
    time = periodTime.split(":")
    
    time[0] = int(time[0]) + 20 * (period - 1)
    time[1] = int(int(time[1]) * 100 / 60)
    
    game_mins = float(str(time[0]) + '.' + str(time[1]).zfill(2))

    return game_mins*60


