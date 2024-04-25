import pandas as pd
import numpy as np

## Load dataframes 
df_train = pd.read_csv('data/raw/tier_1_data_train.csv', index_col=False)
df_test = pd.read_csv('data/raw/tier_1_data_test.csv', index_col=False)

## Drop unused columns
df_train = df_train.drop(columns=["url", "event", "match-id", "date", "team1-id", "team2-id"])
df_test = df_test.drop(columns=["url", "event", "match-id", "date", "team1-id", "team2-id"])

## Helper Functions To process string data
def convert_match_stage(ms_str):
    '''
    input: 
        ms_str: string containing information about match stage

    output: a string containing what stage of the tournament the match is
    '''
    if 'group' in ms_str.lower():
        return 'G'
    elif 'quarter' in ms_str.lower():
        return 'QF'
    elif 'semi' in ms_str.lower():
        return 'SF'
    elif 'grand' in ms_str.lower():
        return 'GF'
    else:
        return 'NA'

def convert_match_type(mt_str):
    '''
    input: 
        mt_str: string containing information about match type

    output: a string containing whether the match is a BO1, BO3, or BO5
    '''
    if '1' in mt_str.lower():
        return 'BO1'
    elif '3' in mt_str.lower():
        return 'BO3'
    elif '5' in mt_str.lower():
        return 'BO5'
    else:
        return 'NA'
    
## process string data for match stage and type
df_train['match_stage'] = df_train['match_stage'].apply(convert_match_stage)
df_train['match_type'] = df_train['match_type'].apply(convert_match_type)

df_test['match_stage'] = df_test['match_stage'].apply(convert_match_stage)
df_test['match_type'] = df_test['match_type'].apply(convert_match_type)

## Team Won column
df_train['team_1_won'] = np.int32(df_train['team1score']>df_train['team2score'])
df_test['team_1_won'] = np.int32(df_test['team1score']>df_test['team2score'])

df_train.to_csv('./data/clean/clean_data_train.csv', index=False)
df_test.to_csv('./data/clean/clean_data_test.csv', index=False)
