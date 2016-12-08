import random
def generate():
	# rule =Tree(orf, Tree(equal, Tree(color, 'previous'), 'R'), Tree(equal, Tree(color, 'current'), 'R'))
	# rule = "Tree("+get_clause()+",Tree("+relation()+",Tree("+get_characteristic()+",'previous'),'"+")"

	clause = get_clause()
	relation = get_relation()
	characteristic = get_characteristic()
	rule=''

	if(characteristic=='suit'):
		rule = "Tree("+get_clause()+",Tree("+relation+",Tree("+characteristic+",'previous'),'"+random.choice(['H','S','D','C'])+"'), Tree("+relation+", Tree("+characteristic+",'current'),'"+random.choice(['H','S','D','C'])+"'))"
	elif(characteristic=='color'):
		rule = "Tree("+get_clause()+",Tree("+relation+",Tree("+characteristic+",'previous'),'"+random.choice(['R','B'])+"'), Tree("+relation+", Tree("+characteristic+",'current'),'"+random.choice(['R','B'])+"'))"
	elif(characteristic=='even' or characteristic=='odd'):
		rule = "Tree("+get_clause()+",Tree("+relation+",Tree("+characteristic+",'previous'), Tree("+relation+", Tree("+characteristic+",'current'))))"
	elif(characteristic=='royal' or characteristic=='not_royal'):
		rule = "Tree("+get_clause()+",Tree("+relation+",Tree("+characteristic+",'previous'), Tree("+relation+", Tree("+characteristic+",'current'))))"

	print rule


def get_clause():
	#iff to be added
	clauses=['andf','orf','notf']
	return random.choice(clauses)


def get_relation():
	relation=['equal']
	# relation=['equal','greater','less']
	return random.choice(relation)

def get_characteristic():
	# value is pending
	characteristic=['even','odd','royal','not_royal','suit','color']
	return random.choice(characteristic)

def print_rules():
	for i in range(1,50):
		generate()

print_rules()