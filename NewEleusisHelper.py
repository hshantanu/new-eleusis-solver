# Team Name: Guess My Rule! 

# Members: 
# Vipin Pillai
# Sailakshmi Pisupati
# Rahul Raghavan
# Shantanu Hirlekar


import random
import operator
import itertools
import time
from collections import OrderedDict
from itertools import combinations
<<<<<<< Updated upstream


master_board_state = []


import time

master_board_state = [] # [('10S', []), ('3H', []), ('10H', []), ('10H', []), ('10H', []), ('10H', []) ]

def pick_random_card():
    '''
      This function picks a random card based in the suit and numeric characterstic
    '''
    rank = random.choice( ('A','2','3','4','5','6','7','8','9','10','J','Q','K'))
    suit = random.choice( ('C','D','H','S') )
    card = rank + suit
    return card

def update_board_state(board_state,flag,current_card):
    #If the card is valid, append it at the end of the board state with an empty list.
    
    if flag == True:
        board_state.append((current_card,[]))   
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

def get_master_board_state():
    '''This function returns the master_board_state
    '''
    return master_board_state

def parse_board_state():

    board_state = get_master_board_state()
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
    board_state = get_master_board_state()
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
    weighted_property_dict = {'C1' : 0.92, 'C2':0.92, 'C3': 0.92, 'C4':0.92, 'C5':0.92, 'C6':0.92, 'C7':0.92, 'C8':0.92, 'C9': 0.92, 'C10': 0.92, 'C11': 0.92, 'C12': 0.92, 'C13': 0.92, 'C14' : 0.5, 'C15': 0.5, 'C16': 0.75, 'C17':0.75, 'C18':0.75, 'C19':0.75, 'C20':0.5, 'C21':0.5, 'C22': 0.77, 'C23':0.01}
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

def get_card_value(card):
    """Returns the numeric value of a card or card value as an integer 1..13"""
    prefix = card[:len(card) - 1]
    names = {'A':1, 'J':11, 'Q':12, 'K':13}
    if prefix in names:
        return names.get(prefix)
    else:
        return int(prefix)


def pick_negative_random(card_characterstic_list, last_rule_counter, card_list = []):
    '''
     Picks a random negative card based on the characterstic presented
    '''
    color_mapping = get_color_mapping()
    face_value_mapping = {'A': '1', 'J':'11', 'Q':'12', 'K': '13' }
    royal_card = {'J', 'Q', 'K'}
    numeric_characterstic = {'A':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False,'9':False,'10':False,'J':False,'Q':False,'K':False}
    suit_characterstic = {'C':False,'S':False,'D':False,'H':False}
    legal_cards = parse_board_state()['legal_cards']
    # print('-------------------legal_cards-----------------------', legal_cards)
    illegal_cards = parse_illegal_indices()
    illegal_counter = 0
    for elem in illegal_cards:
        if len(elem) == 2:
            illegal_counter += 1

    ratio_legal = float(len(legal_cards))/float(len(legal_cards)+ illegal_counter)
    # print('-------------------legal_cards-----------------------', len(legal_cards))
    # print('-------------------illegal_card_counter-----------------------', illegal_counter)
    # print('-------------------ratio_legal-----------------------', ratio_legal)
    put_out_legal = False
    if(ratio_legal < 0.667):
        put_out_legal = True

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
    
    if put_out_legal == False:
        
        for number in numeric_characterstic:
            if numeric_characterstic[number] == False:
                numeric_characterstic_list.append(number)

        for suite in suit_characterstic:
            if suit_characterstic[suite] == False:
                suit_characterstic_list.append(suite)
    else:
        
        for number in numeric_characterstic:
            if numeric_characterstic[number] == True:
                numeric_characterstic_list.append(number)

        for suite in suit_characterstic:
            if suit_characterstic[suite] == True:
                suit_characterstic_list.append(suite)


    if ((not numeric_characterstic_list) or (not suit_characterstic_list)):
        print('No valid card, Picking random card')
        return pick_random_card()
    else:
        # send empty card list now
        card = get_card_from_characterstic(suit_characterstic, numeric_characterstic, card_list, card_characterstic_list)
        return card

def get_color_mapping():
    return {'R': 'D,H', 'B': 'S,C'}

def get_card_from_characterstic(suite_characterstic, number_characterstic, card_list, characterstic_list):
    no_card_found = True
    negative_card_list = []
    color_mapping = get_color_mapping()
    if (card_list):
        if no_card_found == True and characterstic_list:
            # pick the other characterstic
            # first the color
            if 'color' in characterstic_list and len(characterstic_list['color']) == 1:
                suites = color_mapping[characterstic_list['color']].split(',')
                for suite in suites:
                    for card in card_list:
                        if suite in card:
                            negative_card_list.append(card)

            # suite
            if 'suite' in characterstic_list:
                suit_card_list = []
                suite_characterstic = characterstic_list['suite'].split(',')
                if not negative_card_list:
                    negative_card_list = card_list
                for suite in suite_characterstic:
                    for card in negative_card_list:
                        if suite in card:
                            suit_card_list.append(card)
                if suit_card_list:
                    negative_card_list = suit_card_list
            # parity
            if 'even' in characterstic_list or 'odd' in characterstic_list:
                parity_list = []
                if 'even' in characterstic_list:
                    parity = True
                if 'odd' in characterstic_list:
                    parity = False
                
                if not negative_card_list:
                    negative_card_list = card_list
                for card in negative_card_list:
                    if parity == True:
                        if get_card_value(card) % 2==0:
                            parity_list.append(card)
                    elif parity == False:
                        if get_card_value(card)%2 !=0:
                            parity_list.append(card)
                if parity_list:
                    negative_card_list = parity_list
            
            # number        
            if 'numbers' in characterstic_list:
                numbers_card_list = []
                if not negative_card_list:
                    negative_card_list = card_list
                numeric_characterstic = characterstic_list['numbers'].split(',')
                for number in numeric_characterstic:
                    for card in negative_card_list:
                        if number in card:
                            numbers_card_list.append(card)
                if numbers_card_list:
                    negative_card_list = numbers_card_list

            # single card is found
            if len(negative_card_list) == 1:
                return negative_card_list[0]
            else:
                # multiple cards

                return random.choice(negative_card_list)
    if no_card_found == True:
        print('no card found')
        if card_list:
            return random.choice(card_list)
        else:
            return pick_random_card()

    return random.choice(negative_card_list)

def pick_next_negative_card(rule_list, last_rule_counter):
    '''
     This returns a negative card associated with the top rule by using an intersection of the
     card characterstics of the top rule. If there is no intersection found we just return a
     random card
    '''
    # print('-------------------rule_list-----------------------', rule_list)
    top_rule_list = []
    for rules in rule_list:
        top_rule_list.append(rules)

    print('-------------------top_rule_list-----------------------', top_rule_list)
    
    intersection_rule_list = {}
    numbers = {}
    colors = {}
    suites = {}
    even_list = {}
    odd_list = {}
    royal_list = {}
    not_royal_list = {}
    number_list =['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
    color_list =['C14','C15']
    black = ['C14']
    red = ['C15']
    suite_list = ['C16','C17','C18','C19']
    even = ['C20']
    odd = ['C21']
    royal = ['C22']
    not_royal = ['C23']

    for rules in top_rule_list:
        
        number_list =['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
        for rule in rules:
            # put out negative of the current card card characterstic
            
            # numbers
            if (rule[len(rule)-1] in number_list):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in numbers.keys():
                    numbers[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else:
                    numbers[map_card_characteristic_to_value(rule[len(rule)-1])] += 1
            
            #colors
            if (rule[len(rule)-1] in color_list):

                if map_card_characteristic_to_value(rule[len(rule)-1]) not in colors.keys():
                    colors[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else:
                    colors[map_card_characteristic_to_value(rule[len(rule)-1])] += 1

            #suites
            if (rule[len(rule)-1] in suite_list):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in suites.keys():
                    suites[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else:
                    suites[map_card_characteristic_to_value(rule[len(rule)-1])] += 1

            #even
            if (rule[len(rule)-1] in even):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in even_list.keys():
                    even_list[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else: 
                    even_list[map_card_characteristic_to_value(rule[len(rule)-1])] += 1

            #odd
            if (rule[len(rule)-1] in odd):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in odd_list.keys():
                    odd_list[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else:
                    odd_list[map_card_characteristic_to_value(rule[len(rule)-1])] += 1

            #royal
            if (rule[len(rule)-1] in royal):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in royal_list.keys():
                    royal_list[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else:
                    royal_list[map_card_characteristic_to_value(rule[len(rule)-1])] += 1

            #not_royal
            if (rule[len(rule)-1] in not_royal):
                if map_card_characteristic_to_value(rule[len(rule)-1]) not in not_royal_list.keys():
                    not_royal_list[map_card_characteristic_to_value(rule[len(rule)-1])] = 1
                else: 
                    not_royal_list[map_card_characteristic_to_value(rule[len(rule)-1])] += 1
    card_characterstic_list = {}
    print('-------------------numbers-----------------------', numbers)
    if (numbers):
        card_characterstic_list['numbers'] = ','.join(numbers)

    print('-------------------colors-----------------------', colors)
    if (colors):
        
        card_characterstic_list['color'] = ','.join(max_dict(colors))

    print('-------------------suites-----------------------')
    if (suites):
        card_characterstic_list['suite'] = ','.join(suites)

    # merge both list together
    even_odd_list_merged = even_list.copy()
    even_odd_list_merged.update(odd_list)

    
    if (even_odd_list_merged):
        max_even_odd_list = max_dict(even_odd_list_merged)
        if ('odd' in max_even_odd_list):
            card_characterstic_list['odd'] = True
        elif ('even' in max_even_odd_list):
            card_characterstic_list['even'] = True
        else:
            card_characterstic_list['even'] = True
            card_characterstic_list['odd'] = True

    royal_non_royal_list = royal_list.copy()
    royal_non_royal_list.update(not_royal_list)
    if (royal_non_royal_list):        
        max_royal_non_royal_list = max_dict(royal_non_royal_list)
        if ('royal' in max_royal_non_royal_list):
            card_characterstic_list['royal'] = True
        elif ('not_royal' in max_royal_non_royal_list):
            card_characterstic_list['not_royal'] = True
        else:
            card_characterstic_list['royal'] = True
            card_characterstic_list['not_royal'] = True
    return pick_negative_random(card_characterstic_list, last_rule_counter)

def max_dict(dict):
    hash_table = {}
    max_value = dict[dict.keys()[0]]
    for dic in dict:
        if (max_value < dict[dic]):
            max_value = dict[dic]
    
    max_value_list = []

    for dic in dict:
        if (dict[dic] == max_value):
            max_value_list.append(dic)
    
    return max_value_list
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
