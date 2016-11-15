import random

board_state = []

def pick_random_card():
	rank = random.choice( ('A','2','3','4','5','6','7','8','9','T','J','Q','K') )
	suit = random.choice( ('C','D','H','S') )
	card = rank + suit
	return card

def update_board_state(board_state,flag,current):
	#We can also try using the global board state directly without passing it each time.
	#global board_state

	#If the card is valid, append it at the end of the board state with an empty list.
	board_state = board_state
	if flag == True:
		board_state.append(current,[])	
	#If the card is invalid, append it to the invalid list of the last card in the board state.
	else:
		board_state[-1][1].append(curr)
		
	return board_state