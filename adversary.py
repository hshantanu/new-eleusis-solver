from random import randint
class Adversary(object):

	def __init__(self):
		self.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
		self.suits = ["S", "H", "D", "C"]
		self.conditions = ["equal", "greater"]
		self.properties = ["suit", "value"]
		
	def play(self):
		# Plays a random card
		return self.values[randint(0,len(self.values)-1)] + self.suits[randint(0,len(self.suits)-1)]
		# Pick a best from the given set of cards in hand and not random.
	
	def guessRule(self):
		# Guesses a rule
		# check if the guess is correct or matches the proximity of the rule.
		rule = "if("
		for i in range(3):
			cond = self.conditions[randint(0,len(self.properties)-1)]
			if cond == "greater":
				prop = "value"
			else:
				prop = self.properties[randint(0,len(self.properties)-1)]
			
			rule += cond + "(" + prop + "(current), " + prop + "(previous)), "
			
		return rule[:-2]+")"
		
	
a = Adversary()
# print a.play()
# print a.guessRule()
