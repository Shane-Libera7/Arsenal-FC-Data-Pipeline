import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Load environment variables from .env file 
load_dotenv()

#Database connection 
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


#Load Clean Data 
team_stats_fbref = pd.read_csv("data/team_stats_clean.csv")
team_stats_understat = pd.read_csv("data/team_stats_understat_clean.csv")
shooting_stats = pd.read_csv("data/shooting_stats_clean.csv")
player_stats = pd.read_csv("data/player_stats_clean.csv")

#Reset Index on FBref files to make it suitable for PostgreSQL
team_stats_fbref = team_stats_fbref.reset_index()
shooting_stats = shooting_stats.reset_index()


#Load data into PostgreSQL
team_stats_fbref.to_sql("fbref_team_stats", engine, if_exists="replace", index=False)
print(team_stats_fbref.shape)
print("FBref Team Stats loaded")

team_stats_understat.to_sql("understat_team_stats", engine, if_exists="replace", index=False)
print(team_stats_understat.shape)
print("Understat Team Stats loaded")

shooting_stats.to_sql("shooting_stats", engine, if_exists="replace", index=False)
print(shooting_stats.shape)
print("Shooting Stats loaded")

player_stats.to_sql("player_stats", engine, if_exists="replace", index=False)
print(player_stats.shape)
print("Arsenal Player Stats Loaded")

print("All data loaded into PostgreSQL successfully")