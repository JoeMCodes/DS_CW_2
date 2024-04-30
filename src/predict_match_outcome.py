from hltv_api import main as hltv
import pandas as pd
import numpy as np
import joblib
import sklearn as sk
from tensorflow.keras.models import load_model
from ipywidgets import interact

log_reg = joblib.load('outputs/models/log_reg.pkl')
nn_num = load_model('outputs/models/nn_numeric_input.h5')


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
    try:
        ## Gathered data for the match and extract the predictors
        match_stats = hltv.get_match_result_stats(match_id)
        past_player_stats = hltv.get_past_player_stats_for_match(match_id)

        df_match_stats = pd.DataFrame([match_stats])

    except Exception as e: ## Catch other exceptions
        return f'Unknown Error Occurred: {e}'
    
    df = df_match_stats[['match-id', 'match_type', 'match_stage', 'team1_Ranking', 'team2_Ranking']]

    df_past_player_stats = pd.DataFrame([past_player_stats])
    df = pd.merge(df, df_past_player_stats, on='match-id', how = 'inner') ## combine dataframes
    
    X_numerical = df[numerical_features]
    X_numerical = X_numerical.apply(pd.to_numeric)

    if X_numerical.isna().any().any(): ## Handle error when data is missing
        return 'Cannot predict this match due to missing values'

    try:
        ## Predict Probabilities from each model
        log_reg_pred = log_reg.predict_proba(X_numerical)[0][1]
        nn_pred = nn_num.predict(X_numerical.to_numpy().reshape(1,-1))
        nn_prob = (np.exp(nn_pred)/(1+np.exp(nn_pred))).squeeze()

        outcome_pred = 0.9*log_reg_pred + 0.1*nn_prob ## Combine probs via weighting scheme found in 'weighted_model.ipynb'

        return f'Predicted Prob of Team 1 winning is {outcome_pred}'
    except:
        return 'Issue in Calculating Probabilities'
