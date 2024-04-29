from hltv_api import main as hltv
import pandas as pd
import joblib
import sklearn as sk
from ipywidgets import interact

log_reg = joblib.load('outputs/models/log_reg.pkl')

numerical_features = ['team1_Ranking', 'team2_Ranking']
for i in range(10):
    numerical_features.append(f'player{i}_rating')
    numerical_features.append(f'player{i}_kd')

def predict_match_outcome(match_id):
    '''
    input:
    match_id: str or int of the match to predict

    output: Predicted probabilities of teams winning
    '''
    match_stats = hltv.get_match_result_stats(match_id)
    past_player_stats = hltv.get_past_player_stats_for_match(match_id)

    df_match_stats = pd.DataFrame([match_stats])
    df = df_match_stats[['match-id', 'match_type', 'match_stage', 'team1_Ranking', 'team2_Ranking']]

    # df = pd.merge(df, df_match_stats, on='match-id', how = 'inner') ## combine dataframes

    df_past_player_stats = pd.DataFrame([past_player_stats])
    df = pd.merge(df, df_past_player_stats, on='match-id', how = 'inner') ## combine dataframes
    
    X_numerical = df[numerical_features]
    if X_numerical.isna().any().any():
        return 'Cannot predict this match due to missing values'

    outcome_pred = log_reg.predict_proba(X_numerical)[0][1]

    return f'Predicted Prob of Team 1 winning is {outcome_pred}'
