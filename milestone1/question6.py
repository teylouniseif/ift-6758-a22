from operator import index
from matplotlib.figure import Figure
# from matplotlib.figure import figaspect
# from hockey_rink import NHLRink
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import milestone1.question4 as question4
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display
import numpy as np
from milestone1.question4 import *
from sklearn.neighbors import KernelDensity
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
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path,'figures/nhl_rink.png')
    I = Image.open(path)
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
    #Compute the avg shot per match by dividing the number of line in the df by the number of match (number of unique id in df)
    avg_shot_hour = df.shape[0]/df["Game_ID"].nunique()

    if print_rink:
        #If true offers, the possibility to print on a hockey rink the average position of the points
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
    ndf = df[["Team_of_Shooter", "Shot_or_Goal", "Game_ID"]].copy()

    #Count how many shots/goals a team has made in the season
    shot_df = ndf.groupby(["Team_of_Shooter"])["Shot_or_Goal"].count()

    #Count how many game a team has played
    game_df = ndf[["Team_of_Shooter","Game_ID"]].drop_duplicates().groupby(["Team_of_Shooter"])["Game_ID"].count()

    #Compute the average of shot per game (Multiply by 2 to compensate the 2 teams)
    excess_hour = (shot_df/game_df)*2

    #Substract the avg shot per match to all teams avg per match
    return excess_hour-league_avg_shot_hour(df, False)

def KernelD(df) -> pd.DataFrame:
    #Keeps useful columns, removes NAN lines, and values between shot and goal types (starting by shot)
    df = df[["Shot_or_Goal", "X_Coordinate", "Y_Coordinate"]].dropna(axis=0).sort_values(by="Shot_or_Goal", ascending=0).reset_index(drop=True)

    #Turn the coordinates of the goals and the shots in numpy arrays
    goal = df.loc[df.Shot_or_Goal == "Goal"].reset_index(drop = True)[["X_Coordinate", "Y_Coordinate"]].to_numpy()
    shot = df.loc[df.Shot_or_Goal == "Shot"].reset_index(drop = True)[["X_Coordinate", "Y_Coordinate"]].to_numpy()

    shot_goal = [shot, goal]
    types = ["Shots", "Goals"]

    shot_goal_d = list()

    for i in range(len(types)):
        #For every type, train a Kernel density estimator and save its predictions for the type coordinates in shot_goal_d
        kde = KernelDensity(bandwidth=0.03, kernel = 'gaussian')
        kde.fit(shot_goal[i])
        density = np.exp(kde.score_samples(shot_goal[i]))
        shot_goal_d.append(density)

    #Mix all the predictions in a 1D numpy array
    shot_goal_d = np.concatenate((shot_goal_d[0], shot_goal_d[1]))

    #Add a new column in the df with the density
    df["KDensity"] = np.vstack(shot_goal_d)
    return df

#deviser le rink en 16 regions
def diviser_region(df_team: pd.DataFrame):
    dfs_X = []
    df_regions = []
    for i in range(4):
        dfs_X.append(df_team[(df_team['X_Coordinate'].abs()>i*25) & (df_team['X_Coordinate'].abs()<=(i+1)*25)])


    for df_X in dfs_X:
        for i in range(2):
            df_regions.append(df_X[(df_X['Y_Coordinate']>=i*21.25) & (df_X['Y_Coordinate']<(i+1)*21.25)])
        for i in range(2):
            df_regions.append(df_X[(df_X['Y_Coordinate']<i*-21.25) & (df_X['Y_Coordinate']>=(i+1)*-21.25)])


    return df_regions

"""
Une méthode permettant de dessiner les coordonnées de tirs de tous les équipes sur le figure pour une année donnée, mais ces points sont temporairement invisibles.
annee: 2016-2020, pour les regions qui a le excess_shot_rate_hour positive, dessniner les point rouge, sinon les points bleu
"""
def add_points_eachTeam(df, fig : go.Figure , teams):
    dfs_regions = diviser_region(df)
    for i in range(len(teams)):
        for df_region in dfs_regions:
            excess_hour_region =excess_shot_rate_hour(df_region)
            excess_hour_region_team = excess_hour_region[teams[i]]
            df__region_team = df_region.loc[df_region["Team_of_Shooter"]==teams[i]]
            x, y = get_coords_transform(df__region_team)
            if(excess_hour_region_team > 0): #si positive , dessiner les points rouge
                if(i==0):
                    fig.add_trace(
                    go.Scatter(x=x,
                    y=y,
                    mode="markers",
                    marker=dict(color="red",size=3),
                    showlegend=False,
                    visible=True)
                    )
                else:
                    fig.add_trace(
                    go.Scatter(x=x,
                        y=y,
                        mode="markers",
                        marker=dict(color="red",size=3),
                        showlegend=False,
                        visible=False)
                        )
            else:#si negative , dessiner les points bleus
                if(i==0):
                    fig.add_trace(
                    go.Scatter(x=x,
                    y=y,
                    mode="markers",
                    marker=dict(color="blue",size=3),
                    showlegend=False,
                    visible=True)
                    )
                else:
                    fig.add_trace(
                    go.Scatter(x=x,
                        y=y,
                        mode="markers",
                        marker=dict(color="blue",size=3),
                        showlegend=False,
                        visible=False)
                        )
                
        
        
       
                
        

"""
Une méthode permettant de dessiner les coordonnées de tirs de tous les annees sur le figure pour une equipe donnée, mais ces points sont temporairement invisibles.
"""
def add_points_eachYear(df_years : list, fig : go.Figure, team):
    for i in range(len(df_years)):
        dfs_team_region = diviser_region(df_years[i])
        for df_region in dfs_team_region:
            excess_hour_region =excess_shot_rate_hour(df_region)
            excess_hour_region_team = excess_hour_region[team]
            df__region_team = df_region.loc[df_region["Team_of_Shooter"]==team]
            x, y = get_coords_transform(df__region_team)
            if(excess_hour_region_team > 0): #si positive , dessiner les points rouge
                if(i==0):
                    fig.add_trace(
                    go.Scatter(x=x,
                    y=y,
                    mode="markers",
                    marker=dict(color="red",size=3),
                    showlegend=False,
                    visible=True)
                    )
                else:
                    fig.add_trace(
                    go.Scatter(x=x,
                        y=y,
                        mode="markers",
                        marker=dict(color="red",size=3),
                        showlegend=False,
                        visible=False)
                        )
            else:#si negative , dessiner les points bleus
                if(i==0):
                    fig.add_trace(
                    go.Scatter(x=x,
                    y=y,
                    mode="markers",
                    marker=dict(color="blue",size=3),
                    showlegend=False,
                    visible=True)
                    )
                else:
                    fig.add_trace(
                    go.Scatter(x=x,
                        y=y,
                        mode="markers",
                        marker=dict(color="blue",size=3),
                        showlegend=False,
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
                for n in range(16):
                    visibles.append(True)
            else:
                for m in range(16):
                    visibles.append(False)
        
        list_drop_down.append(dict(label=teams[i],
                        method="update",
                        args=[{"visible": visibles},
                            ]))

    fig.update_layout(
    updatemenus=[dict(buttons=list_drop_down)])

    fig.show()
    return fig


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
    df_years = [df2016,df2017,df2018,df2019,df2020]

    fig = get_blank_rink_plotly()
    
    add_points_eachYear(df_years,fig,team)

    years = ["2016","2017","2018","2019","2020"]

    list_drop_down = []
    for i in range(len(years)):
        visibles = []
        for j in range(len(years)):
            if j==i:
                for n in range(16):
                    visibles.append(True)
            else:
                for n in range(16):
                    visibles.append(False)
        
        list_drop_down.append(dict(label=years[i],
                        method="update",
                        args=[{"visible": visibles},
                            ]))

    fig.update_layout(
    updatemenus=[dict(buttons=list_drop_down)])

    fig.show()
    return fig

    


if __name__ == "__main__":
    directory2018 = r'data_saved/play_by_play/2018'
    # """directory2019 = r'data_saved/play_by_play/2019'
    # directory2020 = r'data_saved/play_by_play/2020'"""
    # df2018 = question4.create_full_df(directory=directory2018)
    # print(df2018.info())
    # x, y = get_coords(df2018.loc[df2018["Game_ID"]==2018030114])
    # print(x)
    # print_point(x,y)
    
   

        