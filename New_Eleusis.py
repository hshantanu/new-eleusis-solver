import random

master_board_state = list()
def pick_random_card():
	rank = random.choice( ('A','2','3','4','5','6','7','8','9','T','J','Q','K') )
	suit = random.choice( ('C','D','H','S') )
	card = rank + suit
	return card


print(pick_random_card())


def board_state():
    return master_board_state


def parse_board_state():
	board_state = board_state()
	
	if len(board_state) == 2:
		#2 elements present, initialize prev & prev2
		prev2 = board_state[0]
		prev = board_state[1]

		#Check if 1 or 2 cards are played based on the rule generated.
		#Return the legal board state.
		#Based on the rule curr, prev and prev2 will be initialized. 
	legal_indices = [x for (x,y) in board_state]
	return_dict = {'prev2':prev2, 'prev':prev, 'legal_indices':legal_indices}

def parse_illegal_indices():
	#This function returns list of tuples of length 3 representing curr as the illegal card, 
	#and prev, prev2 are immediately preceding legal ones. 
	#Illegal tuples of length 3 are currently handled. To be extended to length of 2 & 1.
	illegal_tuple_list = list()
	board_state = board_state()
	for index, value in enumerate(board_state):
		if value[1]:
			illegal_index_list = value[1]
			for elem in illegal_index_list:
				illegal_tuple = (board_state[index - 1][0], value[0], elem)
				illegal_tuple_list.append(illegal_tuple)

	return illegal_tuple_list

