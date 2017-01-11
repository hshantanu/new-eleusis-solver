# Team Name: Guess My Rule! 

# Members: 
# Vipin Pillai
# Sailakshmi Pisupati
# Rahul Raghavan
# Shantanu Hirlekar


class HypothesisRankParams:
	def __init__(self, weight, occurrence):
		self.weight = weight
		self.occurrence = occurrence

	def set_weight(self, weight):
		self.weight = weight

	def get_weight(self):
		return self.weight

	def increment_occurrence(self):
		self.occurrence += 1

	def decrement_occurrence(self):
		self.occurrence -= 1

	def get_weighted_product(self):
		return self.weight*self.occurrence
