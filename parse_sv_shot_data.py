#Note: this takes up a lot of memory so try to run this on a clean console and restart after you're done.
import pandas as pd

# These are the headers we want
desired_fields = ["GAME_ID", "SHOT_RESULT", "PERIOD", "GAME_CLOCK", "SHOT_DIST","PT_VALUE"]

# These are all the headers
headers = ["SEASON", "GAME_ID", "SV_GAME_ID", "GAME_DATE", "TEAM_ID", "SV_TEAM_ID", "SHOT_TAKER_TEAM",\
 "PERSON_ID", "SV_PLAYER_ID", "SHOT_RESULT", "PERIOD", "GAME_CLOCK", "WALL_CLOCK", "DRIBBLES", "SHOT_DIST",\
 "TOUCH_TIME", "CLOSE_DEF_PERSON_ID", "CLOSE_DEF_SV_PLAYER_ID", "CLOSE_DEF_DIST", "PT_VALUE", "PTS"]
 
# Get the parsed shot data data for 2014-2015
parsed_shot_data_2014 = pd.read_csv('data/Hackathon_sv_shot_summary_2014-15.txt',sep = ' ', usecols = desired_fields)
# Save to a csv file for later processing
parsed_shot_data_2014.to_csv('data/Hackathon_sv_shot_summary_2014-15.csv', header = desired_fields)

# Get the parsed shot data data for 2015-2016
parsed_shot_data_2015 = pd.read_csv('data/Hackathon_sv_shot_summary_2015-16.txt',sep = ' ', usecols = desired_fields)
# Save to a csv file for later processing
parsed_shot_data_2015.to_csv('data/Hackathon_sv_shot_summary_2015-16.csv', header = desired_fields)