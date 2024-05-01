from hltv_api import main as hltv
import pandas as pd
import requests
from bs4 import BeautifulSoup

## gets list of recent (last 12 months) event id's for top tier tournaments (Defined as International LAN's with prize pool greater or equal to 100000$)
events_page = hltv.get_parsed_page('https://www.hltv.org/events/archive?startDate=2023-04-25&endDate=2024-04-25&eventType=INTLLAN&eventType=LOCALLAN&prizeMin=100000&prizeMax=2000000')

event_ids = []
for event in events_page.find_all('a', attrs={'class': 'a-reset small-event standard-box'}):
    event_id = event.get('href').split('/')[2]
    event_ids.append(event_id)


## Gets information and creates dataframe for each event
df_per_event = []
for id in event_ids[0:2]: ## the two latest tournaments wil be used a test dataset
    data = hltv.get_results_by_event(id) ## get all matches and outcome data for tournament
    df = pd.DataFrame(data)

    ## This gets further match data for each match
    match_ids = df['match-id']
    match_stats = []
    past_player_stats = []
    for match_id in match_ids:
        match_stats.append(hltv.get_match_result_stats(match_id))
        past_player_stats.append(hltv.get_past_player_stats_for_match(match_id))

    df_match_stats = pd.DataFrame(match_stats)
    df_match_stats = df_match_stats[['match-id', 'match_type', 'match_stage']] ## Get relevant information from match stats
    df = pd.merge(df, df_match_stats, on='match-id', how = 'inner') ## combine dataframes

    df_past_player_stats = pd.DataFrame(past_player_stats)
    df = pd.merge(df, df_past_player_stats, on='match-id', how = 'inner') ## combine dataframes
    
    event_team_rankings = hltv.get_event_team_rankings(id) ## gets team rankings at time of the event
    team_rankings_df = pd.DataFrame(list(event_team_rankings.items()), columns=['Team', 'Ranking'])

    ## Add team rankings to dataframe
    df = pd.merge(df, team_rankings_df, left_on='team1', right_on='Team', how = 'left')
    df = df.rename(columns={'Ranking': 'team1_Ranking'}).drop(columns=['Team'])
    df = pd.merge(df, team_rankings_df, left_on='team2', right_on='Team', how = 'left')
    df = df.rename(columns={'Ranking': 'team2_Ranking'}).drop(columns=['Team'])

    df_per_event.append(df)

df = pd.concat(df_per_event) ## Combines all dataframes together

df.to_csv('./data/raw/tier_1_data_test.csv', index=False)

print('Test Data Collected!')


## Repeat the above for the train data

## Gets information and creates dataframe for each event
df_per_event = []
for id in event_ids[2:]:
    data = hltv.get_results_by_event(id) ## get all matches and outcome data for tournament
    df = pd.DataFrame(data)

    ## This gets further match data for each match
    match_ids = df['match-id']
    match_stats = []
    past_player_stats = []
    for match_id in match_ids:
        match_stats.append(hltv.get_match_result_stats(match_id))
        past_player_stats.append(hltv.get_past_player_stats_for_match(match_id))

    df_match_stats = pd.DataFrame(match_stats)
    df_match_stats = df_match_stats[['match-id', 'match_type', 'match_stage']]
    df = pd.merge(df, df_match_stats, on='match-id', how = 'inner') ## combine dataframes

    df_past_player_stats = pd.DataFrame(past_player_stats)
    df = pd.merge(df, df_past_player_stats, on='match-id', how = 'inner') ## combine dataframes
    
    event_team_rankings = hltv.get_event_team_rankings(id) ## gets team rankings at time of the event
    team_rankings_df = pd.DataFrame(list(event_team_rankings.items()), columns=['Team', 'Ranking'])

    ## Add team rankings to dataframe
    df = pd.merge(df, team_rankings_df, left_on='team1', right_on='Team', how = 'left')
    df = df.rename(columns={'Ranking': 'team1_Ranking'}).drop(columns=['Team'])
    df = pd.merge(df, team_rankings_df, left_on='team2', right_on='Team', how = 'left')
    df = df.rename(columns={'Ranking': 'team2_Ranking'}).drop(columns=['Team'])

    df_per_event.append(df)

df = pd.concat(df_per_event) ## Combines all dataframes together

df.to_csv('./data/raw/tier_1_data_train.csv', index=False)

print('Train Data Collected!')