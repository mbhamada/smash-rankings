#############################
# Challonge API for Smash 4 #
# ------------------------- #
# * Optimized for Python 3  #
#                           #
# Malachi Hamada            #
#############################

from trueskill import Rating, rate_1vs1
import challonge
import pickle
import string
import unicodedata

names = {} 
tournaments = []
options = "1) Add a tournament\n2) Get specific player data\n3) Rerun all data from scratch\n4) Exit"

##################
# ** FEATURES ** #
##################  

def update(name, scores, wins, tourneys):
	"""Retrieves a tournament by name (url) and updates the global scores and 
	   wins dictionaries with new tournament data.

	name:     The name of the tournament.
	scores:   A dictionary that maps the player's name to his/her TrueSkill Rating.
	wins:     A dictionary that maps the player's name to a list of players he/she has defeated.
	tourneys: A dictionary that maps the players name to a list of tournaments he/she has attended.
	"""
	tournament = challonge.tournaments.show(name)
	participants = challonge.participants.index(tournament["id"])
	matches = challonge.matches.index(tournament["id"])
	  
	# Add each player to the database.
	players = {}
	for p in participants:
		tag = p["name"]
		if tag in names.keys():
			tag = names[tag]
		players[p["id"]] = tag
		if tag not in wins.keys():
			wins[tag] = []
		if tag not in scores.keys():
			scores[tag] = Rating()
		if tag not in tourneys.keys():
			tourneys[tag] = []
		tourneys[tag].append(name)

	# Update the 'wins' dictionary.
	for m in matches:
		if m["winner-id"] == None: 
			pass
		else:
			winner = players[m["winner-id"]]
			loser = players[m["loser-id"]]
			wins[winner].append(loser)

	# Update the 'scores' dictionary.
	for w, ls in wins.items():
		for l in ls:
			new_r1, new_r2 = rate_1vs1(scores[w], scores[l])
			scores[w] = new_r1
			scores[l] = new_r2

	return (scores, wins, tourneys)

def add_tournament(name, scores, wins):
	"""Adds a new tournament to the database and updates the data.

	name:   The name of the tournament.
	scores: A dictionary that maps the player's name to his/her TrueSkill Rating.
	wins:   A dictionary that maps the player's name to a list of players he/she has defeated.
	"""
	scores, wins, tourneys = update(name, scores, wins, tourneys)
	serialize_data(scores, wins)
	write_data(scores, wins, tourneys)

def player_data(name):
	"""Retrieves data for a specific player. Statistics are shown first, player wins are shown next.

	name: The name of the player.
	"""
	# if len(scores) == 0:
	# 	get_data()


##########################
# ** HELPER FUNCTIONS ** # 
##########################

def write_data(scores, wins, tourneys):
	"""Takes data from the scores and wins dictionaries and writes it to two csv files.

	scores:   A dictionary that maps the player's name to his/her TrueSkill Rating.
	wins:     A dictionary that maps the player's name to a list of players he/she has defeated.
	tourneys: A dictionary that maps the players name to a list of tournaments he/she has attended.
	"""
	#Create a string array 'lines' that contains ranking information.
	lines = []
	for player in scores.keys():
	    mu = scores[player].mu
	    sig = scores[player].sigma
	    score = mu - 3 * sig
	    num_t = len(tourneys[player])
	    lines.append(player + "," + str(num_t) + "," + str(mu) + "," + str(sig) + "," + str(score))

	# Update the CSV file containing ranking information.    
	with open("stats/scores.csv", "w") as f:
		for item in lines:
		    f.write(item+"\n")

	# Update the CSV file containing player wins information.
	with open("stats/wins.csv","w") as f:
		for key, value in wins.items():
		    f.write(key + "," + str(len(value)))
		    for p in value:
		        f.write("," + p)
		    f.write("\n")

def serialize_data(scores, wins):
	"""Serializes the 'scores' and 'wins' dictionaries for later use.
	
	scores: A dictionary that maps the player's name to his/her TrueSkill Rating.
	wins:   A dictionary that maps the player's name to a list of players he/she has defeated.
	"""
	file = open("data/scores.pkl", "wb")
	pickle.dump(scores, file)
	file.close()

	file = open("data/wins.pkl", "wb")
	pickle.dump(wins, file)
	file.close() 

def get_data():
	"""Retrieves the serialized scores and wins dictionaries.
	"""
	file = open("data/scores.pkl","rb")
	scores = pickle.load(file)

	file = open("data/wins.pkl","rb")
	wins = pickle.load(file)

	return (scores, wins)

def get_credentials(func):
	"""Returns credentials as a tuple.
	"""
	cred = []
	with open("names/credentials.txt", "r") as f:
		for line in f:
			cred.append(line.rstrip('\n'))
	if len(cred) == 0:
		print("No Challonge credentials found.")
	else:
		return func(cred[0], cred[1])

def get_names():
	"""Creates the names dictionary and the tournaments list.
	"""
	with open("names/players.txt", "r") as f:
		for line in f:
			line = line.rstrip('\n')
			kv = line.split(' * ')
			names[kv[0]] = kv[1]

	with open("names/tournaments.txt", "r") as f:
		for line in f:
			tournaments.append(line.rstrip('\n'))

def re_run():
	"""A helper funciton for run_program created to help with recursion. 
	"""
	option = input("Would you like to do anything else? (y/n): ")
	if option == "y":
		run_program()
	elif option == "n":
		print("Done.")
		return
	else:
		print("Invalid option. Please try again.")
		re_run()

########################
# ** PROGRAM RUNNER ** #
######################## 	

def run_program():
	"""Can carry out several actions based upon the option (#) chosen:
	   1) Adds a new tournament to the database
	   2) Display the data for a specific player
	   3) Rerun the data for all tournaments from scratch 
	   4) Exit the program
	"""
	option_str = input("Choose an option: ")
	option = int(option_str)

	if option not in range(1, 5):
		print("Invalid option. Please try again.\n" + options)
		run_program()
	elif option == 1:
		tournament = input("Please enter a valid tournament url: ")
		print("Adding " + tournament + "...")
		add_tournament(tournament)
		print("Success.")
		re_run()
	elif option == 2:
		player = input("Please enter a valid player name: ")
		player_data(player)
		re_run()
	elif option == 3:
		print("Running...\nTournaments checked:")
		scores = {}
		wins = {}
		tourneys = {}
		for t in tournaments:
			scores, wins, tourneys = update(t, scores, wins, tourneys)
			print("* " + t)
		serialize_data(scores, wins)
		write_data(scores, wins, tourneys)
		re_run()
	else:
		print("Done.")
		return

##############
# ** MAIN ** #
############## 

# Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
get_credentials(challonge.set_credentials)
get_names()
print("What would you like to do?\n" + options)
run_program()
