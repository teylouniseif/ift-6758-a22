import pandas as pd
import json
import tqdm
import os
import numpy as np
from question4 import *

def split_DF_by_Distances(df: pd.DataFrame):
    metaDF = []
    for i in range(40):
        df1 = df[df['Distance']>= i*5]
        df1 = df1[df1['Distance']< (i*5)+5]
        metaDF.append(df1)
    return metaDF

def get_Chances_Goal(list):
    chances = []
    try:
        for (i,ex) in enumerate(list):
            count = 0
            for event in ex.iterrows():
                if event[1][5]=="Goal":
                    count += 1
            chances.append(count/len(ex))
    except Exception as e:
        chances.append(0.0)
    return(chances)

if __name__ == "__main__":
    directory = r'data_saved'
    df = create_full_df(directory=directory)
    splitDF = split_DF_by_Distances(df)
    get_Chances_Goal(splitDF)