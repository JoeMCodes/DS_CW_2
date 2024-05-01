import src.predict_match_outcome as pred

def test_working():
    actual_output = pred.predict_match_outcome(2371505)
    expected_output = 'Predicted Prob of Team 1 winning is 0.7048109114120522'
    assert actual_output == expected_output, f"Expected: {expected_output}, Actual: {actual_output}"

def test_missing_players():
    actual_output = pred.predict_match_outcome(2371508)
    expected_output = 'Cannot predict this match due to missing values'
    assert actual_output == expected_output, f"Expected: {expected_output}, Actual: {actual_output}"

def test_missing_team_ranking():
    actual_output = pred.predict_match_outcome(2371509)
    expected_output = "Unknown Error Occurred: 'NoneType' object has no attribute 'contents'"
    assert actual_output == expected_output, f"Expected: {expected_output}, Actual: {actual_output}"

test_working()

test_missing_players()

test_missing_team_ranking()

print('Tests Passed Successfully')
    