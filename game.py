
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

game_end_player = False
for round_num in range(14):
    # Each player plays a card or guesses a rule
    player_cards = []
    if round_num == 1:
        player_cards = cards
    if (not is_tree_instance(player.play(player_cards))):
        if (not is_tree_instance(adversary1.play())):
            if (not is_tree_instance(adversary2.play())):
                if (not is_tree_instance(adversary3.play())):
                    continue
                else:
                    game_end_player = adversary3
                    game_ended = True
                    break
            else:
                game_end_player = adversary2
                game_ended = True
                break

        else:
            game_end_player = adversary1                        
            game_ended = True
            break
    else:
        game_end_player = player
        game_ended = True
        break

player_list = [player, adversary1, adversary2, adversary3]
player_scores={player:0, adversary1:0,adversary2:0,adversary3:0}
for key in player_list:
    key_rule = key.play()
    result_score = score(key_rule,player_scores, key, game_end_player)
    print 'Score for ' + str(key.__class__.__name__) + ':  ' + str(result_score)    
print "Exited"
