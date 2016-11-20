import random

master_board_state = list()

board_state = []

def pick_random_card():
	rank = random.choice( ('A','2','3','4','5','6','7','8','9','10','J','Q','K') )
	suit = random.choice( ('C','D','H','S') )
	card = rank + suit
	return card

# R => Red
# B => Black
# C => Club
# D => Diamond
# H => Hearts
# S => Spade
numeric_characterstic = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suit_characterstic = ['C','S','D','H']

def pick_random_card(card_characterstic_list):
	'''
	 Pick a random card using the card characterstic list given in the input
	'''
	if (card_characterstic_list):
		card_number = card_characterstic_list['numeric_characterstic']
		if(len(card_characterstic_list['suit_characterstic'])==1):
			card_suit = card_characterstic_list['suit_characterstic']
		else:
			# case when multiple card characterstic are present for example getting negative card
			card_suit = card_characterstic_list['suit_characterstic'].split(',')
		# TODO need to handle removing color
		# TODO And removing royal card

		numeric_characterstic.remove(card_number) # remove the number
		suit_characterstic.remove(card_suit) # remove the suit as we dont want a random card with the same suit
	rank = random.choice( numeric_characterstic )
	suit = random.choice( suit_characterstic )
	card = rank + suit
	return card

def update_board_state(board_state,flag,current_card):
	#We can also try using the global board state directly without passing it each time.
	#global board_state

	#If the card is valid, append it at the end of the board state with an empty list.
	board_state = board_state
	if flag == True:
		board_state.append(current_card,[])	
	#If the card is invalid, append it to the invalid list of the last card in the board state.
	else:
		board_state[-1][1].append(current_card)
		
	return board_state

def initialize_negative_characteristic_list(card_characterstic_list):
	# mapping of negative character
	negative_characterstic_list = {'Black':'Red','Red':'Black', 'C':'H,D' , 'S' : 'H,D', 'H': 'S,C', 'D': 'S,C'}
	if (not card_characterstic_list):
		print('Characterstic list empty')
		return None
	characterstic_list = []
	if (card_characterstic_list['suit_characterstic']) :
		suit_characterstic_values = negative_characterstic_list[card_characterstic_list['suit_characterstic']].split(',')
		characterstic_list.append(suit_characterstic_values[0])
		characterstic_list.append(suit_characterstic_values[1])
	characterstic_list.append(negative_characterstic_list[card_characterstic_list[2]])
	return pick_random_card(characterstic_list)

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
	else:
		curr_tuple = board_state[-1]
		if curr_tuple[1]:
			curr = curr_tuple[1][-1]
		else:
			curr = curr_tuple[0]
		prev2, prev = prev, curr
	legal_cards = [x for (x,y) in board_state]
	return_dict = {'prev2':prev2, 'prev':prev, 'curr':curr, 'legal_indices':legal_cards}

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


def map_card_characteristic_to_property():
	'''
		Return a mapping of all the card characterstic to the property
	'''
	return {1 : 'C1' , 2 : 'C2', 3: 'C3', 4: 'C4', 5: 'C5', 6: 'C6', 7: 'C7', 8: 'C8', 9: 'C9', 10: 'C10', 11: 'C11', 12: 'C12', 13: 'C13', 'red':'C14' , 'black': 'C15', 'diamond': 'C16' , 'heart':'C17', 'spade': 'C18', 'club': 'C19', 'even': 'C20', 'odd': 'C21', 'royal': 'C22' , 'not_royal': 'C23'}

def update_characteristic_list():
	#Read the current card
	#Get the card characteristics by invoking get_card_characteristics()
	#Invoke the map_card_characteristics() to get the corresponding numeric index into the card characteristic list.
	#Append the characteristics list with the index of the current card.
	board_state = parse_board_state()
	curr = board_state['curr']
	card_characteristics = get_card_characteristics(curr)

def get_card_char_from_property(index='red'):

    card_char_prop = map_card_characteristic_to_property();
    property = card_char_prop.get(index)
    return property

def get_card_characteristics(current='QH'):

    #color, suite, number, even/odd, royal

    royal = ['J', 'Q', 'K']
    card_char = {}
    #color = ""
    card_num = current[0]
    card_suite = current[1]

    #See if the card is royal is not
    if card_num in royal:
        card_char['royal'] = 'royal'
    else:
        card_char['not_royal'] = 'not_royal'

    #Adding the color in the char dictionary
    if card_suite == 'H' or card_suite == 'D':
        card_char['color'] = 'red'
    else:
        card_char['color'] = 'black'

    #Adding the suite in the char dictionary
    if card_suite == 'H':
        card_char['suite'] = 'heart'
    elif card_suite == 'D':
        card_char['suite'] = 'diamond'
    elif card_suite == 'C':
        card_char['suite'] = 'club'
    else:
        card_char['suite'] = 'spade'		

    #Adding the number in the card dictionary
    if card_num == "J":
        card_num = 11
    elif card_num == "Q":
        card_num = 12
    elif card_num == "K":
        card_num = 13
    card_char['number'] = card_num

    #Adding the even/odd property of the card in the char dictionary 
    card_num = int(card_num)
    if card_num % 2 == 0:
        card_char['even'] = 'even'
    else:
        card_char['odd'] = 'odd'

    return card_char

def initalize_characteristic_list():
	'''
		Intialize the characterstic list with zero values, which will be later used by update_card_characterstic
	'''
	return {'C1' : 0, 'C2':0, 'C3': 0, 'C4':0, 'C5':0, 'C6':0, 'C7':0, 'C8':0, 'C9': 0, 'C10': 0, 'C11': 0, 'C12': 0, 'C13': 0, 'C14' : 0, 'C15': 0, 'C16': 0, 'C17':0, 'C18':0, 'C19':0, 'C20':0, 'C21':0, 'C22': 0, 'C23':0}


def update_characteristic_list():
	#Read the current card
	#Get the card characteristics by invoking get_card_characteristics()
	#Invoke the map_card_characteristics() to get the corresponding numeric index into the card characteristic list.
	#Append the characteristics list with the index of the current card.
	board_state = parse_board_state()
	curr = board_state['curr']
	card_characteristics = get_card_characteristics(curr)
