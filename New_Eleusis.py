import random
import operator
import itertools
from collections import OrderedDict
from itertools import combinations

# Trivial functions to be used in the important test functions
# All require a nonempty string as the argument

def is_suit(s):
	"""Test if parameter is one of Club, Diamond, Heart, Spade"""
	return s in "CDHS"

def is_color(s):
	"""Test if parameter is one of Black or Red"""
	return s in "BR"

def is_value(s):
	"""Test if parameter is a number or can be interpreted as a number"""
	return s.isdigit() or (len(s) == 1 and s[0] in "AJQK")

def is_card(s):
	"""Test if parameter is a value followed by a suit"""
	return is_suit(s[-1]) and is_value(s[:len(s) - 1])

def value_to_number(name):
	"""Given the "value" part of a card, returns its numeric value"""
	values = [None, 'A', '2', '3', '4', '5', '6',
			  '7', '8', '9', '10', 'J', 'Q', 'K']
	return values.index(name)

def number_to_value(number):
	"""Given the numeric value of a card, returns its "value" name"""
	values = [None, 'A', '2', '3', '4', '5', '6',
			  '7', '8', '9', '10', 'J', 'Q', 'K']
	return values[number]

# -------------------- Important functions

def suit(card):
	"""Returns the suit of a card"""
	return card[-1]

def color(card):
	"""Returns the color of a card"""
	return {'C':'B', 'D':'R', 'H':'R', 'S':'B'}.get(suit(card))

def value(card):
	"""Returns the numeric value of a card or card value as an integer 1..13"""
	prefix = card[:len(card) - 1]
	names = {'A':1, 'J':11, 'Q':12, 'K':13}
	if prefix in names:
		return names.get(prefix)
	else:
		return int(prefix)

def is_royal(card):
	"""Tests if a card is royalty (Jack, Queen, or King)"""
	return value(card) > 10

def equal(a, b):
	"""Tests if two suits, two colors, two cards, or two values are equal."""
	return str(a) == str(b) # This is to allow comparisons with integers

def less(a, b):
	"""Tests if a is less than b, where a and b are suits, cards,
	   colors, or values. For suits: C < D < H < S. For colors,
	   B < R. For cards, suits are considered first, then values.
	   Values are compared numerically."""
	if is_card(a):
		if suit(a) != suit(b):
			return suit(a) < suit(b)
		else:
			return value(a) < value(b)
	elif is_value(a):
		return value_to_number(a) < value_to_number(b)
	else:
		return a < b

def greater(a, b):
	"""The opposite of less"""
	return less(b, a)

def plus1(x):
	"""Returns the next higher value, suit, or card in a suit;
	   must be one. If a color, returns the other color"""
	if is_value(x):
		assert value_to_number(x) < 13
		return number_to_value(value_to_number(x) + 1)
	elif is_suit(x):
		assert x != 'S'
		return "CDHS"["CDHS".index(x) + 1]
	elif is_card(x):
		return number_to_value(value(x) + 1) + suit(x)
	elif is_color(x):
		return "BR"["BR".index(x) - 1]
	
def minus1(x):
	"""Returns the next lower value, suit, or card in a suit;
	   must be one. If a color, returns the other color"""
	if is_value(x):
		assert value_to_number(x) > 1
		return number_to_value(value_to_number(x) - 1)
	elif is_suit(x):
		assert x != 'C'
		return "CDHS"["CDHS".index(x) - 1]
	elif is_card(x):
		return number_to_value(value(x) - 1) + suit(x)
	elif is_color(x):
		return "BR"["BR".index(x) - 1]

def even(card):
	"""Tells if the card's numeric value is even"""
	return value(card) % 2 == 0

def odd(card):
	"""Tells if the card's numeric value is odd"""
	return value(card) % 2 != 0

# -------------------- Lists of allowable functions

# These functions are declared so that logic can be supported;
# the actual implementation is in the 'evaluate' function
def andf(): pass
def orf():  pass
def notf(): pass
def iff():  pass

functions = [suit, color, value, is_royal, equal, less,
			 greater, plus1, minus1, even, odd, andf,
			 orf, notf, iff]

function_names = ['suit', 'color', 'value', 'is_royal',
				  'equal', 'equals', 'less', 'greater', 'plus1',
				  'minus1', 'even', 'odd', 'andf', 'orf',
				  'notf', 'iff', 'and', 'or', 'not', 'if']

# ----- Functions for creating, printing, and evaluating Trees

# Build a dictionary from function names to actual functions
to_function = {'and':andf, 'or':orf, 'not':notf, 'if':iff, 'equals':equal, 'even':even, 'odd':odd}
for f in functions:
	to_function[f.__name__] = f
	
def quote_if_needed(s):
	"""If s is not a function, quote it"""
	function_names = map(lambda x: x.__name__, functions)
	return s if s in function_names else "'" + s + "'"

def scan(s):
	"""This is an iterator for "tokens," where a token is a
	   parenthesis or sequence of nonblank characters; commas
	   and whitespace act as delimiters, and are discarded"""
	token = ''
	for ch in s:
		if ch.isspace():
			continue
		if ch in '(),':
			if token != '':
				yield token
				token = ''
			if ch != ',':
				yield ch
		else:
			token += ch
	if token != '':
		yield token
			
def tree(s):
	"""Given a function in the usual "f(a, b)" notation, returns
	   a Tree representation of that function, for example,
	   equal(color(current),'R') becomes
	   Tree(equal(Tree(color(current)),'R')) """
	tokens = list(scan(s))
	if len(tokens) == 1:
		return tokens[0]
	expr = ""
	functions = [] # a stack of functions
	args = []      # a stack of argument lists
	depth = 0
	for i in range(0, len(tokens) - 1):
		if tokens[i + 1] == '(':
			f = to_function[tokens[i]]
			depth += 1
		expr += tokens[i]
		if tokens[i] == ')':
			expr += ')'
			depth -= 1
	assert depth == 1, "*** Unmatched parentheses ***"
	return expr + '))'

def combine(f, args):
	"""Makes a Tree from a function and a list of arguments"""
	if len(args) == 1:
		return Tree(f, args[0])
	elif len(args) == 2:
		return Tree(f, args[0], args[1])
	elif len(args) == 3:
		return Tree(f, args[0], args[1], args[2])
	else:
		raise Exception("Incorrect arguments: {} {}".format(f, str(args)))
	
def parse(s):
	"""Converts a string representation of a rule into a Tree"""
	def parse2(s, i):
		if s[i] in function_names:
			f = to_function.get(s[i])
			assert s[i + 1] == "(", "No open parenthesis after " + s[i]
			(arg, i) = parse2(s, i + 2)
			args = [arg]
			while s[i] != ")":
				(arg, i) = parse2(s, i)
				args.append(arg)
			subtree = combine(f, args)
			return (subtree, i + 1)
		else:
			return (s[i], i + 1)
	return parse2(list(scan(s)), 0)[0]


class Tree:

	def __init__(self, root, first=None, second=None, third=None):
		"""Create a new Tree; default is no children"""
		self.root = root
		assert root in functions
		if third == None:
			self.test = None
			self.left = first
			self.right = second
		else: # rearrange parameters so test can be put first
			self.test = first
			self.left = second
			self.right = third

	def __str__(self):
		"""Provide a printable representation of this Tree"""
		if self.test != None: # it's an iff Tree
			return 'iff({}, {}, {})'.format(self.left, self.right, self.test)
		if self.left == None and self.right == None:
			return str(self.root)
		elif self.right == None:
			return '{}({})'.format(self.root.__name__, self.left)
		else:
			return '{}({}, {})'.format(self.root.__name__, self.left, self.right)

	def __repr__(self):
		s = "Tree("
		if self.root in functions:
			s += self.root.__name__
		else:
			str(self.root) + '!'
		if self.left != None:  s += ", " + repr(self.left)
		if self.right != None: s += ", " + repr(self.right)
		if self.test != None:  s += ", " + repr(self.test)
		return s + ")"
	
##    debugging = True
##    def evaluate(self, cards):
##        """For debugging, uncomment these lines and change
##           the name of evaluate (below) to evaluate"""
##        before = str(self)
##        after = self.evaluate2(cards)
##        if self.debugging: print "Tree: ", before, "-->", after
##        return after
	
	def evaluate(self, cards):
		"""Evaluate this tree with the given card values"""
		def subeval(expr):
			if expr.__class__.__name__ == "Tree":
				return expr.evaluate(cards)
			else:
				if expr == "current":
					return current
				elif expr == "previous":
					return previous
				elif expr == "previous2":
					return previous2
				else:
					return expr
		try:
			(previous2, previous, current) = cards
			f = self.root
			if f not in functions:
				return f
			
			if f in [suit, color, value, is_royal, minus1, plus1, even, odd]:
				return f(subeval(self.left))
			
			elif f in [equal, less, greater]:
				return f(subeval(self.left), subeval(self.right))
			
			elif f == andf:
				if subeval(self.left):
					return subeval(self.right)
				return False
			
			elif f == orf:
				if subeval(self.left):
					return True
				return subeval(self.right)
			
			elif f == notf:
				return not subeval(self.left)
			
			elif f == iff:
				if subeval(self.test):
					return subeval(self.left)
				else:
					return subeval(self.right)
		except Exception as e:
			print e
			print "Expression = ", self
			print " with cards =", cards
			raise



#master_board_state = [('KS', []), ('9H', []), ('6C', ['KS', '9C']), ('JH', []), ('QD',[]), ('5S', ['AS'])]
#master_board_state = [('KH', []), ('9C', []), ('6D', ['KS', '9C']), ('JS', []), ('QD',[]), ('5C', ['AS'])]
#master_board_state = [('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS']), ('10S', []), ('3H', []), ('6C', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS']), ('10S', []), ('3H', []), ('6C', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS']), ('10S', []), ('3H', []), ('6C', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS']), ('10S', []), ('3H', []), ('6C', []), ('9S', []), ('7H', []), ('6C', ['KS', '9C']), ('6H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS']), ('10S', []), ('3H', []), ('6C', []), ('JD', []), ('QC', []), ('KH', ['KS', '9C']), ('6S', [])]
#master_board_state = [('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS'])]
master_board_state = [('QS', []), ('4D', []), ('5C', ['KS', '9C']), ('10H', []), ('8C',[]), ('9H', ['AS'])]
#master_board_state = [('7C', [])]
#master_board_state = [('10S', []), ('10S', []), ('10S', []), ('10S', []), ('10S', [])]
predicted_rule = ''
card_characteristic_list =[]
board_state = ['9S','3H']
rule_list={}
char_dict={}


numeric_characterstic = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suit_characterstic = ['C','S','D','H']

def pick_random_card():
    '''
      This function picks a random card based in the suit and numeric characterstic
    '''
	rank = random.choice( ('A','2','3','4','5','6','7','8','9','10','J','Q','K') )
	suit = random.choice( ('C','D','H','S') )
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
	'''
      This function intializes a negative characterstic list and picks a random card
    '''
	negative_characterstic_list = {'B':'R','R':'B', 'C':'H,D,S' , 'S' : 'H,D,C', 'H': 'S,C,D', 'D': 'S,C,H', 'Even':'Odd'}
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

def master_board_state_1():
	return master_board_state

def parse_board_state():
    '''
      This function parses the board state and returns a dictionary of legal cards along with current, previous, previous2 cards
    '''
	board_state = master_board_state_1()
	prev = ''
	prev2 = ''
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
	return_dict = {'prev2':prev2, 'prev':prev, 'curr':curr, 'legal_cards':legal_cards}
	return return_dict

def parse_illegal_indices():
	'''This function returns list of tuples of length 3 representing curr as the illegal card, 
	and prev, prev2 are immediately preceding legal ones. 
	Illegal tuples of length 3 and 2 are currently handled. 
    '''
	illegal_tuple_list = list()
	board_state = master_board_state_1()
	for index, value in enumerate(board_state):
		if value[1]:
			illegal_index_list = value[1]
			for elem in illegal_index_list:
				illegal_tuple_length_three = (board_state[index - 1][0], value[0], elem)
				illegal_tuple_list.append(illegal_tuple_length_three)
				illegal_tuple_length_two = (value[0], elem)
				illegal_tuple_list.append(illegal_tuple_length_two)

	return illegal_tuple_list

def map_card_characteristic_to_property(prop):
    '''
        Returns a mapping of value to characterstic and reads a certain property and returns it characterstic
    '''
    property_dict = {'1' : 'C1' , '2' : 'C2', '3': 'C3', '4': 'C4', '5': 'C5', '6': 'C6', '7': 'C7', '8': 'C8', '9': 'C9', '10': 'C10', '11': 'C11', '12': 'C12', '13': 'C13', 'R':'C14' , 'B': 'C15', 'D': 'C16' , 'H':'C17', 'S': 'C18', 'C': 'C19', 'even': 'C20', 'odd': 'C21', 'royal': 'C22' , 'not_royal': 'C23'}
    if prop in property_dict:
        return property_dict[prop]
    else:
        return property_dict 

def map_card_characteristic_to_value(prop):
	'''
      This function returns the value associated with a characterstic
    '''
	property_dict = {'1' : 'C1' , '2' : 'C2', '3': 'C3', '4': 'C4', '5': 'C5', '6': 'C6', '7': 'C7', '8': 'C8', '9': 'C9', '10': 'C10', '11': 'C11', '12': 'C12', '13': 'C13', 'R':'C14' , 'B': 'C15', 'D': 'C16' , 'H':'C17', 'S': 'C18', 'C': 'C19', 'even': 'C20', 'odd': 'C21', 'royal': 'C22' , 'not_royal': 'C23'}

	for val in property_dict:
		if property_dict[val] == prop:
			return val


def get_card_char_from_property(index):
    '''
      This function returns a card characterstic usign the property
    '''
	card_char_prop = map_card_characteristic_to_property();
	property = card_char_prop.get(index)
	return property

def get_card_characteristics(current):
    '''
     This function return a list of all the characterstic associated with the current card
    '''
	#color, suite, number, even/odd, royal
	royal = ['A', 'J', 'Q', 'K']
	card_char = {}
	#color = ""
	if len(current) == 2:
		card_num = current[0]
		card_suite = current[1]
	elif len(current) == 3:
		card_num = current[0]+current[1]
		card_suite = current[2]
	else:
		print current
	#See if the card is royal is not

	if card_num in royal:
		card_char['royal'] = 'royal'
	else:
		card_char['not_royal'] = 'not_royal'

	#Adding the color in the char dictionary
	if card_suite == 'H' or card_suite == 'D':
		card_char['color'] = 'R'
	else:
		card_char['color'] = 'B'

	#Adding the suite in the char dictionary
	if card_suite == 'H':
		card_char['suite'] = 'H'
	elif card_suite == 'D':
		card_char['suite'] = 'D'
	elif card_suite == 'C':
		card_char['suite'] = 'C'
	else:
		card_char['suite'] = 'S'		

	#Adding the number in the card dictionary
	if card_num == 'A':
		card_num = '1'
	elif card_num == 'J':
		card_num = '11'
	elif card_num == 'Q':
		card_num = '12'
	elif card_num == 'K':
		card_num = '13'

	card_char[card_num] = card_num

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
	return {'C1' : [], 'C2':[], 'C3': [], 'C4':[], 'C5':[], 'C6':[], 'C7':[], 'C8':[], 'C9': [], 'C10': [], 'C11': [], 'C12': [], 'C13': [], 'C14' : [], 'C15': [], 'C16': [], 'C17':[], 'C18':[], 'C19':[], 'C20':[], 'C21':[], 'C22': [], 'C23':[]}

def set_characteristic_weights():
	''' 
      This function assigns a weighted probability for each card characterstic
	'''
	weighted_property_dict = {'C1' : 0.92, 'C2':0.92, 'C3': 0.92, 'C4':0.92, 'C5':0.92, 'C6':0.92, 'C7':0.92, 'C8':0.92, 'C9': 0.92, 'C10': 0.92, 'C11': 0.92, 'C12': 0.92, 'C13': 0.92, 'C14' : 0.5, 'C15': 0.5, 'C16': 0.75, 'C17':0.75, 'C18':0.75, 'C19':0.75, 'C20':0.5, 'C21':0.5, 'C22': 0.77, 'C23':0.23}
	return weighted_property_dict

def initialize_variable_offset():
    '''
     This function returns the current, previous, previous2 card
    '''
	offset_list=[]
	count=len(board_state)
	print count
	if count >= 3:
		prev2= board_state[-1]
		prev1=board_state[-2]
		curr = board_state[-3]
		offset_list.append(prev2)
		offset_list.append(prev1)
		offset_list.append(curr)
		print "[Current,Previous1, Previous2]: ",offset_list
	elif count is 1:
		curr = board_state[-1]
		offset_list.append(curr)
		print "[Current]: ",offset_list
	elif count is 0:
		print 'Board empty'
	elif count is 2:
		curr = board_state[-2]
		prev1 = board_state[-1]

		offset_list.append(prev1)
		offset_list.append(curr)
		print "[Current,Previous1]:",offset_list
		return offset_list

def scan_and_rank_hypothesis():
	
	hypothesis_dict = {}
	#get legal indices from the the board state
	board_state = parse_board_state()

	legal_cards = board_state['legal_cards']
	#print str(legal_cards)
	characteristic_index_list = []
	for i in xrange(0, len(legal_cards)):
		update_characteristic_list(legal_cards[i], i, char_dict)

	weighted_property_dict = set_characteristic_weights()
	hypothesis_index_dict = {}
	hypothesis_occurrence_count = {}
	
	mean = 0.0
	for i in xrange(2, len(legal_cards)):
		#Now we have individual chars in characteristic_index_list[i]
		#Decide on how to formulate hypothesis
		#Prev2, prev, curr
		combined_char_indices_list = [char_dict[i-2], char_dict[i-1], char_dict[i]]

		for characteristic_tuple in itertools.product(*combined_char_indices_list):
			#print 'Tuple: ' + str(characteristic_tuple)
			if characteristic_tuple in hypothesis_index_dict.keys():
				hypothesis_index_dict[characteristic_tuple].append((i-2, i-1, i))
			else:
				hypothesis_index_dict[characteristic_tuple] = [(i-2, i-1, i)]
			if characteristic_tuple in hypothesis_dict.keys():
				hypothesis_occurrence_count[characteristic_tuple] += 1
				hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3)*hypothesis_occurrence_count[characteristic_tuple]
			else:
				hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
				hypothesis_occurrence_count[characteristic_tuple] = 1
			mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
	   # print len(hypothesis_dict)     
		#print str(hypothesis_dict)
		#print str(OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True)))
		
	hypothesis_occurrence_count = {}

	for i in xrange(1, len(legal_cards)):
		#Now we have individual chars in characteristic_index_list[i]
		#Decide on how to formulate hypothesis
		combined_char_indices_list = [char_dict[i-1], char_dict[i]]

		for characteristic_tuple in itertools.product(*combined_char_indices_list):
			#print 'Tuple: ' + str(characteristic_tuple)
			if characteristic_tuple in hypothesis_index_dict.keys():
				hypothesis_index_dict[characteristic_tuple].append((i-1, i))
			else:
				hypothesis_index_dict[characteristic_tuple] = [(i-1, i)]

			if characteristic_tuple in hypothesis_dict.keys():
				hypothesis_occurrence_count[characteristic_tuple] += 1
				hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2)*hypothesis_occurrence_count[characteristic_tuple]
			else:
				hypothesis_occurrence_count[characteristic_tuple] = 1
				hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
			mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2

	
	ranked_hypothesis_dict = OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))
		
	hypothesis_offset = len(ranked_hypothesis_dict)
	mean_cutoff = mean/hypothesis_offset
	ranked_hypothesis = {} 
	for value in ranked_hypothesis_dict.iteritems():
		if value[1] > mean_cutoff :
			ranked_hypothesis[value[0]] = value[1]
		else:
			break

	

	#TODO eliminate conflicting hypothesis- ex: consecutive Royal/B/Odd & Non-Royal/R/Even. Check if already handled by pick_negative
	#Using illegal cards to eliminate possible hypothesis
	illegal_tuple_list = parse_illegal_indices()
	# print str(illegal_tuple_list)
	# print(master_board_state)
	for elem in illegal_tuple_list:
		if len(elem) > 2:
			prev2 = elem[0]
			prev = elem[1]
			curr = elem[2]
			# print('illegal_cards: ' + curr)
			# print(curr + ' ' + prev + ' ' + prev2)
			combined_char_indices_list = [get_card_mapping_characterstic(prev2), get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]

		hypothesis_occurrence_count = {}
		
		for characteristic_tuple in itertools.product(*combined_char_indices_list):
			if(len(characteristic_tuple)>2):
				if characteristic_tuple in ranked_hypothesis.keys():
					if characteristic_tuple in hypothesis_occurrence_count:
						hypothesis_occurrence_count[characteristic_tuple] += 1
					else:
						hypothesis_occurrence_count[characteristic_tuple] = 1
					ranked_hypothesis[characteristic_tuple] -= ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3)*hypothesis_occurrence_count[characteristic_tuple]

		else:
			prev = elem[0]
			curr = elem[1]

			hypothesis_occurrence_count = {}
			combined_char_indices_list = [get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]
			for characteristic_tuple in itertools.product(*combined_char_indices_list):
				if ((len(characteristic_tuple)>1) and (len(characteristic_tuple)<=2)):
					if characteristic_tuple in ranked_hypothesis.keys():
						if characteristic_tuple in hypothesis_occurrence_count:
							hypothesis_occurrence_count[characteristic_tuple] += 1
						else:
							hypothesis_occurrence_count[characteristic_tuple] = 1
						ranked_hypothesis[characteristic_tuple] -= ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2)*hypothesis_occurrence_count[characteristic_tuple]

	ranked_hypothesis = OrderedDict(sorted(ranked_hypothesis.items(), key = lambda (key, value) : (value, key), reverse=True))
	# #print str(len(ranked_hypothesis)) + ' len: ' + str(hypothesis_offset)
	#print str(ranked_hypothesis)
	return ranked_hypothesis, hypothesis_index_dict


def scan_and_rank_rules(ranked_hypothesis, hypothesis_index_dict):
	# TODO function needs to be implemented
	board_state = parse_board_state()
	weighted_property_dict = set_characteristic_weights()
	legal_cards = board_state['legal_cards']
	ranked_rules_list = []
	for value in ranked_hypothesis.iteritems():
		ranked_rules_list.append(value[0])
	pruned_ranked_hypothesis = ranked_rules_list[0:10]
	
	pruned_ranked_hypothesis_list = []
	for comb in combinations(pruned_ranked_hypothesis, 3):
		#print 'combination: ' + str(comb)
		pruned_ranked_hypothesis_list.append(comb)


	for comb in combinations(pruned_ranked_hypothesis, 2):
		#print 'combination: ' + str(comb)
		pruned_ranked_hypothesis_list.append(comb)        
	
	#print str(len(pruned_ranked_hypothesis_list))
	pruned_ranked_hypothesis_dict = {}
	mean = 0.0
	for tuple_elem in pruned_ranked_hypothesis_list:
		if len(tuple_elem) == 3:
			for i in xrange(2, len(legal_cards)):
				occurrence_flag = False
				accumulated_weight = 0.0
				if (len(tuple_elem[0])==3 and (tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[0][2] in get_card_mapping_characterstic(legal_cards[i]))):
					accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]] + weighted_property_dict[tuple_elem[0][2]])/3
					if (len(tuple_elem[1])==3 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]))):
						accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]])/3
						if (len(tuple_elem[2])==3 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]))):                    
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]])/3
							occurrence_flag = True
						elif (len(tuple_elem[2])==2 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]])/2
							occurrence_flag = True
					elif (len(tuple_elem[1])==2 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]))):
						accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]])/2                        
						if (len(tuple_elem[2])==3 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]))):                    
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]])/3
							occurrence_flag = True
						elif (len(tuple_elem[2])==2 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]])/2
							occurrence_flag = True
				elif (len(tuple_elem[0])==2 and (tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i]))):
					accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]])/2
					if (len(tuple_elem[1])==3 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]))):
						accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]])/3
						if (len(tuple_elem[2])==3 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]))):                    
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]])/3
							occurrence_flag = True
						elif (len(tuple_elem[2])==2 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]])/2
							occurrence_flag = True
					elif (len(tuple_elem[1])==2 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]))):
						accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]])/2                        
						if (len(tuple_elem[2])==3 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]))):                    
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]])/3
							occurrence_flag = True
						elif (len(tuple_elem[2])==2 and (tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]])/2
							occurrence_flag = True
				if occurrence_flag:
					if tuple_elem in pruned_ranked_hypothesis_dict:
						pruned_ranked_hypothesis_dict[tuple_elem] += accumulated_weight/3
					else:
						pruned_ranked_hypothesis_dict[tuple_elem] = accumulated_weight/3
					mean += accumulated_weight/3

		elif len(tuple_elem) == 2:
			for i in xrange(2, len(legal_cards)):
				if (len(tuple_elem[0])==3 and (tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[0][2] in get_card_mapping_characterstic(legal_cards[i]))):
					accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]] + weighted_property_dict[tuple_elem[0][2]])/3
					if (len(tuple_elem[1])==3 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]])/3
							occurrence_flag = True
					elif (len(tuple_elem[1])==2 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]])/2
							occurrence_flag = True
				elif (len(tuple_elem[0])==2 and (tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i]))):
					accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]])/2
					if (len(tuple_elem[1])==3 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-2])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]])/3
							occurrence_flag = True
					elif (len(tuple_elem[1])==2 and (tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i-1])) and (tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]))):
							accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]])/2
							occurrence_flag = True
				if occurrence_flag:
					if tuple_elem in pruned_ranked_hypothesis_dict:
						pruned_ranked_hypothesis_dict[tuple_elem] += accumulated_weight/2
					else:
						pruned_ranked_hypothesis_dict[tuple_elem] = accumulated_weight/2
					mean += accumulated_weight/2

	pruned_ranked_hypothesis_dict = OrderedDict(sorted(pruned_ranked_hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))
	#print str(pruned_ranked_hypothesis_dict)
	#print len(pruned_ranked_hypothesis_dict)
	hypothesis_offset = len(pruned_ranked_hypothesis_dict)
	mean_cutoff = mean/hypothesis_offset
	pr_ranked_hypothesis = {} 
	for value in pruned_ranked_hypothesis_dict.iteritems():
		if value[1] > mean_cutoff :
			pr_ranked_hypothesis[value[0]] = value[1]
		else:
			break

	pr_ranked_hypothesis = OrderedDict(sorted(pr_ranked_hypothesis.items(), key = lambda (key, value) : (value, key), reverse=True))
	print str(pr_ranked_hypothesis)
	print len(pr_ranked_hypothesis)

	return pr_ranked_hypothesis


def pick_negative_random(card_characterstic_list):
	'''
	 Picks a random negative card based on the characterstic presented
	'''
	color_mapping = {'R': 'D,H', 'B': 'S,C'}
	face_value_mapping = {'A': '1', 'J':'11', 'Q':'12', 'K': '13' }
	royal_card = {'J', 'Q', 'K'}
	numeric_characterstic = {'A':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False,'9':False,'10':False,'J':False,'Q':False,'K':False}
	suit_characterstic = {'C':False,'S':False,'D':False,'H':False}
	if (card_characterstic_list):
		# number 
		if ('number' in card_characterstic_list):
			if (len(card_characterstic_list)==1):
				card_number = card_characterstic_list['number']	
				numeric_characterstic[card_number] = True # remove the number
			else:
				for number in card_characterstic_list['number'].split(','):
					numeric_characterstic[number] = True # remove the number	


		# suite
		if ('suite' in card_characterstic_list):
			if(len(card_characterstic_list['suite'])==1):
				card_suit = card_characterstic_list['suite']
				suit_characterstic[card_suit] = True
			else:
				# case when multiple card characterstic are present for example getting negative card
				card_suit = card_characterstic_list['suite'].split(',')
				suit_characterstic[card_suit[0]] = True
				suit_characterstic[card_suit[1]] = True
			 # remove the suit as we dont want a random card with the same suit
			

		# remove  color cards
		if ('color' in card_characterstic_list):
			color_list = card_characterstic_list['color'].split(',')
			if (len(color_list)== 1):
				card_suit = color_mapping[card_characterstic_list['color']].split(',')
				suit_characterstic[card_suit[0]] = True
				suit_characterstic[card_suit[1]] = True
			else:
				card_suit_0 = color_mapping[color_list[0]].split(',')
				suit_characterstic[card_suit_0[0]] = True
				suit_characterstic[card_suit_0[1]] = True
				card_suit_1 = color_mapping[color_list[1]].split(',')
				suit_characterstic[card_suit_1[0]] = True
				suit_characterstic[card_suit_1[1]] = True
			
		# royal card remove
		if ('royal' in card_characterstic_list):
			for number in numeric_characterstic:
				if (number in royal_card):
					numeric_characterstic[number] = True

		# not royal card removal
		if ('not_royal' in card_characterstic_list):
			for number in numeric_characterstic:
				if (number not in royal_card):
					numeric_characterstic[number] = True			

		# face card
		if ('face' in card_characterstic_list):
			for number in numeric_characterstic:
				if (number in face_value_mapping):
					numeric_characterstic[number] = True

		# not face card
		if ('not_face' in card_characterstic_list):
			for number in numeric_characterstic:
				if (number not in face_value_mapping):
					numeric_characterstic[number] = True

		# remove all odd cards
		if ('odd' in card_characterstic_list):	
			for number in numeric_characterstic:
				if (number in face_value_mapping):
					card_num = face_value_mapping[number]
					if int(card_num)%2!=0:
						numeric_characterstic[number] = True
				elif int(number)%2!=0:
						numeric_characterstic[number] = True

		# remove even cards
		if ('even' in card_characterstic_list):
			for number in numeric_characterstic:
				if (number in face_value_mapping):
					card_num = face_value_mapping[number]
					if int(card_num)%2==0:
						numeric_characterstic[number] = True
				elif int(number)%2==0:
						numeric_characterstic[number] = True
				
			
	
	numeric_characterstic_list = []
	suit_characterstic_list = []
	for number in numeric_characterstic:
		if numeric_characterstic[number] == False:
			numeric_characterstic_list.append(number)

	for suite in suit_characterstic:
		if suit_characterstic[suite] == False:
			suit_characterstic_list.append(suite)

	if ((not numeric_characterstic_list) or (not suit_characterstic_list)):
		print('No valid card, Picking random card')
		return pick_random_card()
	else:
		rank = random.choice( numeric_characterstic_list )
		suit = random.choice( suit_characterstic_list )
		card = rank + suit
		return card

def pick_next_negative_card(rule_list):
    '''
     This returns a negative card associated with the top rule by using an intersection of the
     card characterstics of the top rule. If there is no intersection found we just return a
     random card
    '''
	intersection_rule_list = []
	numbers = []
	colors = []
	suites = []
	even_list = []
	odd_list = []
	royal_list = []
	not_royal_list = []
	number_list =['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
	color_list =['C14','C15']
	suite_list = ['C16','C17','C18','C19']
	even = ['C20']
	odd = ['C21']
	royal = ['C22']
	not_royal = ['C23']
	for rule in rule_list:

		# numbers
		if (rule[len(rule)-1] in number_list):
			numbers.append(map_card_characteristic_to_value(rule[len(rule)-1]))
		
		#colors
		if (rule[len(rule)-1] in color_list):
			colors.append(map_card_characteristic_to_value(rule[len(rule)-1]))

		#suites
		if (rule[len(rule)-1] in suite_list):
			suites.append(map_card_characteristic_to_value(rule[len(rule)-1]))

		#even
		if (rule[len(rule)-1] in even):
			even_list.append(map_card_characteristic_to_value(rule[len(rule)-1]))

		#odd
		if (rule[len(rule)-1] in odd):
			odd_list.append(map_card_characteristic_to_value(rule[len(rule)-1]))

		#royal
		if (rule[len(rule)-1] in royal):
			royal_list.append(map_card_characteristic_to_value(rule[len(rule)-1]))

		#not_royal
		if (rule[len(rule)-1] in not_royal):
			not_royal_list.append(map_card_characteristic_to_value(rule[len(rule)-1]))
	card_characterstic_list = {}
	if (numbers):
		card_characterstic_list['numbers'] = ','.join(numbers)

	if (colors):
		card_characterstic_list['color'] = ','.join(colors)

	if (suites):
		card_characterstic_list['suite'] = ','.join(suites)

	if (even_list):
		card_characterstic_list['even'] = True

	if (odd_list):
		card_characterstic_list['odd'] = True

	if (royal_list):
		card_characterstic_list['royal'] = True

	if (not_royal_list):
		card_characterstic_list['not_royal'] = True
	
	return pick_negative_random(card_characterstic_list)

def update_characteristic_list(current_card, current_card_index, char_dict):
	'''Read the current card
	 Get the card characteristics by invoking get_card_characteristics()
	 Invoke the map_card_characteristics() to get the corresponding numeric index into the card characteristic list.
	Append the characteristics list with the index of the current card.
    '''
	board_state = parse_board_state()
	
	card_characteristics = get_card_characteristics(current_card)
	for characteristic in card_characteristics:
		card_characteristic_index = map_card_characteristic_to_property(card_characteristics[characteristic])

		#char_dict[card_characteristic_index].append(board_state['legal_cards'].index(current_card))
		if current_card_index not in char_dict.keys():
			char_dict[current_card_index] = []
		char_dict[current_card_index].append(card_characteristic_index)
	return char_dict

def get_card_mapping_characterstic(current_card):
	'''Read the current card
	 Get the card characteristics by invoking get_card_characteristics()
	 Invoke the map_card_characteristics() to get the corresponding numeric index into the card characteristic list.
	 Append the characteristics list with the index of the current card.
     '''
	card_characteristics = get_card_characteristics(current_card)
	card_characteristic_list = []
	for characteristic in card_characteristics:
		card_characteristic_index = map_card_characteristic_to_property(card_characteristics[characteristic])
		card_characteristic_list.append(card_characteristic_index)
	return card_characteristic_list

def get_card_from_characteristics(card_characteristics):
    '''
     This function returns a valid card based on the characterstic specified in the parameter
    '''
    # Format {'number': 9, 'suite': 'C', 'color': 'B'}
    # Format {'suite': 'C', 'color': 'B'}
    # Format {'number': 9}
    #Iterate over each of the card characteristic from the input list and compose a matching card. 
    #This will be done by creating a card with first characteristic from the characteristic list and iteratively applying filters based on subsequent characteristics.
    numeric_tuple = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
    suite_tuple = ('C','D','H','S')
    if (card_characteristics):
        if ('color' in card_characteristics and card_characteristics['color'] == 'R') :
            suite_tuple = ('D','H')
        elif('color' in card_characteristics and card_characteristics['color'] == 'B') :
            suite_tuple = ('C','S')
        else:
            suite_tuple = ('C','D','H','S')
        if ('suite' in card_characteristics):
            suite_tuple = (card_characteristics['suite'])
        if ('number' in card_characteristics):
            numeric_tuple = (card_characteristics['number'])

    if ('number' in card_characteristics and card_characteristics['number']) :
        rank = str(card_characteristics['number'])
    else:
        rank = random.choice(numeric_tuple)
    if ('suite' in card_characteristics and card_characteristics['suite']):
        suit = random.choice( suite_tuple )
    else:
        suit = random.choice( suite_tuple ) 
    
    card = rank + suit
    return card

def play(card):
    '''
     This function plays a card and validates the card and then updates the board state with the new card 
     based on whether the card is legal or not
    '''
	#Invoke validate_card() which returns True/False if the current play is legal/illegal.
	#Update the board_state by calling update_board_state()
	#Return a boolean value based on the legality of the card. 
	card_legality = validate_card(card)
	update_board_state(board_state,card_legality,card)
	return card_legality

#scan_and_rank_rules(scan_and_rank_hypothesis())

# ranked_hypothesis_list, hypothesis_index_dict = scan_and_rank_hypothesis()

def validate_and_refine_formulated_rule(rule_list = [(Tree(orf, Tree(equal, Tree(color, 'previous'), 'R'), Tree(equal, Tree(color, 'current'), 'R'))),(Tree(orf, Tree(even, 'previous'), Tree(even,'current'))),(Tree(orf, Tree(andf, Tree(odd, 'previous'), Tree(even,'current')), Tree(andf, Tree(even, 'previous'), Tree(odd,'current'))))]):

	'''
	1. get_card_mapping_characterstic() ==> 
	2. combined_char_indices_list = [get_card_mapping_characterstic(tuple[0]), get_card_mapping_characterstic(tuple[1]), char_dict[i]]

        for characteristic_tuple in itertools.product(*combined_char_indices_list):
            #print 'Tuple: ' + str(characteristic_tuple)
            if characteristic_tuple in hypothesis_index_dict.keys():
                hypothesis_index_dict[characteristic_tuple].append((i-2, i-1, i))
            else:
                hypothesis_index_dict[characteristic_tuple] = [(i-2, i-1, i)]
            if characteristic_tuple in hypothesis_dict.keys():
                hypothesis_occurrence_count[characteristic_tuple] += 1
                hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3)*hypothesis_occurrence_count[characteristic_tuple]
            else:
                hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
                hypothesis_occurrence_count[characteristic_tuple] = 1
            mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
	'''
	
	#board_state = [('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS'])]
	
	i = 0	
	exception_legal = {}
	exception_illegal = {}
	# Red must follow black
	#rule1 = Tree(orf, Tree(equal, Tree(color, 'previous'), 'R'), Tree(equal, Tree(color, 'current'), 'R'))
	#print rule1.evaluate(['6H', '7D', '9S'])
	#Even must follow Odd test
	'''rule2 = Tree(orf, Tree(even, 'previous'), Tree(even,'current'))

	#Alternate the sequence even odd
	rule3 = Tree(orf, Tree(andf, Tree(odd, 'previous'), Tree(even,'current')), Tree(andf, Tree(even, 'previous'), Tree(odd,'current')))

	legal_card = ['10S', '3H', '6H', '7D','9S','7S']
	
	legal_card2 = ['8S','7H','6S']
	print rule2.evaluate((legal_card2))

	legal_card3 = ['6C','5C','7C']
	print rule3.evaluate((legal_card3))'''

	
	#legal_card = ['10S', '3H', '6H', '7D','9S','7S']
	legal_card = parse_board_state()
	legal_card = legal_card['legal_cards']
	#print legal_card
	#legal_card = ['10S','3H']
	#illegal_cards = [('3H', '6C', 'KS'), ('3H', '6C', '9C'), ('7D', '9S', 'AS'), ('6H','7D','9S')]
	illegal_cards = parse_illegal_indices()

	for rule in rule_list:
		while((i + 2) < len(legal_card)):
			my_legal_list = (legal_card[i],legal_card[i+1],legal_card[i+2])
			if rule.evaluate((my_legal_list)) == False:
				if rule in exception_legal:
					exception_legal[rule].append(my_legal_list)
				else:
					exception_legal[rule] = [my_legal_list]
			i += 1

		for tup in illegal_cards:
			if len(tup) > 2:
				my_illegal_list = (tup[0], tup[1], tup[2])
				if rule.evaluate((my_illegal_list)) == True:
					if rule in exception_illegal:
						exception_illegal[rule].append(my_illegal_list)
					else:
						exception_illegal[rule] = [my_illegal_list]

	legal_exceptions_list = exception_legal.values() #The legal exceptions values for a rule
	illegal_exceptions_list = exception_illegal.values() #The illegal exceptions values for a rule

	#print str(legal_exceptions_list) + "legal!!"
	#print illegal_exceptions_list
	#print exception_legal
	#print exception_illegal

	#property_dict = {'1' : 'C1' , '2' : 'C2', '3': 'C3', '4': 'C4', '5': 'C5', '6': 'C6', '7': 'C7', '8': 'C8', '9': 'C9', '10': 'C10', '11': 'C11', '12': 'C12', '13': 'C13', 'red':'C14' , 'black': 'C15', 'diamond': 'C16' , 'heart':'C17', 'spade': 'C18', 'club': 'C19', 'even': 'C20', 'odd': 'C21', 'royal': 'C22' , 'not_royal': 'C23'}
	hypothesis_index_dict = {}
	hypothesis_dict = {}
	weighted_property_dict = set_characteristic_weights()
	hypothesis_occurrence_count = {}
	mean = 0.0

	if len(legal_exceptions_list) > 0:
		for tup in legal_exceptions_list:
			for val in tup:
				combined_char_indices_list = [get_card_mapping_characterstic(val[0]), get_card_mapping_characterstic(val[1]), get_card_mapping_characterstic(val[2])]
				for characteristic_tuple in itertools.product(*combined_char_indices_list):
					if characteristic_tuple in hypothesis_index_dict.keys():
						hypothesis_index_dict[characteristic_tuple].append((val[2],val[1],val[0]))
					else:
						hypothesis_index_dict[characteristic_tuple] = [(val[2],val[1],val[0])]
					if characteristic_tuple in hypothesis_dict.keys():
						hypothesis_occurrence_count[characteristic_tuple] += 1
						hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3)*hypothesis_occurrence_count[characteristic_tuple]
					else:
						hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
						hypothesis_occurrence_count[characteristic_tuple] = 1
					mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]]) / 3
		
		for tup in legal_exceptions_list:
			for val in tup:		
				hypothesis_occurrence_count = {}
				combined_char_indices_list = [get_card_mapping_characterstic(val[1]), get_card_mapping_characterstic(val[2])]
				for characteristic_tuple in itertools.product(*combined_char_indices_list):
					if characteristic_tuple in hypothesis_index_dict.keys():
						hypothesis_index_dict[characteristic_tuple].append((val[2], val[1]))
			        else:
			            hypothesis_index_dict[characteristic_tuple] = [(val[2], val[1])]

			        if characteristic_tuple in hypothesis_dict.keys():
			            hypothesis_occurrence_count[characteristic_tuple] += 1
			            hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2)*hypothesis_occurrence_count[characteristic_tuple]
			        else:
			            hypothesis_occurrence_count[characteristic_tuple] = 1
			            hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
			        mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
		
		ranked_hypothesis_dict = OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))
		hypothesis_offset = len(ranked_hypothesis_dict)
		mean_cutoff = mean/hypothesis_offset
		ranked_hypothesis = {} 
		for value in ranked_hypothesis_dict.iteritems():
			if value[1] > mean_cutoff:
				ranked_hypothesis[value[0]] = value[1]
			else:
				break
		#print ranked_hypothesis_dict
	else:
		print "Legal exception list is NULL!!"
	


	print '=======================================Illegal======================================================================='
	hypothesis_index_dict = {}
	hypothesis_dict = {}
	weighted_property_dict = set_characteristic_weights()
	hypothesis_occurrence_count = {}
	ranked_hypothesis_dict = {}
	mean = 0.0

	if len(illegal_exceptions_list) > 0:
		for tup in illegal_exceptions_list:
			for val in tup:
				combined_char_indices_list = [get_card_mapping_characterstic(val[0]), get_card_mapping_characterstic(val[1]), get_card_mapping_characterstic(val[2])]
				for characteristic_tuple in itertools.product(*combined_char_indices_list):
					if characteristic_tuple in hypothesis_index_dict.keys():
						hypothesis_index_dict[characteristic_tuple].append((val[2],val[1],val[0]))
					else:
						hypothesis_index_dict[characteristic_tuple] = [(val[2],val[1],val[0])]
					if characteristic_tuple in hypothesis_dict.keys():
						hypothesis_occurrence_count[characteristic_tuple] += 1
						hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3)*hypothesis_occurrence_count[characteristic_tuple]
					else:
						hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
						hypothesis_occurrence_count[characteristic_tuple] = 1
					mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]]) / 3
		
		for tup in legal_exceptions_list:
			for val in tup:		
				hypothesis_occurrence_count = {}
				combined_char_indices_list = [get_card_mapping_characterstic(val[1]), get_card_mapping_characterstic(val[2])]
				for characteristic_tuple in itertools.product(*combined_char_indices_list):
					if characteristic_tuple in hypothesis_index_dict.keys():
						hypothesis_index_dict[characteristic_tuple].append((val[2], val[1]))
			        else:
			            hypothesis_index_dict[characteristic_tuple] = [(val[2], val[1])]

			        if characteristic_tuple in hypothesis_dict.keys():
			            hypothesis_occurrence_count[characteristic_tuple] += 1
			            hypothesis_dict[characteristic_tuple] += ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2)*hypothesis_occurrence_count[characteristic_tuple]
			        else:
			            hypothesis_occurrence_count[characteristic_tuple] = 1
			            hypothesis_dict[characteristic_tuple] = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
			        mean += (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
		
		ranked_hypothesis_dict = OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))
		hypothesis_offset = len(ranked_hypothesis_dict)
		mean_cutoff = mean/hypothesis_offset
		ranked_hypothesis = {} 
		for value in ranked_hypothesis_dict.iteritems():
			if value[1] > mean_cutoff:
				ranked_hypothesis[value[0]] = value[1]
			else:
				break
	else:
		print "Illegal exception list is NULL!!"
		
	return
	
	#print ranked_hypothesis_dict


def setRule(ruleExp):
    '''
     This function set the predicted rule variable as the rule exp passed as parameter
    '''
	predicted_rule = ruleExp

def rule():
    '''
     This function returns the current rule
    '''
	#return the current rule
	return predicted_rule;

def score(board_state):
    '''
     This function returns a score associated with the current board state
    '''
	current_score = 0
	play_counter = 0
	board_state = parse_board_state()
	illegal_index_list = parse_illegal_indices()

	if board_state:
		legal_cards = board_state['legal_cards'];
	for card in legal_cards:
		if play_counter >=20:
			current_score +=1
	current_score = current_score + 2*(len(illegal_index_list))
	scientist_rule = scientist()
	current_rule = rule()
	if scientist_rule != current_rule:
		current_score += 15
		# TODO: Validate predicted rule using validate_rule method for the current rule
		# TODO: Check if predicted rule conforms to the rule current 
	return current_score

def find_numeric_characteristic_relation(current_card, prev_card, prev2_card):
    '''
     This function defines a numeric relation between a sliding window of current, prev, prev2 cards
    '''
	numeric_relation_dic = {}
	if (equal(current_card, prev_card)):
		numeric_relation_dic['current_equal_prev'] = True
	if (equal(current_card, prev2_card)):
		numeric_relation_dic['current_equal_prev2'] = True
	if (equal(prev_card, prev2_card)):
		numeric_relation_dic['prev_equal_prev2'] = True

	# greater relation
	if (greater(current_card, prev_card)):
		numeric_relation_dic['current_greater_prev'] = True
	if (greater(current_card, prev2_card)):
		numeric_relation_dic['current_greater_prev2'] = True
	if (greater(prev_card, prev2_card)):
		numeric_relation_dic['prev_greater_prev2'] = True

	# less relation
	if (less(current_card, prev_card)):
		numeric_relation_dic['current_less_prev'] = True
	if (less(current_card, prev2_card)):
		numeric_relation_dic['current_less_prev2'] = True
	if (less(prev_card, prev2_card)):
		numeric_relation_dic['prev_less_prev2'] = True


	# adds relation
	numeric_relation_dic['current_adds_prev'] = value(current_card) + value(prev_card)
	numeric_relation_dic['current_adds_prev2'] = value(current_card) + value(prev2_card)
	numeric_relation_dic['prev_adds_prev2'] = value(prev_card) + value(prev2_card)

	# minus relation
	numeric_relation_dic['current_minus_prev'] = value(current_card) - value(prev_card)
	numeric_relation_dic['current_minus_prev2'] = value(current_card) - value(prev2_card)
	numeric_relation_dic['prev_minus_prev2'] = value(prev_card) - value(prev2_card)

	return numeric_relation_dic;

def validate_card():
	#Output: Return True/False, if the current card conforms to the actual rule.
	#board_state = [('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D',[]), ('9S', ['AS'])]

	#board_state = parse_board_state() ==> Gives error atm

	#This is the actual rule which the rule function should return
	# R must follow B
	rule1 = Tree(orf, Tree(equal, Tree(color, 'previous'), 'R'), Tree(equal, Tree(color, 'current'), 'R'))

	#fetch from legal list
	curr = 'AD'
	prev1 = '9S'
	prev2 = '7D'
	#legal_card = ['10S', '3H', '6H', '7D','9S','7S']
	return rule1.evaluate((prev2,prev1,curr))	

def map_characteristic_value_to_characteristic_property(characteristic_value):
    '''
     This function returns a mapping of the characterstic value to the property
    '''
	characteristic_value_to_characteristic_property_dict = {'R':color, 'B':color, 'S':suit, 'C':suit, 'H':suit, 'D':suit, '1': value, '2': value, '3': value, '4': value, '5': value, '6': value, '7': value, '8': value, '9': value, '10': value}
	return characteristic_value_to_characteristic_property_dict[characteristic_value]    

def create_tree(rule):
    '''
     This function converts the internal mapping of characterstic values eg C1,C2 to a tree format which 
     can be easily validated using the evaluate function
    '''
	#TODO - Handle numeric relations during hypothesis transformation. Will be done by invoking find_characteristic_numeric_relation

	triple_tree_characteristic_list = ['R', 'B', 'S', 'C', 'H', 'D', 'value']

	param_switch_dict = {
		0: 'previous2',
		1: 'previous',
		2: 'current'
	}

	transformed_hypothesis_list = []
	transformed_rule_list = []
	for hypothesis in rule:
		#Form an AND of each hypothesis part of the rule

		for i in xrange(0, len(hypothesis)):
			if len(hypothesis) == 3:
				param_index = i
			elif len(hypothesis) == 2:
				if i == 2:
					break
				param_index = i+1
			
			characteristic_value = map_card_characteristic_to_value(hypothesis[i])
			if characteristic_value in triple_tree_characteristic_list:
				characteristic_property = map_characteristic_value_to_characteristic_property(characteristic_value)
			else:
				characteristic_property = to_function[characteristic_value]

			transformed_hypothesis = Tree(characteristic_property, param_switch_dict.get(param_index))
			if characteristic_value in triple_tree_characteristic_list:
				#create Tree with 3 paramaters
				#characteristic_index = C14, characteristic_value = R, characteristic_property = 'color'
				first_param = equal
				third_param = characteristic_value
				transformed_hypothesis = Tree(first_param, transformed_hypothesis, third_param)
			transformed_hypothesis_list.append(transformed_hypothesis)

		transformed_hypothesis = transformed_hypothesis_list[0]
		for i in xrange(1, len(transformed_hypothesis_list)):
			transformed_hypothesis = Tree(to_function['and'], transformed_hypothesis, transformed_hypothesis_list[i])
		transformed_rule_list.append(transformed_hypothesis)
		transformed_hypothesis_list = []

	transformed_rule = transformed_rule_list[0]
	for i in xrange(1, len(transformed_rule_list)):
		transformed_rule = Tree(to_function['and'], transformed_rule , transformed_rule_list[i])

	return transformed_rule


def scientist():

	parse_board_state()
	initialize_variable_offset()
	pick_random_card()
	plays = 0
	while plays <= 200:
		#play(<card>)
		parse_illegal_indices()
		initalize_characteristic_list()
		#TODO Please remove
		# characteristic_list = get_card_characteristics('7H')
		# update_characteristic_list(characteristic_list)
		# map_card_characteristic_to_property(characteristic_list)
		ranked_hypothesis, hypothesis_index_dict = scan_and_rank_hypothesis()
		pr_ranked_hypothesis = scan_and_rank_rules(ranked_hypothesis, hypothesis_index_dict)
		top_rule = pr_ranked_hypothesis.popitem()
		print 'Top Rule: ' + str(top_rule[0])
		#Create Tree for each rule in pr_ranked_hypothesis and pass to validate
		print str(create_tree(top_rule[0]))
		#validate_and_refine_formulated_rule()
		# pick_next_random_card()
		#validate_and_refine_formulated_rule()
		print 'Negative Card: ' + str(pick_next_negative_card(top_rule[0]))
	

	return ''

scientist()