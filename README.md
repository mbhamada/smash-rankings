# Smash 4 Ranking System

A simple program I wrote for Smash at Berkeley used to rank and collect data on Smash 4 players.

## Built Using

* Python
* Challonge API
* TrueSkill Ranking System

## Getting Started

### Prerequisites

1. Create a new directory to store the api_smash4.py file
2. Create a folder titled "names" in this directory
3. In the names folder create three .txt files titled "credentials.txt", "players.txt", and "tournaments.txt"
4. In credentials.txt, type your Challonge key for the first line and Challonge password for the second line
5. players.txt is used for player tag conflicts i.e. if a player does not use consistent tags between any two tournaments. 
   For each conflict add a line with the incorrect tag followed by " * " followed by the prefered tag. See:
   ```playername * player name``` where "player name" is the prefered player tag
6. In tournaments.txt, for each line type the tournament Challonge id
7. Verify that you have no additional lines for the latter two files

### Running the program

Like any other Python program, simply move to the directory with the program and enter the following into the terminal:

```python api_smash4.py```

The program help you the rest of the way.
Data can be found in the "stats" folder.

## Features

I have three key features in mind for this program:

1. Add a new tournament and update the data
2. Display data for a specific player
3. Collect and rerun all player and tournament data from scratch

Features 1 and 2 will become available once I'm sure that feature 3 is stable.
More features planned for the future.

## Acknowledgements

Shoutouts to Smash at Berkeley, the premier club for the UC Berkeley Smash community.
