import pandas as pd 

team_stats = pd.read_csv("data/team_stats_raw.csv", header=[0,1], index_col=[0,1,2])
shooting_stats = pd.read_csv("data/shooting_stats_raw.csv", header=[0,1], index_col=[0,1,2])
player_stats = pd.read_csv("data/player_stats_raw.csv", header=[0,1], index_col=[0,1,2])


print(("-- TEAM STATS--"))
print(team_stats.shape)
print(team_stats.dtypes)
print(team_stats.isnull().sum())

print(("-- SHOOTING STATS--"))
print(shooting_stats.shape)
print(shooting_stats.dtypes)
print(shooting_stats.isnull().sum())

print(("-- PLAYER STATS--"))
print(player_stats.shape)
print(player_stats.dtypes)
print(player_stats.isnull().sum())
