import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import numpy as np 
from adjustText import adjust_text
import plotly.express as px
import plotly.graph_objects as go
import os 

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


#Database Connection
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")







#Q1 - xG vs Goals Trend 
# -- How has Arsenal's xG compared to actual goals scored across the last 5 seasons?

def q1_xg_vs_goals():
    df = pd.read_sql(""" 
                     SELECT season, home_team, away_team, home_goals, away_goals, home_xg, away_xg
                     FROM understat_team_stats
                     WHERE home_team = 'Arsenal' OR away_team = 'Arsenal'
                     """, engine)
    

    
    #Create  unified Arsenal goals and xG columns 
    df['arsenal_goals'] = np.where(df['home_team'] == 'Arsenal', df['home_goals'], df['away_goals'])
    df['arsenal_xg'] = np.where(df['home_team'] == 'Arsenal', df['home_xg'], df['away_xg'])


    #Aggregate by Season 
    seasonal = df.groupby('season').agg(
        total_goals = ('arsenal_goals', 'sum'),
        total_xg = ('arsenal_xg', 'sum')
        ).reset_index()

    #Calculate both xG difference and Efficiency
    seasonal['xg_difference'] = seasonal['total_goals'] - seasonal['total_xg']
    seasonal['efficiency'] = seasonal['total_goals'] / seasonal['total_xg']

    print(seasonal)


    #Plot 
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(seasonal['season'].astype(str), seasonal['total_goals'], marker='o', label='Actual Goals', color='red', linewidth=2)
    ax.plot(seasonal['season'].astype(str), seasonal['total_xg'], marker='o', label='xG', color='blue', linewidth=2, linestyle='--')

    ax.set_title("Arsenal: xG vs Actual Goals Scored (Last 5 Seasons)", fontsize=14)
    ax.set_xlabel("Season")
    ax.set_ylabel("Goals / xG")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("analysis/xg_vs_goals.png", bbox_inches='tight')
    plt.close()
    print("Q1 chart saved")


#Q2 Player progression
# -- Which player had improved (attacking wise) the most under Arteta over the last 5 seasons?

def q2_player_progression():
    #Pull Player Stats 
    df = pd.read_sql("""    
        SELECT player, season, minutes, xg, xa, xg_chain, xg_buildup
        FROM player_stats
    """, engine)


    #Calculate per 90
    df['90s'] = df['minutes'] / 90
    df['xg_per90'] = df['xg'] / df['90s']
    df['xa_per90'] = df['xa'] / df['90s']
    df['xg_xa_per90'] = df['xg_per90'] + df['xa_per90']

    #Filter to players with at least 900 minutes in a season 
    df = df[df['minutes'] >= 900] 


    #Keep players who have played in at least 2 of the 5 seasons 
    season_counts = df.groupby('player')['season'].count()
    valid_players = season_counts[season_counts >= 2].index
    df = df[df['player'].isin(valid_players)]

    #Calculate Trend slope for each player using numpy polyfit
    #Slope will show the difference in stats per season on avergage 
    def calculate_slope(player_df):
        #convert seasons into simple numbers for the calculation 
        seasons = list(range(len(player_df)))
        values = player_df['xg_xa_per90'].values 
        #np.polyfit(x, y, 1) fits a straight line 
        slope = np.polyfit(seasons, values, 1)[0]
        return slope
    

    #Apply slope calculation to each player's data 
    slopes = df.groupby('player').apply(calculate_slope, include_groups=False).reset_index()
    slopes.columns = ['player', 'improvement_slope']

    #Sort by slope so biggest improvers are at the top 
    slopes = slopes.sort_values('improvement_slope', ascending=False)

    print(slopes)


    #Plot - show top 10 players who improved the most and bottom 5 players for context 
    top_10 = slopes.head(10)
    bottom_5 = slopes.tail(5)
    plot_data = pd.concat([top_10, bottom_5]).sort_values('improvement_slope')

    fig, ax = plt.subplots(figsize=(12, 8))


    #Colour green for improvement, red for declining 
    colors = ['green' if x > 0 else 'red' for x in plot_data['improvement_slope']]

    ax.barh(plot_data['player'], plot_data['improvement_slope'], color=colors)

    ax.axvline(x=0, color='black', linewidth=1)
    ax.set_title("Arsenal: Player Attacking Progression Trend Under Arteta\n(xG + xA per 90, slope across all seasons)", fontsize=14)
    ax.set_xlabel("Improvement Slope (positive = consistently improving)")
    ax.set_ylabel("Player")
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig("analysis/q2_player_progression.png", bbox_inches='tight')
    plt.close()
    print("Q2 chart saved")





def q3_pressing_vs_points():
    import plotly.express as px
    import plotly.graph_objects as go

    df = pd.read_sql("""
        SELECT season, home_team, away_team, home_ppda, away_ppda, home_points, away_points
        FROM understat_team_stats
    """, engine)

    big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester United', 'Tottenham']

    home = df[df['home_team'].isin(big_6)][['season', 'home_team', 'home_ppda', 'home_points']].copy()
    home.columns = ['season', 'team', 'ppda', 'points']

    away = df[df['away_team'].isin(big_6)][['season', 'away_team', 'away_ppda', 'away_points']].copy()
    away.columns = ['season', 'team', 'ppda', 'points']

    combined = pd.concat([home, away])

    seasonal = combined.groupby(['team', 'season']).agg(
        avg_ppda=('ppda', 'mean'),
        total_points=('points', 'sum')
    ).reset_index()

    seasonal['season_str'] = seasonal['season'].astype(str)

    colors = {
        'Arsenal': '#EF0107',
        'Chelsea': '#034694',
        'Liverpool': '#00B2A9',
        'Manchester City': '#6CABDD',
        'Manchester United': '#DA291C',
        'Tottenham': '#132257'
    }

    fig = go.Figure()

    for team in big_6:
        team_data = seasonal[seasonal['team'] == team]
        fig.add_trace(go.Scatter(
            x=team_data['avg_ppda'],
            y=team_data['total_points'],
            mode='markers',
            name=team,
            marker=dict(
                size=12,
                color=colors[team],
                line=dict(color='black', width=1)
            ),
            # This is what shows when you hover over a point
            hovertemplate=(
                f"<b>{team}</b><br>" +
                "Season: %{customdata}<br>" +
                "PPDA: %{x:.2f}<br>" +
                "Points: %{y}<br>" +
                "<extra></extra>"
            ),
            customdata=team_data['season_str']
        ))

    fig.update_layout(
        title="Pressing Intensity vs League Points — Top 6 (Last 5 Seasons)",
        xaxis_title="Average PPDA (lower = more pressing →)",
        yaxis_title="Total Points",
        xaxis=dict(autorange='reversed'),  # flip x axis so lower PPDA is on right
        width=1000,
        height=700,
        legend=dict(x=1.02, y=1),
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey')

    # Save as interactive HTML file
    fig.write_html("analysis/q3_pressing_vs_points.html")

    # Also save as static PNG for README
    fig.write_image("analysis/q3_pressing_vs_points.png")

    print("Q3 chart saved")








#Q4 Arsenal defensive progression over the last 5 seasons 
# -- Has Arsenal's improvement in clean sheets been driven by genuinely conceding fewer quality chances (lower xG conceded), or by outperforming their xG conceded (potentially fortune)?
    

def q4_defensive_stats():
    df = pd.read_sql(""" 
        SELECT season, home_team, away_team, home_xg, away_xg, home_goals, away_goals
        FROM understat_team_stats
        WHERE home_team = 'Arsenal' OR away_team = 'Arsenal'
    """, engine)


    #Unified Arsenal conceded and opponent xG columns 
    df['goals_conceded'] = np.where(
        df['home_team'] == 'Arsenal',
        df['away_goals'],
        df['home_goals']
    )
    df['xg_conceded'] = np.where(
        df['home_team'] == 'Arsenal',
        df['away_xg'],
        df['home_xg']
    )


    #Flag Clean Sheets 
    df['clean_sheet'] = (df['goals_conceded'] == 0).astype(int)

    # Aggregate by season 
    seasonal = df.groupby('season').agg(
        total_goals_conceded=('goals_conceded', 'sum'),
        total_xg_conceded=('xg_conceded', 'sum'),
        clean_sheets=('clean_sheet', 'sum'),
        matches=('goals_conceded', 'count')
    ).reset_index()


    # Negative = conceded fewer goals than xG suggested 
    # Positive = conceded more goals than xG suggested 
    seasonal['xg_difference'] = seasonal['total_goals_conceded'] - seasonal['total_xg_conceded']

    print(seasonal)

    #Chart 1 xG conceded vs actual goals conceded
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(seasonal['season'].astype(str), seasonal['total_goals_conceded'],
            marker='o', label='Goals Conceded', color='red', linewidth=2)
    ax.plot(seasonal['season'].astype(str), seasonal['total_xg_conceded'],
            marker='o', label='xG Conceded', color='blue', linewidth=2, linestyle='--')

    ax.set_title("Arsenal: xG Conceded vs Actual Goals Conceded\n(has defensive improvement been structural or fortunate?)", fontsize=12)
    ax.set_xlabel("Season")
    ax.set_ylabel("Goals / xG")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("analysis/q4_xg_vs_goals_conceded.png", bbox_inches='tight')
    plt.close()


    #Chart 2 Clean Sheets per Season 
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(seasonal['season'].astype(str), seasonal['clean_sheets'], color='#EF0107')

    #Add value labels on top of each bar
    for bar, val in zip(bars, seasonal['clean_sheets']):
        ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            str(int(val)),
            ha='center', fontsize=11, fontweight='bold')

    ax.set_title("Arsenal: Clean Sheets per Season (Last 5 Seasons)", fontsize=13)
    ax.set_xlabel("Season")
    ax.set_ylabel("Clean Sheets")
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig("analysis/q4_clean_sheets.png", bbox_inches='tight')
    plt.close()

    # Chart 3 - Goals conceded vs xG conceded difference
    # Neutral framing — not good or bad, just variance
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(seasonal['season'].astype(str), seasonal['xg_difference'],
        marker='o', color='#EF0107', linewidth=2, markersize=8)

    # Reference line at 0
    ax.axhline(y=0, color='black', linewidth=1, linestyle='--', alpha=0.5)

    # Shade area below 0 in light green to show consistent underperformance
    ax.fill_between(seasonal['season'].astype(str),
                seasonal['xg_difference'],
                0,
                alpha=0.2,
                color='green',
                label='Conceded fewer than xG')

    ax.set_title("Arsenal: Goals Conceded vs xG Conceded Difference\n(negative = conceded fewer goals than chances allowed suggest)", fontsize=11)
    ax.set_xlabel("Season")
    ax.set_ylabel("Goals Conceded - xG Conceded")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("analysis/q4_xg_difference.png", bbox_inches='tight')
    plt.close()
    print("Q4 charts saved")






#Q5 - Which Arsenal players contribute most to build up play over the seasons

def q5_buildup_contribution():

    df = pd.read_sql(""" 
        SELECT player, season, minutes, xg_chain, xg_buildup
        FROM player_stats
        WHERE minutes >= 900
    """, engine)

    # Calculate per 90 to normalise for playing time
    df['90s'] = df['minutes'] / 90
    df['xg_chain_per90'] = df['xg_chain'] / df['90s']
    df['xg_buildup_per90'] = df['xg_buildup'] / df['90s']


    #Average Across all seasons each player appeared in
    player_avg = df.groupby('player').agg(
        avg_xg_chain_per90=('xg_chain_per90', 'mean'),
        avg_xg_buildup_per90=('xg_buildup_per90', 'mean'),
        seasons=('season', 'count')
    ).reset_index()

    # Sort by xg_chain and take top 12
    player_avg = player_avg.sort_values(
    ['seasons', 'avg_xg_chain_per90'], 
    ascending=[False, False]
    ).head(12)
    player_avg = player_avg[player_avg['seasons'] >= 2]

    print(player_avg)


    #Chart - xG Chain vs xG Buildup per 90 
    # -- shows total invlvement vs pure buildup contribution
    fig, ax = plt.subplots(figsize=(12, 7))

    x = range(len(player_avg))
    width = 0.35

    bars1 = ax.bar([i - width/2 for i in x], player_avg['avg_xg_chain_per90'],
                   width, label='xG Chain per 90', color='#EF0107', alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], player_avg['avg_xg_buildup_per90'],
                   width, label='xG Buildup per 90', color='#063672', alpha=0.8)
    

    ax.set_title("Arsenal: Who Drives the Attack?\nxG Chain (total attacking involvement) vs xG Buildup (early build-up contribution) per 90 — Last 5 Seasons\n *Only seasons with 900+ mins played included", fontsize=12)
    ax.set_xlabel("Player")
    ax.set_ylabel("Per 90 Minutes")
    ax.set_xticks(list(x))
    ax.set_xticklabels(player_avg['player'], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig("analysis/q5_buildup_contribution.png", bbox_inches='tight')
    plt.close()
    print("Q5 charts saved")


#Run Code
if __name__ == "__main__":
    try:
        print("Running Q1...")
        q1_xg_vs_goals()
    except Exception as e:
        print(f"Q1 failed: {e}")

    try:
        print("Running Q2...")
        q2_player_progression()
    except Exception as e:
        print(f"Q2 failed: {e}")
    
    try:
        print("Running Q3...")
        q3_pressing_vs_points()
    except Exception as e:
        print(f"Q3 failed: {e}")

    try:
        print("Running Q4...")
        q4_defensive_stats()
    except Exception as e:
        print(f"Q4 failed: {e}")

    try:
        print("Running Q5...")
        q5_buildup_contribution()
    except Exception as e:
        print(f"Q5 Failed: {e}")

    