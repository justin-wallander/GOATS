from pymongo import MongoClient
import pprint
import pandas as pd 
import matplotlib.pyplot as plt 
import requests
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)


#NBA scraping -  totals going back to 1977 and then determine fantasy points from totals? or go based off PER
#might just focus on football/basketball for now


#NFL scraping- fantasy stats going back to 1970 and saving as CSV
nfl_years = list(range(1970, 2020))
for i in nfl_years:
    url = f'https://www.pro-football-reference.com/years/{i}/fantasy.htm'

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]


    rows= []
    for tr in parsed_table.find_all('tr')[1:]:
        cells = []
        tds = tr.find_all('td')
        if len(tds) == 0:
            ths = tr.find_all('th')
            for th in ths:
                cells.append(th.text.strip())
        else:
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    del rows[0][0]

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]
    df.to_csv(f'data/nfl/NFL_{i}.csv')

#reading in and cleaning up dataframes    

df_2019 = pd.read_csv('data/nfl/NFL_2019.csv')
print(df_2019.OvRank)

    


