import random

def pick_random_card():
	rank = random.choice( ('A','2','3','4','5','6','7','8','9','T','J','Q','K') )
	suit = random.choice( ('c','d','h','s') )
	card = rank + suit
	return card


print(pick_random_card())