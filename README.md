# Counter Strike 2 Predictor 

To use the predictor, simply run in the command:
* python predict_match.py
Then, you will see a pop-up window in which you can enter the match-id for the match you wish to predict, and then it will compute the probability of team 1 winning. Please note that this can sometimes take minutes to compute (from scraping the match stats), it may also fail to compute due to missing information about the match or failure to parse the web page. You may also need to download the required packages. Below shows how you can create a virtual environment and install the requirements.

# Creating a venv

First you need to create a virtual environment and download the required packages.

* py -m venv venv
If on windows

* . venv/Scripts/activate
Unix

* venv/Bin/activate
Now you download the required packages

* pip install -r requirements.txt

# Reproducing Results
This project is designed to be entirely reproducible, from data collection to model selection. In the src/data_collection folder can be found scripts for collecting/ scraping data from the website hltv.org and it saves the data in csv files that can be found in data/raw. These scripts can take a very long time to finish, especially 'get_all_data.py' can take many hours and sometimes fails due to cloudfare blocking your web connection. It is recommended to use the already collected datasets, but if you wish to collect the data yourself, the function is designed to save every page of results as it goes, and you can adjust the loop to start again where it broke. To run these scripts, they must be run in module mode in console;

* python -m src.data_collection.get_all_data

Here is a breakdown of the different data collected:
* 'team1' and 'team2' - The names of the teams
* 'match_type' - Whether the match was a Best of 1 (BO1), Best of 3 (BO3), or Best of 5 (BO5). Games in CS2 consist of a number of different maps being played (1,3 or 5) and the winner is the first to win 1, 2, or 3 maps respectively
* 'match_stage' - What stage of the tournament was this match played; Group Stage (GS), Quarter Final (QF), Semi Final (SF), Grand Final (GF), or other (nan)
* player{i}_id - A unique id that identifies the player
* player{i}_rating - A players past 3 month average '2.0 Rating', a score that indicate how well a player performed devised by hltv.org
* player{i}_kd - A players past 3 month average Kills-Deaths ratio
We should also note that players 0 to 4 are Team 1 and 5 to 9 are Team 2 and these players are ordered by their rating.

The data cleaning functions can just be run as normal and takes the data from data/raw and creates tidy and usable dataframes stored as csv files in data/clean. The model selection and training have been done in notebooks, which can be found in src/model_notebooks, to allow users to easily tinker and experiment with different model designs. These notebooks are self running, so one could click run all to recreate results (results for neural networks will be slightly different due to randomness in training using keras api). The preferred models are saved in outputs/models to be used later for prediction, the neural network model is quite large ~0.8MB and so requires Git LFS to upload to GitHub. 

To test if the 'predict_match_outcome.py' function is working properly you can use the test script by running it as module as follows:
* python -m tests.predict_match_test
But please note that if you have changed the models and saved them, then the probability you compute for the matches will be different, resulting in a failed test. You can either update the probability or choose not to run that test. The predict function can sometimes fail, as mentioned above, when certain information about a team is missing. Examples of when this might happen are when a team is using a 'stand-in', and so is missing information about that player on the team stats page, or when the team is new and so there is no current team ranking for them.

# hltv-api

For the data collection, I have used this open source hltv-api as a base and have developed additional functionality for this package. Many thanks to the creator and maintainers of this package, which can be found here: https://github.com/SocksPls/hltv-api . Here is a brief overview of the additional functionality I have provided;

* Fixed cloudfare issues by looping for requests and creating additional get_parsed_page_matches which uses a different referer
* Added get_results_by_event - a function that gets the basic match info and outcomes for a whole event (by event id)
* Added get_event_team_rankings - a function that gets the rankings of each team at the time of the event
* Added get_match_result_stats - a fucntion that gets further information about a match
* Added get_past_player_stats_for_match - a function that gathers the past 3 month performance stats for each player in a match

A more in-depth look at these functions and the changes I have made can be found on my branch of the project, which can be found here: https://github.com/JoeMCodes/hltv-api