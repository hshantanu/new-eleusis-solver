class Exception_Hypothesis:
	def __init__(self, previous2 = None, previous = None, current = None):
		#Here, the position specific flag indicates whether the exception evaluation should be enabled for this position
		self.previous2Flag = False
		self.previousFlag = False
		self.currentFlag = False
		
		if previous2:
			self.previous2Flag = True
			self.previous2 = previous2
		if previous:
			self.previousFlag = True
			self.previous = previous
		if current:
			self.currentFlag = True
			self.current = current
