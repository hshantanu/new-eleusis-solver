from NewEleusisHelper import *
from New_Eleusis import *

import random

players_hand_card={}
def get_number_of_player():
	number_of_player =1
	return number_of_player

def get_number_of_adversaries():
	number_of_adversary=2
	return number_of_adversary

def initialize_player():
	number_of_player = get_number_of_player()
	initialize_player_cards(number_of_player,players_hand_card)

def initialize_player_cards(number_of_player,players_hand_card):	
	number_of_cards_per_player=14
	for i in xrange(number_of_player):
		players_hand_card['P'+str(i)]=get_card_list(number_of_cards_per_player)
	print "Players hand cards ",players_hand_card


def get_card_list(number_of_cards_per_player):
	player_card_list=[]
	for j in range(number_of_cards_per_player):
		player_card_list.append(pick_random_card())
	return player_card_list

def player_card_play(number_of_player):
	for i in range(number_of_player):
		card = pick_player_card(players_hand_card['P'+str(i)],i)
		return card

def pick_player_card(players_hand_card,player_number):
	print "Player",player_number," deck before play ",players_hand_card
	card = random.choice(players_hand_card)
	players_hand_card.remove(card)
	players_hand_card.append(pick_random_card())
	print "Player",player_number," deck after play ",players_hand_card
	return card

def get_player_card_list(player):
	for player in players_hand_card:
		print "Player hand card",players_hand_card[str(player)]
	return players_hand_card[str(player)]