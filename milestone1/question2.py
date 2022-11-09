import json
from os.path import exists
import os
import matplotlib.pyplot as plt
from hockey_rink import NHLRink

def match_info(s, t, n, e):
  #Convert str to id part
  if t[0] == "Saison régulière":
    t = 2
  elif t[0] == "Séries éliminatoires":
    t = 3

  #Build the ID
  id = str(s)+str(t).zfill(2)+str(n).zfill(4)

  #Converts json file with same id in the corresponding folder into a df
  with open(os.path.dirname(os.path.abspath(__file__))+"/data/"+str(s)+"/"+id, 'r') as j:
     contents = json.loads(j.read())

  #Checks whether the game has been recorded
  if "message" in contents:
    print("Game not available")
    return
  else:
    #Print the date and hour of start of the game
    print(contents["gameData"]['datetime']['dateTime'])
    
    #Prints the Game ID, and the abbreviation of the teams playing
    print("Game ID :", n+";", contents["gameData"]["teams"]["home"]["abbreviation"],
    "(home) vs", contents["gameData"]["teams"]["away"]["abbreviation"], "(away)")

    print("       ", "Home  ", "Away")
    print()
    home = contents["liveData"]["linescore"]["teams"]["home"]
    away = contents["liveData"]["linescore"]["teams"]["away"]

    #Table containing the teams, goals, and the SoG
    table = {"Teams:":[contents["gameData"]["teams"]["home"]["abbreviation"], 
    contents["gameData"]["teams"]["away"]["abbreviation"]],
    "Goals:":[home["goals"], 
    away["goals"]],
    "SoG:":[home["shotsOnGoal"],
    away["shotsOnGoal"]]}
    #Print line by line the table
    for k, v in table.items():
      home, away = v
      print(k, home, away)
    
    e = int(e)
    #Print which events we are currently looking at with a title and the time
    print("Event n°", e, "over", contents["liveData"]["plays"]["currentPlay"]["about"]["eventIdx"])
    play = contents["liveData"]["plays"]["allPlays"][e]
    print(play["result"]["description"])
    print(play["about"]["periodTime"])

    #Print the rink with the coordinates of the event, and its location on the rink
    rink = NHLRink(x_shift=50, y_shift=21.25, nzone={"length": 50})
    ax = rink.draw()
    if play["coordinates"]!={} and play["coordinates"]!={}:
      rink.scatter(play["coordinates"]["x"]+50, play["coordinates"]["y"]+21.25)
    
    return 