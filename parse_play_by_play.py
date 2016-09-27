#Note: this takes up a lot of memory so try to run this on a clean console and restart after you're done.
import pandas as pd

# These are the headers we want
desired_fields = ['Event_Msg_Type', 'Game_id',  'Event_Num', 'PC_Time', 'Home_PTS', 'Visitor_PTS', 'Description', 'Event_Description']
# These are all the headers
headers = ['Event_Msg_Type', 'Game_id', 'Event_Num', 'Period', 'Home_PTS', 'Visitor_PTS',\
 'Home_Team_id', 'Away_Team_id', 'PC_Time', 'WC_Time', 'SC_Time', 'Date_EST', 'Home Team',\
'Away Team', 'Description', 'Event_Description']
 
# Get the play by play data for 2014-2015
play_by_play_2014 = pd.read_csv('data/Hackathon_play_by_play.txt',sep = ' ', names = headers, skiprows= 4630542, nrows= 608029)
# Get only the coulmns we want
parsed_play_by_play_2014 = play_by_play_2014[desired_fields]
# Save to a csv file for later processing
parsed_play_by_play_2014.to_csv('data/Hackathon_play_by_play_2014_2015.csv', header = desired_fields)

# Get the play by play data for 2016-2016
play_by_play_2015 = pd.read_csv('data/Hackathon_play_by_play.txt',sep = ' ', names = headers, skiprows= 5238572, nrows= 615501)
# Get only the coulmns we want
parsed_play_by_play_2015 = play_by_play_2015[desired_fields]
# Save to a csv file for later processing
parsed_play_by_play_2015.to_csv('data/Hackathon_play_by_play_2015_2016.csv', header = desired_fields)

