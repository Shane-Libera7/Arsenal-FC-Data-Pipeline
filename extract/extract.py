import soccerdata as sd

fbref = sd.FBref(leagues="ENG-Premier League", seasons=["2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"])


#Pull team Stats 
team_stats = fbref.read_team_season_stats(stat_type="standard")

#Pull shooting stats for xG
shooting_stats = fbref.read_team_season_stats(stat_type="shooting")

#Player stats of just Arsenal 
player_stats = fbref.read_player_season_stats(stat_type="standard")


#Save to CSV 
team_stats.to_csv("data/team_stats_raw.csv", index=True)
shooting_stats.to_csv("data/shooting_stats_raw.csv", index=True)
player_stats.to_csv("data/player_stats_raw.csv", index=True)
print("All stats saved successfully")



