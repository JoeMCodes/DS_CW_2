import pandas as pd
import numpy as np

## Load dataframes 
df_all = pd.read_csv('data/raw/all_data_train.csv', index_col=False)

## Drop unused columns
df_all = df_all.drop(columns=["url", "event", "match-id", "date", "team1-id", "team2-id"])

## drop NA values
df_all = df_all.dropna()

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
df_all['match_stage'] = df_all['match_stage'].apply(convert_match_stage)
df_all['match_type'] = df_all['match_type'].apply(convert_match_type)

## Team Won column
df_all['team_1_won'] = np.int32(df_all['team1score']>df_all['team2score'])

df_all.to_csv('./data/clean/clean_data_all.csv', index=False)
