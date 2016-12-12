import random
from itertools import izip_longest
from NewEleusisHelper import get_master_board_state
#from New_Eleusis import value

sum_greater_than = []
sum_less_than = []
empty_less_flag = False
empty_great_flag = False

#We can use the readymade method from New_Eleusis.py
def value(prop):
	
	property_dict = {'K':13, 'Q':12, 'J':11}
	if(len(prop) == 3):
		prop = prop[0:2]
	elif prop[0] == 'A':
			prop[0] = 1
	else:
		prop = prop[0]

	if prop in property_dict:
		prop = property_dict[prop]

	return int(prop)

def get_mapping(prev2,prev1,legal_flag):

	#print prev2,prev1,legal_flag

	global sum_greater_than,sum_less_than
	global empty_less_flag, empty_great_flag

	if empty_great_flag and empty_less_flag:
		print "Breaking as the conditions are satisfied."
		exit()
	if (len(sum_greater_than) == 1 and len(sum_less_than) == 0):
		print "We have found the rule"
		exit()
	if (len(sum_greater_than) == 0 and len(sum_less_than) == 1):
		print "We have found the rule"
		exit()
	
	prev1 = value(prev1)
	prev2 = value(prev2)
	add = prev2 + prev1
	if len(sum_less_than) == 0 and len(sum_greater_than) == 0:
		sum_greater_than = range(1, add)
		sum_less_than = range(add+1, 27)
	else:
		if legal_flag == True:
			if add-1 < sum_greater_than[-1] and empty_great_flag == False:
				sum_greater_than = range(1,add)
			if add+1 > sum_less_than[0] and empty_less_flag == False:
				sum_less_than = range(add+1,27)
		else:
			if empty_great_flag == False:
				if add > sum_greater_than[-1]: 
					sum_greater_than = []
					empty_great_flag = True
				else:
					print empty_great_flag
					if empty_great_flag == False:
						sum_greater_than = range(add+1,sum_greater_than[-1]+1)
			
			if (add < sum_less_than[0]) and empty_less_flag == False:
				sum_less_than = []
				empty_less_flag = True
			else:
				if empty_less_flag == False:
					sum_less_than = range(sum_less_than[0],add)

	print "Sum greater than " + str(sum_greater_than)
	print "Sum less than " + str(sum_less_than)

def pairs(state):
	for (key, lst), nxt in izip_longest(state, state[1:]):
		for x in lst:
			yield key, x, False
		if nxt is not None:
			yield key, nxt[0], True

def map_numeric():

	master_board_state = [('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D', []), ('9S', ['AS', 'KS', 'QC']), ('KD', []), ('6C', []), ('3D', []), ('AD', []), ('JD', []), ('AS', []), ('2H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D', []), ('9S', ['AS', 'KS', 'QC']), ('KD', []), ('6C', []), ('3D', []), ('AD', []), ('JD', []), ('AS', []), ('2H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D', []), ('9S', ['AS', 'KS', 'QC']), ('KD', []), ('6C', []), ('3D', []), ('AD', []), ('JD', []), ('AS', []), ('2H', []), ('10S', []), ('3H', []), ('6C', ['KS', '9C']), ('6H', []), ('7D', []), ('9S', ['AS', 'KS', 'QC']), ('KD', []), ('6C', []), ('3D', []), ('AD', []), ('JD', []), ('AS', []), ('2H', [])]
	#master_board_state = get_master_board_state()
	#master_board_state = [('QS', []), ('4D', []), ('5C', ['KS', '9C']), ('10H', []), ('8C',[]), ('9H', ['AS'])]
	#master_board_state = [('10S', []), ('3H', []), ('6C', ['KS'])]
	
	my_list = []
	for p in pairs(master_board_state):
		my_list.append(p)

	for val in my_list:
		get_mapping(val[0],val[1],val[2])

map_numeric()