# README #

In this project, we have developed an inductive reasoning based solver for the card game - [New Eleusis](https://en.wikipedia.org/wiki/Eleusis_(card_game)).

We have designed and implemented a probabilistic ranking algorithm which uses the existing board state as training data and formulates ranked hypotheses to predict the card rule using weighted card characteristics as the building blocks.

###Simplifications:###
1. Currently we do not support prophets, sudden death, playing multiple cards at once, hand limits or no-plays.
2. We assume that the scientist rule can only be composed of atmost 3 card positions - current, previous and the previous2 (the one before previous).

###Card characteristics:###
* Diamond, Heart, Spade, Club
* Red, Black
* Even, Odd
* Numeric Value ((Ace=1), 2, 3 ,4 ,5 ,6 ,7 ,8 ,9, 10, (Jack=11), (Queen=12), (King=13))
* Royal / Not Royal

###Strategy:###
1. We start by forming individual characteristic lists which will store the indices of the corresponding cards from the board state. These lists will be maintained concurrently for each card characteristic. [List of card characteristic mention above]
2. The legal indices will be compared for each of the card characteristics to find if they form a sequential pattern. This is to identify the prev2, prev and curr relationships between the sequential index values.
  1. For each legal index from the legal index list from the board state.
    1.  Find the characteristic that index i belongs to - say C(j).
    2.  Then, find the characteristic C(j+k) that has the next incremental index - i+1.
    3.  Then, find the characteristic C(j+m) that has the next incremental index - i+2.
    4.  This combination of C(j), C(j+k), C(j+m) forms a legal hypothesis.
  2. This hypothesis evaluation will be formed for sets of 3 consecutive indices, 2 consecutive indices and the single index itself.
3. This strategy described in step 2 will help in identifying the highest ranked individual hypothesis per 3 length, 2 length and single length categories.
4. Each of these individual hypotheses will now be aggregated to form a set of conjunctive hypotheses set which will be used for the master rule formation. Initially, these hypotheses will be treated as a conjunctive AND based rule.
  1. This hypothesis aggregation comparison will be done using a sliding window mechanism.
  2. For each set of triple indices, double indices and single index, compare combinations of hypotheses composed of 3, 2 and 1 vars.
  3. If H(j) is the hypothesis satisfying legal indices i, i+1, i+2 and H(j+k) is the hypothesis satisfying legal indices i+1, i+2, i+3, increment the rank of rule comprised of conjunctive combination of hypotheses - H(j) & H(j+k). The higher the rank of H(j) & H(j+k), the more confident we are towards believing that the master rule is comprised of an AND combination of H(j) & H(j+k).
  4. Run a validation for the set of rules predicted so far, such that the set of illegal cards along with at most 2 previous legal cards are used to check the violation occurrences for the given rules. A recursive call will be made to validate the pattern in the rule violation occurrences which will in turn be used to formulate the EXCEPT/UNLESS clause. Post validation, a confidence rank will be assigned to each rule based on violation occurrences.
  5. If R(m) is the rule which has the highest rank amongst the set of rules, then select the next card to disprove R(m) using the negative characteristic list corresponding to the first characteristic for each of the hypothesis part of the rule R(m). Rules comprising of single length and 2 length hypotheses combinations will also be used to determine the card for disapproval such that we can optimally arrive at the correct rule prediction.
  6. At any point of time, we will maintain the top 10 rules for each set of 3 length, 2 length and single length categories.
5. The next selected card for play should be such that it will try to disprove the highest ranked rule so far.
6. Every time a rule survives a disapproval attempt, increment the confidence rank for this rule.
7. Will return the rule as successful if we reach a threshold for the ranking index.

###Prerequisites:###
* Python 2.7
