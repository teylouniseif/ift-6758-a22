import json
from os.path import exists
import os

def match_info(s, t, n):
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
    print("OT")
    print("       ", "Home  ", "Away")
    print()
    table = {"Teams:":[contents["gameData"]["teams"]["home"]["abbreviation"], 
    contents["gameData"]["teams"]["away"]["abbreviation"]],
    "Goals:":[contents["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["goals"], 
    contents["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["goals"]],
    "SoG:":[contents["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["shots"],
    contents["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["shots"]],
    "SO Goals:":[contents["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["shots"],
    contents["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["shots"]],
    "SO Attempts:":[contents["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["shots"],
    contents["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["shots"]]}
    for k, v in table.items():
      home, away = v
      print(k, home, away)
    return 