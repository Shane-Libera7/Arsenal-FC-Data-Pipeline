import pandas as pd 
import pytest 
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os 


load_dotenv(dotenv_path=".env")

#Load Clean Data 
team_stats_fbref = pd.read_csv("data/team_stats_clean.csv")
team_stats_understat = pd.read_csv("data/team_stats_understat_clean.csv")
shooting_stats = pd.read_csv("data/shooting_stats_clean.csv")
player_stats = pd.read_csv("data/player_stats_clean.csv")


#Database connection 
def get_engine():
    return create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )



#Shape Tests
def test_fbref_team_stats_row_count():
    assert len(team_stats_fbref) == 30

def test_shooting_stats_row_count():
    assert len(shooting_stats) == 30

def test_player_stats_has_rows():
    assert len(player_stats) > 0

#Season Coverage Tests 
expected_seasons_str = ['2122', '2223', '2324', '2425', '2526']
expected_seasons_int = [2122, 2223, 2324, 2425, 2526]

def test_all_seasons_present_team_stats_understat():
    actual_seasons = team_stats_understat['season'].unique().tolist()
    for season in expected_seasons_int:
        assert season in actual_seasons

def test_all_seasons_present_team_stats_fbref():
    actual_seasons = team_stats_fbref['season'].astype(str).unique().tolist()
    for season in expected_seasons_str:
        assert season in actual_seasons

def test_all_seasons_present_shooting():
    actual_seasons = shooting_stats['season'].astype(str).unique().tolist()
    for season in expected_seasons_str:
        assert season in actual_seasons
        

def test_all_seasons_present_players():
    actual_seasons = player_stats['season'].unique().tolist()
    for season in expected_seasons_int:
        assert season in actual_seasons



#Filter Tests
def test_player_stats_arsenal_only():
    assert player_stats['team'].unique().tolist() == ['Arsenal']

def test_team_stats_febref_big_6_only():
    big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester Utd', 'Tottenham Hotspur']
    teams = team_stats_fbref['team'].unique().tolist()
    for team in teams:
        assert team in big_6


def test_team_stats_understat_big_6_only():
    big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester United', 'Tottenham']
    for _, row in team_stats_understat.iterrows():
        assert row['home_team'] in big_6 or row['away_team'] in big_6





#Null Tests

def test_no_nulls_in_player_goals():
    assert player_stats['goals'].isnull().sum() == 0

def test_no_nulls_in_team_stats():
    assert team_stats_fbref['goals'].isnull().sum() == 0

def test_no_nulls_in_understat_xg():
    assert team_stats_understat['home_xg'].isnull().sum() == 0


#Value Range Tests 
def test_goals_non_negative():
    assert (player_stats['goals'] >= 0).all()

def test_ppda_realistic_range():
    assert (team_stats_understat['home_ppda'] > 0).all()
    assert (team_stats_understat['home_ppda'] < 200).all()

def test_xg_non_negative():
    assert (team_stats_understat['home_xg'] >= 0).all()
    assert (team_stats_understat['away_xg'] >= 0).all()


#Data Type Tests
def test_player_stats_minutes_is_numeric():
    assert pd.api.types.is_numeric_dtype(player_stats['minutes'])

def test_understat_ppda_is_float():
    assert pd.api.types.is_float_dtype(team_stats_understat['home_ppda'])


#Database Tests
def test_database_connection():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1

def test_all_tables_exist():
    engine = get_engine()
    expected_tables = [
        'fbref_team_stats',
        'shooting_stats',
        'understat_team_stats',
        'player_stats'
    ]
    with engine.connect() as conn:
        for table in expected_tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            assert count > 0