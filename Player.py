from New_Eleusis import *
from NewEleusisHelper import *

import random
global game_ended
game_ended = False

players_hand_card={}
class Player: 
	def __init__(self):
		self.hand = self.get_card_list(14)
	
	def update_hand(self, card):
		print 'Player playing ' + str(self.hand)
		print str(card)
		self.hand.remove(card)
		self.hand.append(pick_random_card())

	def get_number_of_adversaries(self):
		number_of_adversary=2
		return number_of_adversary

	def get_card_list(self, number_of_cards_per_player):
		player_card_list=[]
		for j in range(number_of_cards_per_player):
			player_card_list.append(pick_random_card())
		return player_card_list

	def player_card_play(self):
		return self.pick_player_card()

	def pick_player_card(self):
		card = random.choice(self.hand)
		self.hand.remove(card)
		self.hand.append(pick_random_card())
		return card

	def play(self, cards=None):
		return play_player_card(self, cards, self.hand)

	def get_player_card_list(self, player):
		for player in players_hand_card:
			print "Player hand card",players_hand_card[str(player)]
		return players_hand_card[str(player)]
