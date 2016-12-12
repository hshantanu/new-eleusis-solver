# Team Name: Guess My Rule! 

# Members: 
# Vipin Pillai
# Sailakshmi Pisupati
# Rahul Raghavan
# Shantanu Hirlekar


import random
import re
import operator
import itertools
from collections import OrderedDict
from itertools import combinations
import time
from NewEleusisHelper import *
from New_Eleusis import *


char_dict={}
begin_index = 0
hypothesis_dict = {}

current_dict = {}
previous_dict = {}
previous2_dict = {}


def scan_and_rank_hypothesis(three_length_hypothesis_flag):
    
    global hypothesis_dict
    global begin_index
    global char_dict

    orf_flag = True
    board_state = parse_board_state()
    legal_cards = board_state['legal_cards']
    legal_length = len(legal_cards)

    characteristic_index_list = []
    for i in xrange(begin_index, legal_length):
        update_characteristic_list(legal_cards[i], i, char_dict)

    weighted_property_dict = set_characteristic_weights()
    hypothesis_occurrence_count = {}
    
    mean = 0.0
    if three_length_hypothesis_flag:
        for i in xrange(begin_index+2, legal_length):

            combined_char_indices_list = [char_dict[i-2], char_dict[i-1], char_dict[i]]

            start_time = time.time()
            for characteristic_tuple in itertools.product(*combined_char_indices_list):
                generate_combination(characteristic_tuple[0], characteristic_tuple[1], characteristic_tuple[2])
        
    hypothesis_occurrence_count = {}

    for i in xrange(begin_index+2, legal_length):
        #Now we have individual chars in characteristic_index_list[i]
        #Decide on how to formulate hypothesis
        combined_char_indices_list = [char_dict[i-1], char_dict[i]]

        for characteristic_tuple in itertools.product(*combined_char_indices_list):
                generate_combination(None, characteristic_tuple[0], characteristic_tuple[1])
        
    ranked_hypothesis_dict = OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))

    cumulative_sum = 0.0
    for key, value in hypothesis_dict.iteritems():
        cumulative_sum += value
    
    hypothesis_offset = len(hypothesis_dict)
    
    if hypothesis_offset == 0:
        hypothesis_offset = 1 
    mean_cutoff = cumulative_sum/hypothesis_offset

    ranked_hypothesis = {} 
    for key, value in hypothesis_dict.iteritems():
        if value > mean_cutoff :
            ranked_hypothesis[key] = value
    
    ranked_hypothesis_dict = OrderedDict(sorted(ranked_hypothesis.items(), key = lambda (key, value) : (value, key), reverse=True))

    # print 'Current iteration status: ' + str(ranked_hypothesis_dict.iteritems()[0])
    begin_index = legal_length-2
    # exit()        

    #TODO eliminate conflicting hypothesis- ex: consecutive Royal/B/Odd & Non-Royal/R/Even. Check if already handled by pick_negative
    #Using illegal cards to eliminate possible hypothesis
    illegal_tuple_list = parse_illegal_indices()
    
    for elem in illegal_tuple_list:
        if len(elem) > 2 and three_length_hypothesis_flag:
            prev2 = elem[0]
            prev = elem[1]
            curr = elem[2]

            combined_char_indices_list = [get_card_mapping_characterstic(prev2), get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]

            for characteristic_tuple in itertools.product(*combined_char_indices_list):
                generate_combination(characteristic_tuple[0], characteristic_tuple[1], characteristic_tuple[2], is_illegal=True)
        else:
            prev = elem[0]
            curr = elem[1]

            combined_char_indices_list = [get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]
            for characteristic_tuple in itertools.product(*combined_char_indices_list):
                generate_combination(None, characteristic_tuple[0], characteristic_tuple[1], is_illegal=True)

    ranked_hypothesis = OrderedDict(sorted(ranked_hypothesis.items(), key = lambda (key, value) : (value, key), reverse=True))

    # print str(ranked_hypothesis_dict) + '  ' + str(cumulative_sum) + '   ' +  str(len(hypothesis_dict)) + '  ' + str(mean_cutoff)
    # exit()
    return ranked_hypothesis


def scan_and_rank_rules(ranked_hypothesis, numeric_hypothesis = []):
    board_state = parse_board_state()
    weighted_property_dict = set_characteristic_weights()
    legal_cards = board_state['legal_cards']
    ranked_rules_list = []
    for value in ranked_hypothesis.iteritems():
        ranked_rules_list.append(value[0])

    #dict = {'and(previous=C2,current=C3)':12, 'or(previous=C2,current=C3)':3}
    pruned_ranked_hypothesis = ranked_rules_list[0:5]
    pruned_ranked_hypothesis_dict = {}
    for comb in combinations(pruned_ranked_hypothesis, 3):
        # pruned_ranked_hypothesis_dict.append(comb)
        rule1 = tree_transform(comb[0])
        rule2 = tree_transform(comb[1])
        rule3 = tree_transform(comb[2])
        pruned_ranked_hypothesis_dict[Tree(andf, rule1, rule2, rule3)]
        pruned_ranked_hypothesis_dict[Tree(orf, rule1, rule2, rule3)]
        pruned_ranked_hypothesis_dict[Tree(andf, rule1, Tree(orf, rule2, rule3))]
        pruned_ranked_hypothesis_dict[Tree(andf, rule2, Tree(orf, rule1, rule3))]
        pruned_ranked_hypothesis_dict[Tree(andf, rule3, Tree(orf, rule1, rule2))]
        pruned_ranked_hypothesis_dict[Tree(orf, rule1, Tree(andf, rule2, rule3))]
        pruned_ranked_hypothesis_dict[Tree(orf, rule2, Tree(andf, rule1, rule3))]
        pruned_ranked_hypothesis_dict[Tree(orf, rule3, Tree(andf, rule1, rule2))]


    for comb in combinations(pruned_ranked_hypothesis, 2):
        # pruned_ranked_hypothesis_dict[comb]
        rule1 = tree_transform(comb[0])
        rule2 = tree_transform(comb[1])
        pruned_ranked_hypothesis_dict[Tree(andf, rule1, rule2)]
        pruned_ranked_hypothesis_dict[Tree(orf, rule1, rule2)]

    for hypo in pruned_ranked_hypothesis:
        rule = tree_transform(hypothesis)    
        pruned_ranked_hypothesis_dict[rule]
    
    pruned_ranked_hypothesis_dict = {}
    pruned_ranked_hypothesis_index = {}
    mean = 0.0
    for i in xrange(2, len(legal_cards)):
        for rule in pruned_ranked_hypothesis_dict:
            if (rule.evaluate(legal_cards[i-2], legal_cards[i-1], legal_cards[i])):
                #Increment rank of rule
                pass
    hypothesis_offset = len(pruned_ranked_hypothesis_dict)
    if hypothesis_offset == 0:
        hypothesis_offset = 1
    mean_cutoff = mean / hypothesis_offset
    pr_ranked_hypothesis = {}
    for key in pruned_ranked_hypothesis_dict.keys():
        if pruned_ranked_hypothesis_dict[key] < mean_cutoff:
            del pruned_ranked_hypothesis_dict[key]
            del pruned_ranked_hypothesis_index[key]

    print str(pruned_ranked_hypothesis_index)
    pr_ranked_hypothesis = OrderedDict(sorted(pruned_ranked_hypothesis_dict.items(), key=lambda (key, value): (value, key), reverse=True))
    return pr_ranked_hypothesis

def scan_and_rank_numeric_hypothesis(three_length_hypothesis_flag,):
    hypothesis_dict = {}
    board_state = parse_board_state()
    master_board_state = get_master_board_state()
    legal_cards_list = board_state['legal_cards']
    print "Legal card list",legal_cards_list
    illegal_cards_list = parse_illegal_indices()
    curr = board_state['curr']
    prev1 = board_state['prev']
    prev2 = board_state['prev2']
    print "Current is ", curr,' Previous is ',prev1,' Previous 2 is ',prev2
    print "Master board state",master_board_state

    # print "Legal cards",legal_cards_list
    # print "Illegal cards",illegal_cards_list
    for i in board_state:
        print "i",i
    for i in range(len(board_state)):
        for i in board_state:
            curr = board_state['curr']
            prev1 = board_state['prev']
            prev2 = board_state['prev2']
            print "Current is ", curr,' Previous is ',prev1,' Previous 2 is ',prev2
    get_numerical_range_relation(board_state)

    characteristic_index_list = []
    weighted_property_dict = set_characteristic_weights()
    mean = 0.0
    # if three_length_hypothesis_flag:
    #     for i in xrange(2, len(board_state)):
    #         numeric_relation_list = find_numeric_characteristic_relation(board_state[i - 2], board_state[i - 1], board_state[i])
    #         print 'Numeric Relation List: ' + str(numeric_relation_list)
    #         for numeric_relation in numeric_relation_list:
    #             if numeric_relation in hypothesis_dict.keys():
    #                 hypothesis_dict[numeric_relation] += 1
    #             else:
    #                 hypothesis_dict[numeric_relation] = 1
    #             mean += 1

    # for i in xrange(1, len(board_state)):
    #     numeric_relation_list = find_numeric_characteristic_relation(prev_card=board_state[i - 1], current_card=board_state[i])
    #     numeric_relation_list = list((str(x) for x in numeric_relation_list))
    #     for numeric_relation in numeric_relation_list:
    #         if numeric_relation in hypothesis_dict.keys():
    #             hypothesis_dict[numeric_relation] += 1
    #         else:
    #             hypothesis_dict[numeric_relation] = 1
    #         mean += 1

    # legal_cards = board_state['legal_cards']
    # print "Board state:",board_state
    # print "legal state:", legal_cards
    # print str(legal_cards)
    # characteristic_index_list = []
    # weighted_property_dict = set_characteristic_weights()
    # mean = 0.0
    # if three_length_hypothesis_flag:
    #     for i in xrange(2, len(legal_cards)):
    #         numeric_relation_list = find_numeric_characteristic_relation(legal_cards[i - 2], legal_cards[i - 1], legal_cards[i])
    #         print 'Numeric Relation List: ' + str(numeric_relation_list)
    #         for numeric_relation in numeric_relation_list:
    #             if numeric_relation in hypothesis_dict.keys():
    #                 hypothesis_dict[numeric_relation] += 1
    #             else:
    #                 hypothesis_dict[numeric_relation] = 1
    #             mean += 1

    # for i in xrange(1, len(legal_cards)):
    #     numeric_relation_list = find_numeric_characteristic_relation(prev_card=legal_cards[i - 1], current_card=legal_cards[i])
    #     numeric_relation_list = list((str(x) for x in numeric_relation_list))
    #     for numeric_relation in numeric_relation_list:
    #         if numeric_relation in hypothesis_dict.keys():
    #             hypothesis_dict[numeric_relation] += 1
    #         else:
    #             hypothesis_dict[numeric_relation] = 1
    #         mean += 1

    # hypothesis_offset = len(hypothesis_dict)
    # mean_cutoff = 0
    # numeric_ranked_hypothesis = {}
    # for value in hypothesis_dict.iteritems():
    #     if value[1] > mean_cutoff:
    #         numeric_ranked_hypothesis[value[0]] = value[1]
    #     else:
    #         break

    # illegal_tuple_list = parse_illegal_indices()
    # for elem in illegal_tuple_list:
    #     if len(elem) > 2 and three_length_hypothesis_flag:
    #         prev2 = elem[0]
    #         prev = elem[1]
    #         curr = elem[2]
    #         numeric_relation_list = find_numeric_characteristic_relation(prev2, prev, curr)
    #         for numeric_relation in numeric_relation_list:
    #             if numeric_relation in numeric_ranked_hypothesis.keys():
    #                 numeric_ranked_hypothesis[numeric_relation] -= 1

    #     else:
    #         prev = elem[0]
    #         curr = elem[1]
    #         numeric_relation_list = find_numeric_characteristic_relation(prev_card=prev, current_card=curr)
    #         for numeric_relation in numeric_relation_list:
    #             if numeric_relation in numeric_ranked_hypothesis.keys():
    #                 numeric_ranked_hypothesis[numeric_relation] -= 1

    # numeric_ranked_hypothesis = OrderedDict(sorted(numeric_ranked_hypothesis.items(), key=lambda (key, value): (value, key), reverse=True))
    # return numeric_ranked_hypothesis

def get_numerical_range_relation(board_state):
    print "Board state"

def add_elements(previous2_dict, previous_dict, current_dict, rule):
    values = get_elements(rule)

    if (values['previous2']):

        if values['previous2'] in previous2_dict:
            previous2_dict[values['previous2']].append(rule)
        else:
            previous2_dict[values['previous2']] = [rule]

    if (values['previous']):
        if values['previous'] in previous_dict:
            previous_dict[values['previous']].append(rule)
        else:
            previous_dict[values['previous']] = [rule]

    if (values['current']):
        if values['current'] in current_dict:
            current_dict[values['current']].append(rule)
        else:
            current_dict[values['current']] = [rule]


    
def get_elements(rule):
    previous = re.compile(".*((previous)=\'([C][1-9][0-9]?)\').*")
    
    if previous.match(rule):
        previous = previous.match(rule).group(3)

    else:
        previous = []
    previous2 = re.compile(".*((previous2)=\'([C][1-9][0-9]?)\').*")
    if  previous2.match(rule):
        previous2 =  previous2.match(rule).group(3)
    else:
        previous2 = []
    current = re.compile(".*((current)=\'([C][1-9][0-9]?)\').*")
    if current.match(rule):
        current = current.match(rule).group(3)
    else:
        current = []
    
    return {'previous': previous, 'current':current, 'previous2':previous2}

def get_key_value_pair_dict(dictionary):
    if (dictionary['current']):
        return current_dict, dictionary['current']
    if (dictionary['previous']):
        return previous_dict, dictionary['previous']
    if (dictionary['previous2']):
        return previous2_dict, dictionary['previous2']

def get_key_value_pair(dictionary):
    if (dictionary['current']):
        return 'current', dictionary['current']
    if (dictionary['previous']):
        return 'previous', dictionary['previous']
    if (dictionary['previous2']):
        return 'previous2', dictionary['previous2']

def parse_elements(rule):
    weighted_property_dict = set_characteristic_weights()
    sub_rule_tokens = ''
    if (rule.startswith('and')):
        sub_rule_tokens = rule[4:-1].split(',')
        if (('or' in sub_rule_tokens[1])):
            c0_dict,c0_value = get_key_value_pair_dict(get_elements(sub_rule_tokens[0]))
            # since this is an and value we add it to the weighted property hypothesis_dict
            value = weighted_property_dict[c0_value]
            c1_dict,c1_value = get_key_value_pair(get_elements(sub_rule_tokens[1]))
            
            c1_weighted_value = weighted_property_dict[c1_value]

            c2_dict,c2_value = get_key_value_pair_dict(get_elements(sub_rule_tokens[1]))
            
            c2_weighted_value = weighted_property_dict[c2_value]
            total_weight = (value + max(c1_weighted_value, c2_weighted_value))/2
            if rule in hypothesis_dict:
                hypothesis_dict[rule] += total_weight
            else:
                hypothesis_dict[rule] = total_weight
        
        else:
            # the logic only includes an and
            # check in the dictionary if the same value exist
            if (rule in hypothesis_dict):
                hypothesis_dict[rule] += hypothesis_dict[rule]
            else:
                hypothesis_dict[rule] = calculate_weight(get_elements(rule), True)

    elif(rule.startswith('or')):
        sub_rule_tokens = rule[3:-1]
        if ('and' in sub_rule_tokens[1]):
            c0_dict,c0_value = get_key_value_pair_dict(get_elements(sub_rule_tokens[0]))
            # since this is an and value we add it to the weighted property hypothesis_dict
            value = weighted_property_dict[c0_value]
            c1_dict,c1_value = get_key_value_pair(get_elements(sub_rule_tokens[1]))
            
            c1_weighted_value = weighted_property_dict[c1_value]

            c2_dict,c2_value = get_key_value_pair_dict(get_elements(sub_rule_tokens[1]))
            
            c2_weighted_value = weighted_property_dict[c2_value]
            total_weight = max(value, ((c1_weighted_value + c2_weighted_value)/2))
            if rule in hypothesis_dict:
                hypothesis_dict[rule] += total_weight
            else:
                hypothesis_dict[rule] = total_weight
        else:
            # the logic only includes an and
            # check in the dictionary if the same value exist
            if (rule in hypothesis_dict):
                hypothesis_dict[rule] += hypothesis_dict[rule]
            else:
                # calculate the weight
                hypothesis_dict[rule] = calculate_weight(get_elements(rule), False)

def get_hypothesis_by_characterstic(index_position_dict, characterstic):
    if characterstic in index_position_dict:
        return index_position_dict[characterstic]
    return None

def evaluate(index_position_dict, previous2, previous, current, key, is_illegal= False):
    weighted_property_dict = set_characteristic_weights()
    global hypothesis_dict

    if key == 'current':
        rule_list = get_hypothesis_by_characterstic(index_position_dict, current)
        weight_index = current
    elif key == 'previous':
        rule_list = get_hypothesis_by_characterstic(index_position_dict, previous)
        weight_index = previous
    elif key == 'previous2':
        rule_list = get_hypothesis_by_characterstic(index_position_dict, previous2)
        weight_index = previous2
    first_flag = False
    second_flag = False
    third_flag = False 
    for rule in rule_list:
        split_rule = rule.split(',')
        if split_rule[0].startswith('and'):
            key,value = get_key_value_pair(get_elements(split_rule[0]))
            if check_value(current, previous, previous2, key, value):
                first_flag = True
            if split_rule[1].startswith('or'):
                key,value = get_key_value_pair(get_elements(split_rule[1]))
                if check_value(current, previous, previous2, key, value):
                    second_flag = True
                key,value = get_key_value_pair(get_elements(split_rule[2]))
                if check_value(current, previous, previous2, key, value):
                    third_flag = True
                # perform normal 'and'
                if (first_flag and (second_flag or third_flag)):
                    if is_illegal:
                        hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                    else:
                        hypothesis_dict[rule] += weighted_property_dict[weight_index]
            elif not split_rule[1].startswith('or') and not split_rule[1].startswith('and'):
                key,value = get_key_value_pair(get_elements(split_rule[1]))
                if check_value(current, previous, previous2, key, value):
                    second_flag = True
                if len(split_rule)>2:
                    key,value = get_key_value_pair(get_elements(split_rule[2]))
                    if check_value(current, previous, previous2, key, value):
                        third_flag = True
                    if (first_flag and second_flag and third_flag):
                        if is_illegal:
                            hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                        else:
                            hypothesis_dict[rule] += weighted_property_dict[weight_index]
                else:
                    if (first_flag and second_flag):
                        if is_illegal:
                            hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                        else:
                            hypothesis_dict[rule] += weighted_property_dict[weight_index]
        elif split_rule[0].startswith('or'):
            key,value = get_key_value_pair(get_elements(split_rule[0]))
            if check_value(current, previous, previous2, key, value):
                first_flag = True
            if split_rule[1].startswith('and'):
                key,value = get_key_value_pair(get_elements(split_rule[1]))
                if check_value(current, previous, previous2, key, value):
                    second_flag = True
                key,value = get_key_value_pair(get_elements(split_rule[2]))
                if check_value(current, previous, previous2, key, value):
                    third_flag = True
                if (first_flag or (second_flag and third_flag)):
                    if is_illegal:
                        hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                    else:
                        hypothesis_dict[rule] += weighted_property_dict[weight_index]
            elif not split_rule[1].startswith('and') and not split_rule[1].startswith('or'):
                if split_rule[1].startswith('and'):
                    key,value = get_key_value_pair(get_elements(split_rule[1]))
                    if check_value(current, previous, previous2, key, value):
                        second_flag = True
                    if len(split_rule)>2:
                        key,value = get_key_value_pair(get_elements(split_rule[2]))
                        if check_value(current, previous, previous2, key, value):
                            third_flag = True
                        if (first_flag or second_flag or third_flag):
                            if is_illegal:
                                hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                            else:
                                hypothesis_dict[rule] += weighted_property_dict[weight_index]               
                else:
                    if (first_flag or second_flag):
                        if is_illegal:
                            hypothesis_dict[rule] -= weighted_property_dict[weight_index]    
                        else:
                            hypothesis_dict[rule] += weighted_property_dict[weight_index]

    
def check_value(current, previous, previous2, key, value):
    if key == 'current':
        return current == value
    if key == 'previous':
        return previous == value
    if key == 'previous2':
        return previous2 == value
    return False

def calculate_weight(values, and_flag):
    weighted_property_dict = set_characteristic_weights()
    dividend = 2
    # set to default 0 as we might have a 2 length rule as well
    previous2_weight = 0
    
    previous_weight = weighted_property_dict[values['previous']]
    current_weight = weighted_property_dict[values['current']]
    if (values['previous2']):
        previous2_weight = weighted_property_dict[values['previous2']]
        dividend = 3
    if and_flag:
        return ((current_weight+previous_weight+previous2_weight)/dividend)
    else:
        return max(current_weight, previous_weight, previous2_weight) 

def generate_combination(previous2, previous, current, is_illegal=False):
    global previous2_dict
    global previous_dict
    global current_dict
    characterstic_combination = []

    if previous2:
        if previous2 in previous2_dict:
            evaluate(previous2_dict, previous2, previous, current, "previous2", is_illegal)
    if previous:
        if previous in previous_dict:
            evaluate(previous_dict, previous2, previous, current, "previous", is_illegal)
    
    if current:
        if current in current_dict:
            evaluate(current_dict, previous2, previous, current, "current", is_illegal)

    if not is_illegal:
        if (previous2 == None):
            # two length hypothesis
            characterstic_combination.append("or(current='"+current+"',previous='"+previous+"')")
            characterstic_combination.append("and(current='"+current+"',previous='"+previous+"')")
        else:
            characterstic_combination.append("or(current='"+current+"',previous='"+previous+"',previous2='"+previous2+"')")
            characterstic_combination.append("and(current='"+current+"',previous='"+previous+"',previous2='"+previous2+"')")
            characterstic_combination.append("or(current='"+current+"',and(previous='"+previous+"',previous2='"+previous2+"'))")
            characterstic_combination.append("and(current='"+current+"',or(previous='"+previous+"',previous2='"+previous2+"'))")
            characterstic_combination.append("or(previous='"+previous+"',and(current='"+current+"',previous2='"+previous2+"'))")
            characterstic_combination.append("and(previous='"+previous+"',or(current='"+current+"',previous2='"+previous2+"'))")
            characterstic_combination.append("or(previous2='"+previous2+"',and(current='"+current+"',previous='"+previous+"'))")
            characterstic_combination.append("and(previous2='"+previous2+"',or(current='"+current+"',previous='"+previous+"'))")

        for rule in characterstic_combination:
            parse_elements(rule)
            add_elements(previous2_dict, previous_dict, current_dict, rule) 

    # merged_rules = list(set(prev_possible_rules) & set(curr_possible_rules))
    # for rule in merged_rules:
    #     evaluate(current_dict, previous2, previous, current, "current")