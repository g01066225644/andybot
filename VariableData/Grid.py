import pandas as pd
from ast import literal_eval


class Grid:
    def __init__(self, location):
        col = ['지역', '좌표']
        df = pd.read_csv('grid.csv', names=col, converters={'좌표': literal_eval})
        self.xy = df.loc[df['지역'] == location, '좌표'].values[0]

    def get_xy(self):
        return self.xy

