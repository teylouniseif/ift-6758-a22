import os
import requests
from tqdm import tqdm

class HockeySeason:
    def __init__(self, start_year):
        self.start_year = start_year
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.datapath = os.path.join(current_dir,os.getenv('DATAPATH', 'data'))
    def download(self):
        if not os.path.isdir(self.datapath):
            os.mkdir(self.datapath)
        if not os.path.isdir(os.path.join(self.datapath,str(self.start_year))):
            os.mkdir(os.path.join(self.datapath,str(self.start_year)))
        reg_season = 1230
        if self.start_year >= 2017:
            reg_season = 1271
        for j in tqdm(range(reg_season)):
            for i in range(1, 5):
                try:
                    id = str(self.start_year)+str(i).zfill(2)+str(j).zfill(4)
                    url = f'https://statsapi.web.nhl.com/api/v1/game/{id}/feed/live'
                    response = requests.get(url)
                    f = open(os.path.join(self.datapath,id), 'w')
                    f.write(response.text)
                    f.close()
                except Exception as e:
                    continue
                
