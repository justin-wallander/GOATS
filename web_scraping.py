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

#NFL
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



#NBA data cleaning and merging

nba_years = list(range(1977, 2020))
for i in nba_years:
    nba_i = pd.read_csv(f'data/nba/NBA_{i}.csv')
    nba_i = nba_i[nba_i.Age != 'Pos']
    nba_i['Year'] = i
    nba_i = nba_i.reset_index()
    cols = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG',
            'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT',
            'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
            'PTS', 'Year']
    nba_i = nba_i[cols]
    nba_i['Player'] = nba_i['Player'].apply(lambda x: x.replace('*', ''))

    #issue where if a player was traded, he is in with both teams and then a total is inputted as well

    multi_entries = nba_i['Player'].value_counts() > 1
    multi_names = []
    for idx, val in enumerate(multi_entries.index):
        if multi_entries[idx]:
            multi_names.append(val)

    delete_idx = []
    for idx, row in nba_i.iterrows():
        for ele in multi_names:
            if row['Player'] == ele and row['Tm'] != 'TOT':
                delete_idx.append(idx)
    nba_i = nba_i.drop(nba_i.index[delete_idx])


    val_cols = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P',
                '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST',
                'STL', 'BLK', 'TOV', 'PF', 'PTS']

    str_cols = ['Player', 'Pos', 'Tm']
    for col in str_cols:
        nba_i[col] = nba_i[col].fillna('?')

    for col in val_cols:
        nba_i[col] = nba_i[col].fillna(0)
        nba_i[col] = nba_i[col].astype(float)

    nba_i.to_csv(f'data/nba/NBA_{i}.csv')


#merging to one master csv:
master = pd.read_csv('data/nba/NBA_1977.csv')
for col in master.columns:
    if 'Unnamed' in col:
        del master[col]
nba_years = list(range(1978, 2020))
for i in nba_years:

    nba_i = pd.read_csv(f'data/nba/NBA_{i}.csv')
    for col in nba_i.columns:
        if 'Unnamed' in col:
            del nba_i[col]
    master = master.append(nba_i, ignore_index = True)

master.to_csv('data/nba/Master_NBA.csv')
print(master.shape)
print(master.info())
print(master.describe())



    


