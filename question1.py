import pandas as pd
import requests
import json
from os.path import exists

def get_player_stats(year: int, player_type: str) -> pd.DataFrame:
    """

    Uses Pandas' built in HTML parser to scrape the tabular player statistics from
    https://www.hockey-reference.com/leagues/ . If the player played on multiple 
    teams in a single season, the individual team's statistics are discarded and
    the total ('TOT') statistics are retained (the multiple team names are discarded)

    Args:
        year (int): The first year of the season to retrieve, i.e. for the 2016-17
            season you'd put in 2016
        player_type (str): Either 'skaters' for forwards and defensemen, or 'goalies'
            for goaltenders.
    """

    if player_type not in ["skaters", "goalies"]:
        raise RuntimeError("'player_type' must be either 'skaters' or 'goalies'")
    
    url = f'https://www.hockey-reference.com/leagues/NHL_{year}_{player_type}.html'

    print(f"Retrieving data from '{url}'...")

    # Use Pandas' built in HTML parser to retrieve the tabular data from the web data
    # Uses BeautifulSoup4 in the background to do the heavylifting
    df = pd.read_html(url, header=1)[0]

    # get players which changed teams during a season
    players_multiple_teams = df[df['Tm'].isin(['TOT'])]

    # filter out players who played on multiple teams
    df = df[~df['Player'].isin(players_multiple_teams['Player'])]
    df = df[df['Player'] != "Player"]

    # add the aggregate rows
    df = df.append(players_multiple_teams, ignore_index=True)

    return df

def get_data_season(year_begin: str, year_end: str, path: str):
    """
    une fonction qui accepte l'année cible et un chemin de fichier comme argument, puis recherche dans le chemin de fichier 
    spécifié un fichier correspondant à l'ensemble de données que vous allez télécharger. 
    S'il existe, il pourrait immédiatement ouvrir le fichier et renvoyer le contenu enregistré. 
    Sinon, il pourrait télécharger le contenu de l'API REST et l'enregistrer dans le fichier avant de renvoyer les données.
    """

    if not exists(path):
        url = "https://statsapi.web.nhl.com/api/v1/seasons"+"/"+year_begin+year_end

        data_seasons = requests.get(url).json()['seasons']
        
        #enregistrer les donnees en format json
        try:
            with open(path,'a',encoding="utf-8") as f:
                f.write(json.dumps(data_seasons,indent=1,ensure_ascii=False)) #si ensure_ascii=False，la valeur retourne peux contient les valuers non ascii
        except IOError as e:
            print(str(e))
        
        finally:
            f.close()

        return data_seasons
    else:
        f_open = open(path, 'r')
        return json.load(f_open)

def get_data_play_by_play(gameID: str, path: str):
    if not exists(path):
        url = "https://statsapi.web.nhl.com/api/v1/game"+"/"+gameID+"/feed/live"

        data_play_by_play = requests.get(url).json()
        
        #enregistrer les donnees en format json
        try:
            with open(path,'a',encoding="utf-8") as f:
                f.write(json.dumps(data_play_by_play,indent=1,ensure_ascii=False)) #si ensure_ascii=False，la valeur retourne peux contient les valuers non ascii
        except IOError as e:
            print(str(e))
        
        finally:
            f.close()

        return data_play_by_play
    else:
        f_open = open(path, 'r')
        return json.load(f_open)


    





if __name__ == "__main__":
    # df = get_player_stats(2016, 'goalies')
    # print(df.head())
    r = get_data_season("2017","2018","data_saved/season_2017_2018.json")
    r2 = get_data_play_by_play("2017020001","data_saved/play_by_play_2017020001.json")