import pandas as pd 

#Load Raw data 

team_stats_fbref = pd.read_csv("data/team_stats_fbref_raw.csv", header=[0,1], index_col=[0,1,2])
team_stats_understat = pd.read_csv("data/team_stats_understat_raw.csv")
shooting_stats = pd.read_csv("data/shooting_stats_raw.csv", header=[0,1], index_col=[0,1,2])
player_stats = pd.read_csv("data/player_stats_raw.csv")


#Clean FBref Team Stats 
big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester Utd', 'Manchester United', 'Manchester City', 'Tottenham Hotspur', 'Tottenham']

team_stats_fbref = team_stats_fbref.drop(columns=[('url', 'Unnamed: 23_level_1')])



#Filter for just big 6 teams 
team_stats_fbref = team_stats_fbref[team_stats_fbref.index.get_level_values(2).isin(big_6)]

#Rename Columns to clean names 
team_stats_fbref.columns = ['players_used', 'avg_age', 'possession',
    'matches_played', 'starts', 'minutes', '90s',
    'goals', 'assists', 'goals_assists', 'goals_no_pen',
    'penalties_scored', 'penalties_att', 'yellow_cards', 'red_cards',
    'goals_per90', 'assists_per90', 'goals_assists_per90',
    'goals_no_pen_per90', 'goals_assists_no_pen_per90']


#Clean Understat Team stats
team_stats_understat = team_stats_understat.drop(columns=['league_id', 'season_id', 'game_id', 'home_team_id', 'away_team_id', 'date'])


#Filter for Big 6 teams 
team_stats_understat = team_stats_understat[
    (team_stats_understat['home_team'].isin(big_6)) |
    (team_stats_understat['away_team'].isin(big_6))
]






#Clean Shooting Stats 
shooting_stats = shooting_stats.drop(columns=[('url', 'Unnamed: 15_level_1')])

#Filter for big 6 
shooting_stats = shooting_stats[shooting_stats.index.get_level_values(2).isin(big_6)]

#Rename columns 
shooting_stats.columns = ['players_used', '90s', 'goals', 'shots', 'shots_on_target',
    'shots_on_target_pct', 'shots_per90', 'shots_on_target_per90',
    'goals_per_shot', 'goals_per_shot_on_target',
    'penalties_scored', 'penalties_att']


#Clean Player stats 

#Filter for just Arsenal players 
player_stats = player_stats[player_stats['team'] == 'Arsenal']

#Drop Columns not needed
player_stats = player_stats.drop(columns=['league_id', 'season_id', 'team_id', 'player_id'])






#Save Clean Data

team_stats_fbref.to_csv("data/team_stats_clean.csv", index=True)
team_stats_understat.to_csv("data/team_stats_understat_clean.csv", index=False)
shooting_stats.to_csv("data/shooting_stats_clean.csv", index=True)
player_stats.to_csv("data/player_stats_clean.csv", index=False)



print("Tranformation complete")
print(f"Team FBref Stats: {team_stats_fbref.shape}")
print(f"Understat team Stats: {team_stats_understat.shape}")
print(f"Shooting Stats: {shooting_stats.shape}")
print(f"Player Stats: {player_stats.shape}")
