import soccerdata as sd
understat = sd.Understat(leagues="ENG-Premier League", seasons=["2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"])
fbref = sd.FBref(leagues="ENG-Premier League", seasons=["2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"], no_cache=False)


#Pull Team Overview Stats -- later to be filtered for just Big 6 (Arsenal, Chelsea, Liverpool, Man City, Man Utd, Spurs)
team_stats_fbref = fbref.read_team_season_stats(stat_type="standard")
team_stats_fbref.to_csv("data/team_stats_fbref_raw.csv", index=True)
print("Overall team stats saved successfully")

#Team xG and pressing data -- later to be filtered for just Big 6 teams 
team_stats_understat = understat.read_team_match_stats()
team_stats_understat.to_csv("data/team_stats_understat_raw.csv", index=True)
print("xG stats saved successfully")


#Pull standard G/A stats of teams -- later to be filtered for just big 6 teams
shooting_stats = fbref.read_team_season_stats(stat_type="shooting")
shooting_stats.to_csv("data/shooting_stats_raw.csv", index=True)
print("Shooting stats saved successfully")

#Player stats -- to later be filtered for just Arsenal
player_stats = understat.read_player_season_stats()
player_stats.to_csv("data/player_stats_raw.csv", index=True)
print("Player stats saved successfully")









