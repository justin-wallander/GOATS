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

# NBA scraping 
nba_years = list(range(1977, 2020))
for i in nba_years:
    url = f'https://www.basketball-reference.com/leagues/NBA_{i}_totals.html'

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]


    rows= []
    for tr in parsed_table.find_all('tr'):
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
    df.to_csv(f'data/nba/NBA_{i}.csv')



#reading in and cleaning up dataframes
# 2019 was completed in setting this up, so we will range to 2018   
nfl_years = list(range(1970, 2019))
for i in nfl_years:

    nfl_i = pd.read_csv(f'data/nfl/NFL_{i}.csv')
    #adding Years column
    # nfl_i.columns = ['Unnamed: 0', 'Player', 'Tm', 'FantPos', 'Age', 'G', 'GS', 'Cmp', 'Att',
    #    'Yds', 'TD', 'Int', 'Att.1', 'Yds.1', 'Y/A', 'TD.1', 'Tgt', 'Rec',
    #    'Yds.2', 'Y/R', 'TD.2', 'Fmb', 'FL', 'TD.3', '2PM', '2PP', 'FantPt',
    #    'PPR', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'Year']
    nfl_i['Year'] = i
    #making Tgt column if it does not exist:
    if 'Tgt' not in nfl_i.columns:
        nfl_i['Tgt'] = 0
    #removing idx col- not sure if this defaults when I save or what
    nfl_i = nfl_i.iloc[:, 1:]

    #cleaning columns with NaN values
    nfl_i.FantPos = nfl_i.FantPos.fillna('?')
    nfl_i['Y/A'] = nfl_i['Y/A'].fillna(0)
    nfl_i['Y/R'] = nfl_i['Y/R'].fillna(0)
    nfl_i['2PM'] = nfl_i['2PM'].fillna(0)
    nfl_i['2PP'] = nfl_i['2PP'].fillna(0)
    nfl_i['FantPt'] = nfl_i['FantPt'].fillna(0)
    nfl_i['PPR'] = nfl_i['PPR'].fillna(0)
    nfl_i['DKPt'] = nfl_i['DKPt'].fillna(0)
    nfl_i['FDPt'] = nfl_i['FDPt'].fillna(0)
    nfl_i['VBD'] = nfl_i['VBD'].fillna(0)
    del nfl_i['OvRank']

    #deleting header rows:
    nfl_i = nfl_i[nfl_i.Age != 'FantPos']


    #changing dtype to float for specific cols:
    val_col = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Yds', 'TD', 'Int', 'Att.1', 'Yds.1', 'Y/A', 'TD.1',
        'Tgt', 'Rec', 'Yds.2', 'Y/R', 'TD.2', 'Fmb', 'FL', 'TD.3', '2PM', '2PP', 'FantPt', 'PPR',
        'DKPt', 'FDPt', 'VBD', 'PosRank']

    for col in val_col:
        nfl_i[col] = nfl_i[col].astype(float)

    #saving to csv

    nfl_i.to_csv(f'data/nfl/NFL_{i}.csv', index = False)

#merging to one master csv:
master = pd.read_csv('data/nfl/NFL_1970.csv')
for col in master.columns:
    if 'Unnamed' in col:
        del master[col]
nfl_years = list(range(1971, 2020))
for i in nfl_years:

    nfl_i = pd.read_csv(f'data/nfl/NFL_{i}.csv')
    for col in nfl_i.columns:
        if 'Unnamed' in col:
            del nfl_i[col]
    master = master.append(nfl_i, ignore_index = True)

master.to_csv('data/nfl/Master.csv')
print(master.shape)
print(master.describe())
print(master.info())














nba_2019 = pd.read_csv('data/nba/NBA_2019.csv')
print(nba_2019.head())

    


