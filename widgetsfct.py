import json
from os.path import exists

def match_info(s, t, n):
  print(t[0])
  if t[0] == "Saison régulière":
    t = 2
  elif t[0] == "Séries éliminatoires":
    t = 3
  id = str(s)+str(t).zfill(2)+str(n).zfill(4)
  print("data"+"/"+str(s)+"/"+id)
  #/content/data/2016/2016010000.json
  file = (json.loads("data"+"/"+str(s)+"/"+id+".json"))
  print(file)
  """if "message" in file:
    print("Game not available")
    quit()
  else:
    print(file["datetime"])
    return file["datetime"]"""