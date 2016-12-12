# Team Name: Guess My Rule! 

# Members: 
# Vipin Pillai
# Sailakshmi Pisupati
# Rahul Raghavan
# Shantanu Hirlekar


import random
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


            for characteristic_tuple in itertools.product(*combined_char_indices_list):

                # or logic
                or_tuple = (characteristic_tuple[0], characteristic_tuple[1], characteristic_tuple[2])
                or_characterstic_tuple = (or_tuple, orf_flag)

                normalized_or_wt_sum = (weighted_property_dict[or_tuple[0]]+weighted_property_dict[or_tuple[1]] + weighted_property_dict[or_tuple[2]])/3
                if (or_tuple[0] in combined_char_indices_list[0] or or_tuple[1] in combined_char_indices_list[1] or or_tuple[2] in combined_char_indices_list[2]):
                    if or_characterstic_tuple in hypothesis_dict.keys():
                        hypothesis_dict[or_characterstic_tuple].increment_occurrence()
                    else:
                        hypothesis_dict[or_characterstic_tuple] = HypothesisRankParams(normalized_or_wt_sum, 1)
                mean += normalized_or_wt_sum
                
                #And logic
                normalized_and_wt_sum = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
                if characteristic_tuple in hypothesis_dict.keys():
                    hypothesis_dict[characteristic_tuple].increment_occurrence()
                else:
                    hypothesis_dict[characteristic_tuple] = HypothesisRankParams(normalized_and_wt_sum, 1)
                mean += normalized_and_wt_sum

        
    hypothesis_occurrence_count = {}

    for i in xrange(begin_index+2, legal_length):
        #Now we have individual chars in characteristic_index_list[i]
        #Decide on how to formulate hypothesis
        combined_char_indices_list = [char_dict[i-1], char_dict[i]]

        for characteristic_tuple in itertools.product(*combined_char_indices_list):

            # or logic
            or_tuple = (characteristic_tuple[0], characteristic_tuple[1])
            or_characterstic_tuple = (or_tuple, orf_flag)

            normalized_or_wt_sum = (weighted_property_dict[or_tuple[0]]+weighted_property_dict[or_tuple[1]])/2
            if (or_tuple[0] in combined_char_indices_list[0] or or_tuple[1] in combined_char_indices_list[1]):
                if or_characterstic_tuple in hypothesis_dict.keys():
                    hypothesis_dict[or_characterstic_tuple].increment_occurrence()
                else:
                    hypothesis_dict[or_characterstic_tuple] = HypothesisRankParams(normalized_or_wt_sum, 1)
            mean += normalized_or_wt_sum
            # and logic
            normalized_and_wt_sum = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2
            if characteristic_tuple in hypothesis_dict.keys():
                hypothesis_dict[characteristic_tuple].increment_occurrence()
            else:
                hypothesis_dict[characteristic_tuple] = HypothesisRankParams(normalized_and_wt_sum, 1)

            mean += normalized_and_wt_sum
        
    ranked_hypothesis_dict = OrderedDict(sorted(hypothesis_dict.items(), key = lambda (key, value) : (value, key), reverse=True))
        
    hypothesis_offset = len(ranked_hypothesis_dict)
    if hypothesis_offset == 0:
        hypothesis_offset = 1 
    mean_cutoff = mean/hypothesis_offset
    ranked_hypothesis = {} 
    for value in ranked_hypothesis_dict.iteritems():
        if value[1] > mean_cutoff :
            ranked_hypothesis[value[0]] = value[1]
        else:
            break

    begin_index = legal_length-2

    #TODO eliminate conflicting hypothesis- ex: consecutive Royal/B/Odd & Non-Royal/R/Even. Check if already handled by pick_negative
    #Using illegal cards to eliminate possible hypothesis
    illegal_tuple_list = parse_illegal_indices()
    
    for elem in illegal_tuple_list:
        if len(elem) > 2 and three_length_hypothesis_flag:
            prev2 = elem[0]
            prev = elem[1]
            curr = elem[2]

            combined_char_indices_list = [get_card_mapping_characterstic(prev2), get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]

            hypothesis_occurrence_count = {}
            
            for characteristic_tuple in itertools.product(*combined_char_indices_list):
                or_tuple = (characteristic_tuple[0], characteristic_tuple[1], characteristic_tuple[2])
                or_characterstic_tuple = (or_tuple, orf_flag)
                normalized_or_wt_sum = (weighted_property_dict[or_tuple[0]]+weighted_property_dict[or_tuple[1]] + weighted_property_dict[or_tuple[2]])/3
                if (or_tuple[0] not in combined_char_indices_list[0] and or_tuple[1] not in combined_char_indices_list[1] and or_tuple[2] not in combined_char_indices_list[2]):
                        if or_characterstic_tuple in ranked_hypothesis.keys():
                            ranked_hypothesis[or_characterstic_tuple].decrement_occurrence()

                normalized_and_wt_sum = (weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]]+weighted_property_dict[characteristic_tuple[2]])/3
                if(len(characteristic_tuple)>2):
                    if characteristic_tuple in ranked_hypothesis.keys():
                        ranked_hypothesis[characteristic_tuple].decrement_occurrence()

        else:
            prev = elem[0]
            curr = elem[1]

            hypothesis_occurrence_count = {}
            combined_char_indices_list = [get_card_mapping_characterstic(prev), get_card_mapping_characterstic(curr)]
            for characteristic_tuple in itertools.product(*combined_char_indices_list):
                or_tuple = (characteristic_tuple[0], characteristic_tuple[1])
                or_characterstic_tuple = (or_tuple, orf_flag)
                
                # or logic for illegal cards
                if ((len(or_characterstic_tuple)>1) and (len(or_characterstic_tuple)<=2)):
                    normalized_or_wt_sum = (weighted_property_dict[or_tuple[0]]+weighted_property_dict[or_tuple[1]])/2
                    if (or_tuple[0] not in combined_char_indices_list[0] and or_tuple[1] not in combined_char_indices_list[1]):
                        if or_characterstic_tuple in ranked_hypothesis.keys():
                            ranked_hypothesis[or_characterstic_tuple].decrement_occurrence()

                    # and logic
                if ((len(characteristic_tuple)>1) and (len(characteristic_tuple)<=2)):
                    if characteristic_tuple in ranked_hypothesis.keys():
                        if characteristic_tuple in hypothesis_occurrence_count:
                            hypothesis_occurrence_count[characteristic_tuple] += 1
                        else:
                            hypothesis_occurrence_count[characteristic_tuple] = 1
                        ranked_hypothesis[characteristic_tuple] -= ((weighted_property_dict[characteristic_tuple[0]]+weighted_property_dict[characteristic_tuple[1]])/2)*hypothesis_occurrence_count[characteristic_tuple]

    ranked_hypothesis = OrderedDict(sorted(ranked_hypothesis.items(), key = lambda (key, value) : (value, key), reverse=True))

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
    pruned_ranked_hypothesis_list = []
    for comb in combinations(pruned_ranked_hypothesis, 3):
        # pruned_ranked_hypothesis_list.append(comb)
        rule1 = tree_transform(comb[0])
        rule2 = tree_transform(comb[1])
        rule3 = tree_transform(comb[2])
        pruned_ranked_hypothesis_list.append(Tree(andf, rule1, rule2, rule3))
        pruned_ranked_hypothesis_list.append(Tree(orf, rule1, rule2, rule3))
        pruned_ranked_hypothesis_list.append(Tree(andf, rule1, Tree(orf, rule2, rule3)))
        pruned_ranked_hypothesis_list.append(Tree(andf, rule2, Tree(orf, rule1, rule3)))
        pruned_ranked_hypothesis_list.append(Tree(andf, rule3, Tree(orf, rule1, rule2)))
        pruned_ranked_hypothesis_list.append(Tree(orf, rule1, Tree(andf, rule2, rule3)))
        pruned_ranked_hypothesis_list.append(Tree(orf, rule2, Tree(andf, rule1, rule3)))
        pruned_ranked_hypothesis_list.append(Tree(orf, rule3, Tree(andf, rule1, rule2)))


    for comb in combinations(pruned_ranked_hypothesis, 2):
        # pruned_ranked_hypothesis_list.append(comb)
        rule1 = tree_transform(comb[0])
        rule2 = tree_transform(comb[1])
        pruned_ranked_hypothesis_list.append(Tree(andf, rule1, rule2))
        pruned_ranked_hypothesis_list.append(Tree(orf, rule1, rule2))

    for hypo in pruned_ranked_hypothesis:
        rule = tree_transform(hypothesis)    
        pruned_ranked_hypothesis_list.append(rule)
    
    pruned_ranked_hypothesis_dict = {}
    pruned_ranked_hypothesis_index = {}
    mean = 0.0
    for tuple_elem in pruned_ranked_hypothesis_list:
        if len(tuple_elem) == 3:
            for i in xrange(2, len(legal_cards)):
                occurrence_flag = False
                accumulated_weight = 0.0
                if len(tuple_elem[0]) == 3 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][2] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]] + weighted_property_dict[tuple_elem[0][2]]) / 3
                    if len(tuple_elem[1]) == 3 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]]) / 3
                        if len(tuple_elem[2]) == 3 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]]) / 3
                            occurrence_flag = True
                        elif len(tuple_elem[2]) == 2 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]]) / 2
                            occurrence_flag = True
                    elif len(tuple_elem[1]) == 2 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]]) / 2
                        if len(tuple_elem[2]) == 3 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]]) / 3
                            occurrence_flag = True
                        elif len(tuple_elem[2]) == 2 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]]) / 2
                            occurrence_flag = True
                elif len(tuple_elem[0]) == 2 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[1][1]]) / 2
                    if len(tuple_elem[1]) == 3 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]]) / 3
                        if len(tuple_elem[2]) == 3 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]]) / 3
                            occurrence_flag = True
                        elif len(tuple_elem[2]) == 2 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]]) / 2
                            occurrence_flag = True
                    elif len(tuple_elem[1]) == 2 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]]) / 2
                        if len(tuple_elem[2]) == 3 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][2] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]] + weighted_property_dict[tuple_elem[2][2]]) / 3
                            occurrence_flag = True
                        elif len(tuple_elem[2]) == 2 and tuple_elem[2][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[2][1] in get_card_mapping_characterstic(legal_cards[i]):
                            accumulated_weight += (weighted_property_dict[tuple_elem[2][0]] + weighted_property_dict[tuple_elem[2][1]]) / 2
                            occurrence_flag = True
                if occurrence_flag:
                    if tuple_elem in pruned_ranked_hypothesis_dict:
                        pruned_ranked_hypothesis_dict[tuple_elem] += accumulated_weight / 3
                    else:
                        pruned_ranked_hypothesis_dict[tuple_elem] = accumulated_weight / 3
                    legal_tuple = (i - 2, i - 1, i)
                    if tuple_elem in pruned_ranked_hypothesis_index:
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    else:
                        pruned_ranked_hypothesis_index[tuple_elem] = []
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    mean += accumulated_weight / 3

        elif len(tuple_elem) == 2:
            for i in xrange(2, len(legal_cards)):
                occurrence_flag = False
                accumulated_weight = 0.0
                if len(tuple_elem[0]) == 3 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][2] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]] + weighted_property_dict[tuple_elem[0][2]]) / 3
                    if len(tuple_elem[1]) == 3 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]]) / 3
                        occurrence_flag = True
                    elif len(tuple_elem[1]) == 2 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]]) / 2
                        occurrence_flag = True
                elif len(tuple_elem[0]) == 2 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]]) / 2
                    if len(tuple_elem[1]) == 3 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][2] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]] + weighted_property_dict[tuple_elem[1][2]]) / 3
                        occurrence_flag = True
                    elif len(tuple_elem[1]) == 2 and tuple_elem[1][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[1][1] in get_card_mapping_characterstic(legal_cards[i]):
                        accumulated_weight += (weighted_property_dict[tuple_elem[1][0]] + weighted_property_dict[tuple_elem[1][1]]) / 2
                        occurrence_flag = True
                if occurrence_flag:
                    if tuple_elem in pruned_ranked_hypothesis_dict:
                        pruned_ranked_hypothesis_dict[tuple_elem] += accumulated_weight / 2
                    else:
                        pruned_ranked_hypothesis_dict[tuple_elem] = accumulated_weight / 2
                    legal_tuple = (i - 2, i - 1, i)
                    if tuple_elem in pruned_ranked_hypothesis_index:
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    else:
                        pruned_ranked_hypothesis_index[tuple_elem] = []
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    mean += accumulated_weight / 2

        elif len(tuple_elem) == 1:
            for i in xrange(2, len(legal_cards)):
                occurrence_flag = False
                accumulated_weight = 0.0
                if len(tuple_elem[0]) == 3 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 2]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][2] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]] + weighted_property_dict[tuple_elem[0][2]]) / 3
                    occurrence_flag = True
                elif len(tuple_elem[0]) == 2 and tuple_elem[0][0] in get_card_mapping_characterstic(legal_cards[i - 1]) and tuple_elem[0][1] in get_card_mapping_characterstic(legal_cards[i]):
                    accumulated_weight += (weighted_property_dict[tuple_elem[0][0]] + weighted_property_dict[tuple_elem[0][1]]) / 2
                    occurrence_flag = True
                if occurrence_flag:
                    if tuple_elem in pruned_ranked_hypothesis_dict:
                        pruned_ranked_hypothesis_dict[tuple_elem] += accumulated_weight / 2
                    else:
                        pruned_ranked_hypothesis_dict[tuple_elem] = accumulated_weight / 2
                    legal_tuple = (i - 2, i - 1, i)
                    if tuple_elem in pruned_ranked_hypothesis_index:
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    else:
                        pruned_ranked_hypothesis_index[tuple_elem] = []
                        pruned_ranked_hypothesis_index[tuple_elem].append(legal_tuple)
                    mean += accumulated_weight / 2

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

def scan_and_rank_numeric_hypothesis(three_length_hypothesis_flag):
    hypothesis_dict = {}
    board_state = parse_board_state()
    legal_cards = board_state['legal_cards']
    print str(legal_cards)
    characteristic_index_list = []
    weighted_property_dict = set_characteristic_weights()
    mean = 0.0
    if three_length_hypothesis_flag:
        for i in xrange(2, len(legal_cards)):
            numeric_relation_list = find_numeric_characteristic_relation(legal_cards[i - 2], legal_cards[i - 1], legal_cards[i])
            print 'Numeric Relation List: ' + str(numeric_relation_list)
            for numeric_relation in numeric_relation_list:
                if numeric_relation in hypothesis_dict.keys():
                    hypothesis_dict[numeric_relation] += 1
                else:
                    hypothesis_dict[numeric_relation] = 1
                mean += 1

    for i in xrange(1, len(legal_cards)):
        numeric_relation_list = find_numeric_characteristic_relation(prev_card=legal_cards[i - 1], current_card=legal_cards[i])
        numeric_relation_list = list((str(x) for x in numeric_relation_list))
        for numeric_relation in numeric_relation_list:
            if numeric_relation in hypothesis_dict.keys():
                hypothesis_dict[numeric_relation] += 1
            else:
                hypothesis_dict[numeric_relation] = 1
            mean += 1

    hypothesis_offset = len(hypothesis_dict)
    mean_cutoff = 0
    numeric_ranked_hypothesis = {}
    for value in hypothesis_dict.iteritems():
        if value[1] > mean_cutoff:
            numeric_ranked_hypothesis[value[0]] = value[1]
        else:
            break

    illegal_tuple_list = parse_illegal_indices()
    for elem in illegal_tuple_list:
        if len(elem) > 2 and three_length_hypothesis_flag:
            prev2 = elem[0]
            prev = elem[1]
            curr = elem[2]
            numeric_relation_list = find_numeric_characteristic_relation(prev2, prev, curr)
            for numeric_relation in numeric_relation_list:
                if numeric_relation in numeric_ranked_hypothesis.keys():
                    numeric_ranked_hypothesis[numeric_relation] -= 1

        else:
            prev = elem[0]
            curr = elem[1]
            numeric_relation_list = find_numeric_characteristic_relation(prev_card=prev, current_card=curr)
            for numeric_relation in numeric_relation_list:
                if numeric_relation in numeric_ranked_hypothesis.keys():
                    numeric_ranked_hypothesis[numeric_relation] -= 1

    numeric_ranked_hypothesis = OrderedDict(sorted(numeric_ranked_hypothesis.items(), key=lambda (key, value): (value, key), reverse=True))
    return numeric_ranked_hypothesis
