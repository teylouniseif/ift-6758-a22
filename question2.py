import json
from os.path import exists
import os
import matplotlib.pyplot as plt
from hockey_rink import NHLRink

def match_info(s, t, n, e):
  if t[0] == "Saison régulière":
    t = 2
  elif t[0] == "Séries éliminatoires":
    t = 3
  id = str(s)+str(t).zfill(2)+str(n).zfill(4)
  with open(os.path.dirname(os.path.abspath(__file__))+"/data/"+str(s)+"/"+id, 'r') as j:
     contents = json.loads(j.read())
  if "message" in contents:
    print("Game not available")
    return
  else:

    print(contents["gameData"]['datetime']['dateTime'])
    
    print("Game ID :", n+";", contents["gameData"]["teams"]["home"]["abbreviation"],
    "(home) vs", contents["gameData"]["teams"]["away"]["abbreviation"], "(away)")

    print("       ", "Home  ", "Away")
    print()
    home = contents["liveData"]["boxscore"]["teams"]["home"]
    away = contents["liveData"]["boxscore"]["teams"]["away"]

    table = {"Teams:":[contents["gameData"]["teams"]["home"]["abbreviation"], 
    contents["gameData"]["teams"]["away"]["abbreviation"]],
    "Goals:":[home["teamStats"]["teamSkaterStats"]["goals"], 
    away["teamStats"]["teamSkaterStats"]["goals"]],
    "SoG:":[home["shotsOnGoal"],
    away["shotsOnGoal"]]}
    for k, v in table.items():
      home, away = v
      print(k, home, away)
    
    e = int(e)

    print("Event n°", e, "over", contents["liveData"]["plays"]["currentPlay"]["about"]["eventIdx"])
    play = contents["liveData"]["plays"]["allPlays"][e]
    print(play["result"]["description"])
    print(play["about"]["periodTime"])

    rink = NHLRink(x_shift=100, y_shift=42.5, nzone={"length": 50})
    ax = rink.draw()
    if play["coordinates"]!={} and play["coordinates"]!={}:
      rink.scatter(play["coordinates"]["x"], play["coordinates"]["y"])
    
    return 