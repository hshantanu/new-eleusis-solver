class HypothesisRankParams:
	def __init__(self, weight, occurrence):
		self.weight = weight
		self.occurrence = occurrence

	def set_weight(self, weight):
		self.weight = weight

	def increment_occurrence(occurrence):
		self.occurrence += 1

	def decrement_occurrence(occurrence):
		self.occurrence -= 1