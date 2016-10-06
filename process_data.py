import pandas as pd
import numpy as np
#determine whether a shot recorded in the play by play is a corner 3

def IsItACorner3(pbp_event, Shot_summary):

	#Parse play by play string to grab important info
	Game_id=np.int64(pbp_event['Game_id'])

	pbp_seconds=pbp_event['PC_Time']
	pbp_seconds=(int(pbp_seconds)/10)
	pbp_period=np.int64(pbp_event['Period'])
	#create upper and lower bound for time comparison
	upper = pbp_seconds+2
	lower = pbp_seconds-2

	#Create Conditions to filter through shot summary
	games = Shot_summary['GAME_ID'] == Game_id
	periods = Shot_summary['PERIOD'] == pbp_period
	lowers = Shot_summary['GAME_CLOCK'] > lower
	uppers = Shot_summary['GAME_CLOCK'] < upper

	#determine if a corner 3 can be linked to the play by play shot
	corner_three = Shot_summary[games & periods & lowers & uppers]
	#If there is a corner 3 linked, return True
	return (not corner_three.empty)

def isFastbreak(pbp_file, event, index):
	"""
	This function checks if a fast break has happened given the shot data and
	the plays happening immediatedly after it. Checks every consecutive event
	if a shot or foul lead to free throws has happened until a change of
	possesion or end of the set of events

	Input:
	plays -> list of strings of the play by play data
	line  -> row of the play by play data of the shot

	Output:
	boolean
	"""

	startTime = event["PC_Time"]
	period = event["Period"]
	gameId = event['Game_id']
	description = str(event["Description"])
	shootingTeam = description[description.find("[")+1:description.find("]")]

	nextLine = pbp_file.iloc[index+1]

	while((startTime - nextLine["PC_Time"] < 70) and (startTime - nextLine["PC_Time"] > 0) and \
	(period == nextLine["Period"]) and (gameId == nextLine['Game_id'])):
		if shootingTeam in nextLine["Description"]:
			if ("Foul" not in nextLine["Description"]):
				return False
		else:
			if ("Shot" in nextLine["Description"]) or ("Free Throw" in nextLine["Description"]):
				return True
		try:
			nextLine = pbp_file.iloc[index+1]
		except IndexError:
			break
	return False

def IsMissedShot(line):
	'''
	Checks if a shot attempt has missed

	Input:
	line -> string of the play by play date of the shot

	Output:
	boolean
	'''
	return ("Missed" in str(line["Description"]))

def IsThree(line):
	"""
	Checks if a shot attempt is a three pointer

	Input:
	line -> string of the play by play date of the shot

	Output:
	boolean
	"""
	return ("3pt Shot" in str(line["Description"]))

def IsTwo(line):
	'''
	Checks if a shot attempt is a two pointer

	Input:
	line -> string of the play by play date of the shot

	Output:
	boolean
	'''
	return (("Shot" in str(line["Description"])) and ("3pt" not in str(line["Description"])))

def main(year):
	shot_file = None
	pbp_file = None
	if year == 2014:
		shot_file = "Hackathon_sv_shot_summary_2014-15.csv"
		pbp_file = "Hackathon_play_by_play_2014-15.csv"
	elif year == 2015:
		shot_file = "Hackathon_sv_shot_summary_2015-16.csv"
		pbp_file = "Hackathon_play_by_play_2015-16.csv"
	else:
		print("Invalid year! Try 2014 or 2015.")
		return;
	#count of how many fastbreaks occur from corner threes and twos
	Shot_summary=pd.read_csv(shot_file)
	IsAThree= Shot_summary["PT_VALUE"] == 3
	lower_dist=Shot_summary['SHOT_DIST'] > 22
	upper_dist=Shot_summary['SHOT_DIST'] < 24.5
	Shot_summary = Shot_summary[IsAThree & lower_dist & upper_dist]

	TotalMissedShots = 0;
	TotalMissedTwos = 0;
	TotalMissedThrees = 0;
	TotalMissedCornerThrees = 0;
	MissedTwosFastBreak = 0;
	MissedThreeFastBreak = 0;
	MissedCornerThreeFastBreak = 0;

	pbp = pd.read_csv(pbp_file);
	for index, row in pbp.iterrows():
		if(IsMissedShot(row)):
			TotalMissedShots += 1
			fastBreak = isFastbreak(pbp, row, index);
			if(IsTwo(row)):
				TotalMissedTwos += 1
				MissedTwosFastBreak += fastBreak
			if(IsThree(row)):
				TotalMissedThrees += 1
				MissedThreeFastBreak += fastBreak
			if(IsItACorner3(row, Shot_summary)):
				TotalMissedCornerThrees += 1
				MissedCornerThreeFastBreak += fastBreak

	print("Missed shots in " + str(year) + ": " + str(TotalMissedShots))
	print("Missed two pointers in "  + str(year) + ": " + str(TotalMissedTwos))
	print("Missed three pointers in " + str(year) + ": " + str(TotalMissedThrees))
	print("Missed corner threes in " + str(year) + ": " + str(TotalMissedCornerThrees))
	print("Fast Breaks from Missed Twos in " + str(year) + ": " + str(MissedTwosFastBreak))
	print("Fast Breaks from Missed Threes in " + str(year) +": " + str(MissedThreeFastBreak))
	print("Fast Breaks from Missed Corner Threes in " + str(year) +": " + str(MissedCornerThreeFastBreak))

	Output = open("output_" + str(year) + ".txt", "w+");
	#Print out the data
	Output.write("Missed shots in " + str(year) + ": " + str(TotalMissedShots))
	Output.write("Missed two pointers in "  + str(year) + ": " + str(TotalMissedTwos))
	Output.write("Missed three pointers in " + str(year) + ": " + str(TotalMissedThrees))
	Output.write("Missed corner threes in " + str(year) + ": " + str(TotalMissedCornerThrees))
	Output.write("Fast Breaks from Missed Twos in " + str(year) + ": " + str(MissedTwosFastBreak))
	Output.write("Fast Breaks from Missed Threes in " + str(year) +": " + str(MissedThreeFastBreak))
	Output.write("Fast Breaks from Missed Corner Threes in " + str(year) +": " + str(MissedCornerThreeFastBreak))

	Output.close()

	print("done, check files");

if __name__ == '__main__':
	main(2014)
	main(2015)