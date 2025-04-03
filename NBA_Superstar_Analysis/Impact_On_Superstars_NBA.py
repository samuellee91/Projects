#!/usr/bin/env python
# coding: utf-8

# # Import and Install Necessary Tools

# In[225]:


# Install necessary packages


# In[226]:


pip install nba_api


# In[227]:


# import necessary toolsets
import pandas as pD
import numpy as nP
from scipy import stats
#pD.set_option('display.max_rows', 500)
#pD.set_option('display.max_columns', 500)


# In[228]:


from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from nba_api.stats.endpoints import LeagueGameFinder, boxscoretraditionalv2
from nba_api.stats.library.parameters import Season


# In[229]:


# Define NBA Superstar and join date
nbaStar = "Shaquille O'Neal"
nbaTeam = 'LAL'
joinDate = '1996-07-18'
season = '1995-1997'
startSeason = 1995
endSeason = 1997


# # Pull Team Data via API

# In[230]:


# get team id based on team string name
def getTeamID(teamName):
    allTeams = teams.get_teams()

    teamId = None
    for team in allTeams:
        if teamName.lower() in team['abbreviation'].lower():
            return team['id']

    return(f"{teamName} not found")


# In[231]:


# Function to add Opponenet's score to the Data Frame
def addOpponentScore(gameDf):
    # get list of all game ID
    gameDf['OPPONENT_SCORE'] = None
    
    for index, row in gameDf.iterrows():
        gameId = row['GAME_ID']
        
        teamAbbr = row['TEAM_ABBREVIATION']
        
        # Get corresponding game by game id
        opponent = gameDf[gameDf['GAME_ID'] == gameId]
        
        # Find opponent's row
        opponent = opponent[opponent['TEAM_ABBREVIATION'] != teamAbbr]
        
        # Get opponent's score and add it to new column
        if not opponent.empty:
            opponent = opponent.iloc[0]['PTS']
            gameDf.at[index, 'OPPONENT_SCORE'] = opponent
        
    return gameDf


# In[232]:


# Get Game Schedule for specific team in specific time frame
def getGameSchedule(startSeason, endSeason):
    allGames = pD.DataFrame()
    for season in range(startSeason, endSeason):
        seasonId = f"{season}-{str(season + 1)[2:]}"
        gameFinder = leaguegamefinder.LeagueGameFinder(season_nullable=seasonId)
        try:
            # Get the data and convert it to a DataFrame
            gameSchedule = gameFinder.get_data_frames()[0]
            
            # Concatenate this season's data with the previous data
            allGames = pD.concat([allGames, gameSchedule], ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for season {seasonId}: {e}")
            
    return allGames


# In[233]:


#Get game schedule based on 
allGamesData = getGameSchedule(startSeason,endSeason) # get data frame of all games for that team


# In[234]:


allGamesWithOpponent = addOpponentScore(allGamesData) # add opponent's score to the data frame


# In[235]:


# Filter by desired team
allGames = allGamesWithOpponent[allGamesWithOpponent['TEAM_ABBREVIATION'] == nbaTeam]


# # A/B Testing (t-test)

# In[236]:


# Convert join date to datetme
starJoinDate = pD.to_datetime(joinDate)


# In[237]:


# Categorize pre and post superstar addition
allGames = allGames.copy() #added in because Python unsure if only COPY of DF was being manipulated
allGames['GAME_DATE'] = pD.to_datetime(allGames['GAME_DATE'])
preSuperStar = allGames[allGames['GAME_DATE'] < starJoinDate]
postSuperStar = allGames[allGames['GAME_DATE'] >= starJoinDate]


# In[238]:


# Get Team PTS, WIN %, and plus/minus
preSuperStarPts = preSuperStar['PTS']
postSuperStarPts = postSuperStar['PTS']

preSuperStarWinPct = preSuperStar['WL'].apply(lambda x: 1 if x == 'W' else 0)
postSuperStarWinPct = postSuperStar['WL'].apply(lambda x: 1 if x == 'W' else 0)
preWinPct = preSuperStar['WL'].map({'W': 1, 'L': 0}).mean() * 100
postWinPct = postSuperStar['WL'].map({'W': 1, 'L': 0}).mean() * 100

preSuperStarPlusMin = preSuperStar['PLUS_MINUS']
postSuperStarPlusMin = postSuperStar['PLUS_MINUS']


# In[239]:


# Perform T-test for pre and post superstar
# T-test Team Pts

tStatsPts, pValuePts = stats.ttest_ind(preSuperStarPts, postSuperStarPts)


# In[240]:


# T-test Win %
tStatsWinPct, pValueWinPct = stats.ttest_ind(preSuperStarWinPct,postSuperStarWinPct)


# In[241]:


# T-test Plus/Minus
tStatsPlusMin, pValuePlusMin = stats.ttest_ind(preSuperStarPlusMin, postSuperStarPlusMin)


# In[242]:


#significance level
alpha = 0.05


# In[243]:


#Store into dataframe
results = {
    'Metric': ['Win Percentage', 'Plus/Minus', 'Team Points Made'],
    'Pre-Superstar Mean': [preWinPct, preSuperStarPlusMin.mean(), preSuperStarPts.mean()],
    'Post-Superstar Mean': [postWinPct, postSuperStarPlusMin.mean(), postSuperStarPts.mean()],
    'T-statistic': [tStatsWinPct, tStatsPlusMin, tStatsPts],
    'P-value': [pValueWinPct, pValuePlusMin, pValuePts],
    'Significance': ['Significant' if pValueWinPct < alpha else 'Not Significant', 
                     'Significant' if pValuePlusMin < alpha else 'Not Significant',
                     'Significant' if pValuePts < alpha else 'Not Significant']
}


# In[244]:


resultsDf = pD.DataFrame(results)


# In[245]:


resultsDf


# In[246]:


#Export out to CSV to show in Power BI
resultsDf.to_csv(f'{nbaStar}_join_{nbaTeam}_analysis_results.csv', index=False)


# In[ ]:





# In[249]:


# Combine CSV files, add player column name and export 1 csv as a dataframe for Power BI visualization
filePaths = [
    'Lebron James_join_LAL_analysis_results.csv',
    'Kyrie Irving_join_BOS_analysis_results.csv',
    'Donovan Mitchell_join_CLE_analysis_results.csv',
    'James Harden_join_HOU_analysis_results.csv'
]

dfs = []

for file in filePaths:
    if file.endswith('.csv'): 
        df = pD.read_csv(file)
        
        playerName = file.split('_')[0]
        
        df['Player'] = playerName
        
        dfs.append(df)
        
combinedDf = pD.concat(dfs, ignore_index = True)
combinedDf.to_csv('Combined_Player_analysis_results.csv', index = False)

