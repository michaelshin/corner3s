import pandas as pd
import numpy as np
#determine whether a shot recorded in the play by play is a corner 3

def IsItACorner3(pbp_event, Shot_summary):
    
    #load shot summary data to link play by play to
    
    
    #Parse play by play string to grab important info
    split_event=pbp_event.split(" ")
    Game_id=np.int64(split_event[2])   
    pbp_seconds=split_event[9]
    pbp_seconds=(int(pbp_seconds)/10)
    pbp_period=np.int64(split_event[4])
    
    #create upper and lower bound for time comparison    
    upper=pbp_seconds+2
    lower=pbp_seconds-2
    
    #Create Conditions to filyter through shot summary
    games = Shot_summary['GAME_ID']==Game_id 
    periods = Shot_summary["PERIOD"]==pbp_period 
    lowers = Shot_summary["GAME_CLOCK"]>lower
    uppers = Shot_summary["GAME_CLOCK"] < upper
    lower_dist=Shot_summary["SHOT_DIST"]>22
    upper_dist=Shot_summary["SHOT_DIST"]<24.5
    #pt_value=Shot_summary["PT_VALUE"]==3
    
   #determine if a corner 3 can be linked to the play by play shot
    corner_three= Shot_summary[games & periods & lowers & uppers & lower_dist \
    &  upper_dist] #& pt_value]

     
    #If there is a corner 3 linked, return True, else False
    if (len(corner_three.index)>0):
    	#print(pbp_event[0] + " " + )
        return True
    else:
        return False




def readForward(fileReader, event):
	"""	
	return an array of strings that represent the next 7 seconds of play information
	it will also seek backward the total number of bytes it has read forward, so that the original iterator can
	continue.

	fileReader : reference to file
	event: string that triggered the readForward call

	output:
	all the recorded events into an array
	"""	

	result = []
	start = getTime(event);
	line = fileReader.readline();
	numBytes = len(line);

	while(line != "" and start - getTime(line) < 70 and start - getTime(line) > 0): #while current line is within 7 seconds
		line = fileReader.readline();
		numBytes += len(line);
		line = line.replace("\n", "");
		result.append(line);

	numBytes = numBytes * -1;
	fileReader.seek(numBytes, 1);

	return result;

def getTime(PbpRow):
	#return 7200 indexed time from the play by play file.
	return int(PbpRow.split(" ")[9]);

def isBreakAway(plays, shot):
	'''
	This function checks if a fast break has happened given the shot data and 
	the plays happening immediatedly after it. Checks every consecutive event
	if a shot or foul lead to free throws has happened until a change of 
	possesion or end of the set of events
	
	Input:
	plays -> list of strings of the play by play data
	shot -> string of the play by play data of the shot
	
	Output:
	boolean   
	'''
	shootingTeam = shot[shot.find("[")+1:shot.find("]")]
	for event in plays:
		if shootingTeam in event:
			if ("Foul" not in event):
				break
		else:
			if ("Shot" in event) or ("Free Throw" in event):
				return True
	return False

def IsMissedShot(line):
	'''
	Checks if a shot attempt has missed
	
	Input:
	line -> string of the play by play date of the shot
	
	Output:
	boolean
	'''
	return ("Missed Shot" in line)

def IsThree(line):
	"""
		see below
	"""
	return ("Shot" in line) and ("3pt" in line)

def IsTwo(line):
	'''
	Checks if a shot attempt is a two pointer

	Input:
	line -> string of the play by play date of the shot
	
	Output:
	boolean
	'''

	return (("Shot" in line) and ("3pt" not in line))

def main():
	#count of how many fastbreaks occur from corner threes and twos
	Shot_summary=pd.read_csv("Hackathon_sv_shot_summary_2014-15.csv")
	IsAThree= Shot_summary["PT_VALUE"] == 3
	Shot_summary = Shot_summary[IsAThree]

	TotalLines = 0;
	MissedCornerThrees = 0;
	MissedTwos = 0;
	CornerThreeFastBreakCount = 0;
	TwosFastBreakCount = 0;

	#output file with events that were relevant to the counts.

	#2014 values
	CornerThreeFile2014 = open("cornerThree14.txt",'w+')
	ThreeFile2014 = open("Three14.txt", "w+")
	TwosFile2014 = open("otherShots1415.txt", 'w+')

	TotalMissedShots2014 = 0;
	TotalMissedTwos2014 = 0;
	TotalMissedThrees2014 = 0;
	TotalMissedCornerThrees2014 = 0;
	MissedTwosFastBreak2014 = 0;
	MissedThreeFastBreak2014 = 0;
	MissedCornerThreeFastBreak2014 = 0;


	#2015 values
	CornerThreeFile2015 = open("cornerThree15.txt","w+")
	ThreeFile2015 = open("Three15.txt", "w+")
	TwosFile2015 = open("otherShots1415.txt", 'w+')
	TotalMissedShots2015 = 0;
	TotalMissedTwos2015 = 0;
	TotalMissedThrees2015 = 0;
	TotalMissedCornerThrees2015 = 0;
	MissedTwosFastBreak2015 = 0;
	MissedThreeFastBreak2015 = 0;
	MissedCornerThreeFastBreak2015 = 0;


	file = open("Hackathon_play_by_play2014on.txt", 'r')
	line = file.readline();
	while(line):
		line = file.readline();
		try:
			if(line.split(" ")[2][1:3] == '14'):		
				if(IsMissedShot(line)):
					TotalMissedShots2014 += 1;
					nextSevenSeconds = readForward(file, line);
					if(IsTwo(line)):
						#it's not a corner 3, add it to the other file
						TotalMissedTwos2014 += 1;
						MissedTwosFastBreak2014 += isBreakAway(nextSevenSeconds, line);
						TwosFile2014.write("|".join(nextSevenSeconds) + "\n")

					if(IsThree(line)):
						TotalMissedThrees2014 += 1;
						MissedThreeFastBreak2014 += isBreakAway(nextSevenSeconds, line);
						ThreeFile2014.write("|".join(nextSevenSeconds) + "\n")

					if(IsItACorner3(line, Shot_summary)):
						TotalMissedCornerThrees2014 += 1;
						MissedCornerThreeFastBreak2014+= isBreakAway(nextSevenSeconds, line);
						CornerThreeFile2014.write("|".join(nextSevenSeconds) + "\n")
			else:
				if(IsMissedShot(line)):
					TotalMissedShots2015 += 1;
					nextSevenSeconds = readForward(file, line);
					if(IsTwo(line)):
						#it's not a corner 3, add it to the other file
						TotalMissedTwos2015 += 1;
						MissedTwosFastBreak2015 += isBreakAway(nextSevenSeconds, line);
						TwosFile2015.write("|".join(nextSevenSeconds) + "\n")

					if(IsThree(line)):
						TotalMissedThrees2015 += 1;
						MissedThreeFastBreak2015 += isBreakAway(nextSevenSeconds, line);
						ThreeFile2015.write("|".join(nextSevenSeconds) + "\n")

					if(IsItACorner3(line, Shot_summary)):
						TotalMissedCornerThrees2015 += 1;
						MissedCornerThreeFastBreak2015+= isBreakAway(nextSevenSeconds, line);
						CornerThreeFile2015.write("|".join(nextSevenSeconds) + "\n")
		except IndexError:

			print(TotalMissedShots2014)
			print(TotalMissedTwos2014)
			print(TotalMissedThrees2014)
			print(TotalMissedCornerThrees2014)
			print(MissedTwosFastBreak2014)
			print(MissedThreeFastBreak2014)
			print(MissedCornerThreeFastBreak2014)

			print(TotalMissedShots2015)
			print(TotalMissedTwos2015)
			print(TotalMissedThrees2015)
			print(TotalMissedCornerThrees2015)
			print(MissedTwosFastBreak2015)
			print(MissedThreeFastBreak2015)
			print(MissedCornerThreeFastBreak2015)



			Output = open("output.txt", "w+");
			Output.write("Missed shots in 2014: " + str(TotalMissedShots2014))
			Output.write("Missed two pointers in 2014: " + str(TotalMissedTwos2014))
			Output.write("Missed three pointers in 2014: " + str(TotalMissedThrees2014))
			Output.write("Missed corner threes in 2014: " + str(TotalMissedCornerThrees2014))
			Output.write("Fast Breaks from Missed Twos in 2014: " + str(MissedTwosFastBreak2014))
			Output.write("Fast Breaks from Missed Threes in 2014: " + str(MissedThreeFastBreak2014))
			Output.write("Fast Breaks from Missed Corner Threes in 2014: " +str(MissedCornerThreeFastBreak2014))

			Output.write("\n");

			Output.write("Missed shots in 2015: " + str(TotalMissedShots2015))
			Output.write("Missed two pointers in 2015: " + str(TotalMissedTwos2015))
			Output.write("Missed three pointers in 2015: " + str(TotalMissedThrees2015))
			Output.write("Missed corner threes in 2015: " + str(TotalMissedCornerThrees2015))
			Output.write("Fast Breaks from Missed Twos in 2015: " + str(MissedTwosFastBreak2015))
			Output.write("Fast Breaks from Missed Threes in 2015: " + str(MissedThreeFastBreak2015))
			Output.write("Fast Breaks from Missed Corner Threes in 2015: " + str(MissedCornerThreeFastBreak2015))

			Output.close();


			CornerThreeFile2014.close()
			ThreeFile2014.close()
			TwosFile2014.close()
			CornerThreeFile2015.close()
			ThreeFile2015.close()
			TwosFile2015.close()
			CornerThreeFile.close();
			TwosFile.close()
			file.close();
			break
	print("done, check files");

main();


