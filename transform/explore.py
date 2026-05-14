import pandas as pd 

team_stats_fbref = pd.read_csv("data/team_stats_fbref_raw.csv", header=[0,1], index_col=[0,1,2])
team_stats_understat = pd.read_csv("data/team_stats_understat_raw.csv")
shooting_stats = pd.read_csv("data/shooting_stats_raw.csv", header=[0,1], index_col=[0,1,2])
player_stats = pd.read_csv("data/player_stats_raw.csv")


print(("-- FBREF TEAM STATS--"))
print(team_stats_fbref.shape)
print(team_stats_fbref.dtypes)
print(team_stats_fbref.isnull().sum())

print("-- UNDERSTAT TEAM STATS--")
print(team_stats_understat.shape)
print(team_stats_understat.dtypes)
print(team_stats_understat.isnull().sum())

print(("--SHOOTING STATS--"))
print(shooting_stats.shape)
print(shooting_stats.dtypes)
print(shooting_stats.isnull().sum())

print(("-- PLAYER STATS--"))
print(player_stats.shape)
print(player_stats.dtypes)
print(player_stats.isnull().sum())




