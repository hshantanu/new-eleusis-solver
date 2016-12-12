#Put your program name in place of program_name

from New_Eleusis import play_card
from New_Eleusis import score
from random import randint
# from new_eleusis import *
from Player import *

global game_ended
game_ended = False

def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[randint(0, len(values)-1)] + suits[randint(0, len(suits)-1)]

# class Player(object):
#     def __init__(self):
#         self.hand = [generate_random_card() for i in range(14)]

#     def play(self, cards):
#         """
#         'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
#         Your scientist should play a card out of its given hand OR return a rule, not both.
#         'game_ended' parameter is a flag that is set to True once the game ends. It is False by default
#         """
#         return scientist(self, cards, self.hand)

class Adversary(object):
    def __init__(self):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
        Your scientist should play a card out of its given hand.
        """
        # Return a rule with a probability of 1/14
        prob_list = [i for i in range(14)]
        prob = prob_list[randint(0, 13)]
        if False:
            # Generate a random rule
            rule = ""
            conditions = ["equal", "greater"]
            properties = ["suit", "value"]
            cond = conditions[randint(0,len(properties)-1)]
            if cond == "greater":
                prop = "value"
            else:
                prop = properties[randint(0,len(properties)-1)]

            rule += cond + "(" + prop + "(current), " + prop + "(previous)), "
            return rule[:-2]+")"
        else:
            next_card = self.hand[randint(0, len(self.hand)-1)]
            play_card(next_card)
            return next_card

# The players in the game
player = Player()
adversary1 = Adversary()
adversary2 = Adversary()
adversary3 = Adversary()

# Set a rule for testing
#rule = "iff(is_royal(current), False)"
rule = Tree(andf, Tree(equal, Tree(color, 'previous'), 'R'), Tree(equal, Tree(color, 'current'), 'B'))
setRule(rule)
# The three cards that adhere to the rule
cards = ["10H", "2C", "4S"]

def is_tree_instance(instance):
    return True if instance.__class__.__name__ == 'Tree' else False

for round_num in range(14):
    # Each player plays a card or guesses a rule
    print 'I\'m playing a rule : '
    if (not is_tree_instance(player.play(cards))) and (not is_tree_instance(adversary1.play())) and (not is_tree_instance(adversary2.play())) and (not is_tree_instance(adversary3.play())):
        continue
    else:
        game_ended = True
        break

print "Exited"
# Everyone has to guess a rule
rule_player = player.play()
print 'rule player: ' + str(rule_player)
# Check if the guessed rule is correct and print the score
result_score, player_won = score(rule_player)
print 'Score ' + str(result_score) 