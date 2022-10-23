from operator import index
from matplotlib.figure import Figure
# from matplotlib.figure import figaspect
# from hockey_rink import NHLRink
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import question4
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display
import numpy as np
from question4 import *
# from matplotlib.widgets import Button



#Une fonction qui dessine une patinoire vide
# def get_blank_rink():
#     global fig
#     fig=plt.figure(figsize=(10,10))
#     ax = fig.add_subplot(111)
#     ax.set_facecolor("white")
#     fig.patch.set_facecolor("white")
#     fig.patch.set_alpha(0.0)
#     ax.set_xticklabels(labels = [''], fontsize = 18,alpha = .7,minor=False)
#     ax.set_yticklabels(labels = [''], fontsize = 18,alpha = .7,minor=False)
#     I = Image.open('figures/nhl_rink.png')
#     box = (I.size[0]/2,0,I.size[0],I.size[1])
#     imgcut = I.crop(box)
#     imgcut = I.crop(box)
#     ax.imshow(imgcut);#width, height = imgcut.size
#     print(fig)

#Une fonction qui dessine une patinoire vide
def get_blank_rink_plotly() ->  go.Figure:
    I = Image.open('figures/nhl_rink.png')
    box = (I.size[0]/2,0,I.size[0],I.size[1])
    imgcut = I.crop(box)

    # Create figure
    fig = go.Figure()

    img_width = 550
    img_height = 467


    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width ]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height],
        scaleanchor="x"
    )
    
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width,
            y=img_height,
            sizey=img_height,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source= imgcut)
    )
    fig.update_layout(
        width=img_width,
        height=img_height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    return fig




    
    

"""
Une fonction qui dessine des coordonnées de tir sur l'image d'une patinoire.

entree: x, y sont les pandas.series qui contient les cordonnees x et y
 
"""
def print_points_plotly(x,y):
    I = Image.open('/Users/hrh/Desktop/programmeFile/dataSicence/projet/ift-6758-a22/figures/nhl_rink.png')
    box = (I.size[0]/2,0,I.size[0],I.size[1])
    imgcut = I.crop(box)

    # Create figure
    fig = go.Figure()

    fig.add_scatter(x=x,
                    y=y,mode="markers",marker=dict(
                        color="blue",
                        size=7 ))
    img_width = 550
    img_height = 467

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width ]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height],
        scaleanchor="x"
    )
    
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width,
            y=img_height,
            sizey=img_height,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source= imgcut)
    )

    fig.update_layout(
        width=img_width,
        height=img_height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    fig.show()


#une fonction qui transformer les cordonnees reel en cordonnees image
def get_coords_transform(df):
    """
    true rink: x->[-100,+100]
    y->[-42.5,+42.5]
    our image: x->[0,550]
    y->[0, 467]
    """
    x = df["X_Coordinate"].abs()
    y = df["Y_Coordinate"]
    #transformer les true cordonnee en codonnee image
    x= x.apply(lambda x: (x/100) * 550)
    y= y.apply(lambda y:  233.5 + (y/42.5) * 233.5 if y>0 else  233.5 - (-y/42.5) * 233.5)
    return x, y

def league_avg_shot_hour(df, print_rink=True):
    avg_shot_hour = df.shape[0]/df["Game_ID"].nunique()

    if print_rink:
        
        x = df["X_Coordinate"].abs()
        y = df["Y_Coordinate"]
        x_avg = x.sum()/x.shape[0]
        y_avg = y.sum()/x.shape[0]
        x_avg_image =  (x_avg/100) * 550
        y_avg_image = 233.5 + (y_avg/42.5) * 233.5 if y_avg>0 else  233.5 - (-y_avg/42.5) * 233.5
        print("x:",x_avg, "y:", y_avg)

        
        print_points_plotly(pd.Series(x_avg_image),pd.Series(y_avg_image))

    return avg_shot_hour

def excess_shot_rate_hour(df):
    #Copy only the elements we want
    df = df[["Team_of_Shooter", "Shot_or_Goal", "Game_ID"]].copy()

    #Count how many shots/goals a team has made in the season
    shot_df = df.groupby(["Team_of_Shooter"])["Shot_or_Goal"].count()

    #Count how many game a team has played
    game_df = df[["Team_of_Shooter","Game_ID"]].drop_duplicates().groupby(["Team_of_Shooter"])["Game_ID"].count()

    #Compute the average of shot per game (Multiply by 2 to compensate the 2 teams)
    excess_hour = (shot_df/game_df)*2

    return excess_hour

"""
Une méthode permettant de dessiner les coordonnées de tirs de tous les équipes sur le figure pour une année donnée, mais ces points sont temporairement invisibles.
annee: 2016-2020
"""
def add_points_eachTeam(df, fig : Figure , teams):
    # teams = list(set(df["Team_of_Shooter"].tolist()))
    for i in range(len(teams)):
        x, y = get_coords_transform(df.loc[df["Team_of_Shooter"]==teams[i]])
        #par default le premier team est visible!
        if(i==0):
            fig.add_trace(
            go.Scatter(x=x,
            y=y,
            mode="markers",
            marker=dict(color="blue",size=7),
            visible=True)
            )
        else:
            fig.add_trace(
            go.Scatter(x=x,
                y=y,
                mode="markers",
                marker=dict(color="blue",size=7),
                visible=False)
                )
"""
Une méthode permettant de dessiner les coordonnées de tirs de tous les annees sur le figure pour une equipe donnée, mais ces points sont temporairement invisibles.
"""
def add_points_eachYear(df_years : list, fig : Figure):
    for i in range(len(df_years)):
        x, y = get_coords_transform(df_years[i])
        if(i==0):
            fig.add_trace(
            go.Scatter(x=x,
            y=y,
            mode="markers",
            marker=dict(color="blue",size=7),
            visible=True)
            )
        else:
            fig.add_trace(
            go.Scatter(x=x,
                y=y,
                mode="markers",
                marker=dict(color="blue",size=7),
                visible=False)
                )


"""
Une méthode qui peut rendre le graphique interactif, avec des options pour sélectionner l'équipe.
"""
def print_cordonne_tir_eachTeam(year):
    path = 'data_saved/play_by_play/'+year
    df = create_full_df(directory=path)

    fig = get_blank_rink_plotly()

    teams = list(set(df["Team_of_Shooter"].tolist()))
    add_points_eachTeam(df,fig, teams)

    
    list_drop_down = []
    for i in range(len(teams)):
        visibles = []
        for j in range(len(teams)):
            if j==i:
                visibles.append(True)
            else:
                visibles.append(False)
        
        list_drop_down.append(dict(label=teams[i],
                        method="update",
                        args=[{"visible": visibles},
                            ]))

    fig.update_layout(
    updatemenus=[dict(buttons=list_drop_down)])

    fig.show()

"""
Une méthode qui peut creer un graphique interactif pour chaque saison de 2016-17 à 2020-2021. 
"""
def print_cordonne_tir_eachYear(team):
    directory2018 = r'data_saved/play_by_play/2018'
    directory2017 = r'data_saved/play_by_play/2017'
    directory2016 = r'data_saved/play_by_play/2016'
    directory2019 = r'data_saved/play_by_play/2019'
    directory2020 = r'data_saved/play_by_play/2020'
    df2018 = create_full_df(directory=directory2018)
    df2017 = create_full_df(directory=directory2017)
    df2016 = create_full_df(directory=directory2016)
    df2019 = create_full_df(directory=directory2019)
    df2020 = create_full_df(directory=directory2020)
    df_years = [df2016.loc[df2016["Team_of_Shooter"]==team],df2017.loc[df2017["Team_of_Shooter"]==team],df2018.loc[df2018["Team_of_Shooter"]==team],
    df2019.loc[df2019["Team_of_Shooter"]==team],df2020.loc[df2020["Team_of_Shooter"]==team]]

    fig = get_blank_rink_plotly()
    
    add_points_eachYear(df_years,fig)

    years = ["2016","2017","2018","2019","2020"]

    list_drop_down = []
    for i in range(len(years)):
        visibles = []
        for j in range(len(years)):
            if j==i:
                visibles.append(True)
            else:
                visibles.append(False)
        
        list_drop_down.append(dict(label=years[i],
                        method="update",
                        args=[{"visible": visibles},
                            ]))

    fig.update_layout(
    updatemenus=[dict(buttons=list_drop_down)])

    fig.show()
    



if __name__ == "__main__":
    directory2018 = r'data_saved/play_by_play/2018'
    # """directory2019 = r'data_saved/play_by_play/2019'
    # directory2020 = r'data_saved/play_by_play/2020'"""
    # df2018 = question4.create_full_df(directory=directory2018)
    # print(df2018.info())
    # x, y = get_coords(df2018.loc[df2018["Game_ID"]==2018030114])
    # print(x)
    # print_point(x,y)
    
   

        