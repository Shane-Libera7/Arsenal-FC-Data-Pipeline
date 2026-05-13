import pandas as pd 

#Load Raw data 

team_stats = pd.read_csv("data/team_stats_raw.csv", header=[0,1], index_col=[0,1,2])
shooting_stats = pd.read_csv("data/shooting_stats_raw.csv", header=[0,1], index_col=[0,1,2])
player_stats = pd.read_csv("data/player_stats_raw.csv", header=[0,1], index_col=[0,1,2])


#Clean Team Stats 

team_stats = team_stats.drop(columns=[('url', 'Unnamed: 23_level_1')])

#Rename Columns to clean names 
team_stats.columns = ['players_used', 'avg_age', 'possession',
    'matches_played', 'starts', 'minutes', '90s',
    'goals', 'assists', 'goals_assists', 'goals_no_pen',
    'penalties_scored', 'penalties_att', 'yellow_cards', 'red_cards',
    'goals_per90', 'assists_per90', 'goals_assists_per90',
    'goals_no_pen_per90', 'goals_assists_no_pen_per90']

#Clean Shooting Stats 

shooting_stats = shooting_stats.drop(columns=[('url', 'Unnamed: 15_level_1')])

#Rename columns 
shooting_stats.columns = ['players_used', '90s', 'goals', 'shots', 'shots_on_target',
    'shots_on_target_pct', 'shots_per90', 'shots_on_target_per90',
    'goals_per_shot', 'goals_per_shot_on_target',
    'penalties_scored', 'penalties_att']


#Clean Player stats 

#Drop Columns not needed
player_stats = player_stats.drop(columns=['nation', 'born', 'Unnamed: 3_level_0'])

#Sort index 
player_stats = player_stats.sort_index()

#Drop nulls 
player_stats = player_stats.dropna()

#Filter for just Arsenal players 
player_stats = player_stats[player_stats.index.get_level_values(2) == 'Arsenal']


#Rename columns 
player_stats.columns = ['position', 'age',
    'matches_played', 'starts', 'minutes', '90s',
    'goals', 'assists', 'goals_assists', 'goals_no_pen',
    'penalties_scored', 'penalties_att', 'yellow_cards', 'red_cards',
    'goals_per90', 'assists_per90', 'goals_assists_per90',
    'goals_no_pen_per90', 'goals_assists_no_pen_per90']




#Fix Data Types 

for col in ['matches_played', 'starts', 'minutes', 'yellow_cards', 'red_cards']:
    player_stats[col] = player_stats[col].astype(int)




#Save Clean Data

team_stats.to_csv("data/team_stats_clean.csv", index=True)
shooting_stats.to_csv("data/shooting_stats_clean.csv", index=True)
player_stats.to_csv("data/player_stats_clean.csv", index=True)



print("Tranformation complete")
print(f"Team Stats: {team_stats.shape}")
print(f"Shooting Stats: {shooting_stats.shape}")
print(f"Player Stats: {player_stats.shape}")
