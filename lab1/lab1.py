# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain, pretty_goal_tree
from data import *
import pprint

pp = pprint.PrettyPrinter(indent=1)
pprint = pp.pprint

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

# Fill this in with your rule 
transitive_rule = IF(AND(
    "(?y) beats (?z)",
    "(?x) beats (?y)"
), THEN("(?x) beats (?z)") )

# You can test your rule by uncommenting these pretty print statements
#  and observing the results printed to your screen after executing lab1.py
# pprint(forward_chain([transitive_rule], abc_data))
# pprint(forward_chain([transitive_rule], poker_data))
# pprint(forward_chain([transitive_rule], minecraft_data))


#### Part 3: Family Relations #########################################

# Define your rules here. We've given you an example rule whose lead you can follow:
friend_rule = IF( AND("person (?x)", "person (?y)"), THEN ("friend (?x) (?y)", "friend (?y) (?x)") )

same_rule = IF("person (?x)", THEN("same (?x) (?x)"))

child_rule = IF(AND("parent (?y) (?x)"), THEN("child (?x) (?y)"))

sibling_rule = IF(
    AND(
        "parent (?z) (?x)",
        "parent (?z) (?y)",
        NOT(
            "same (?x) (?y)"
        )
    ),
    THEN(
        "sibling (?x) (?y)"
    )
)

grandparent_rule = IF(
    AND(
        "parent (?z) (?x)",
        "parent (?y) (?z)"
        ),
    THEN(
        "grandparent (?y) (?x)"
    )
)

grandchild_rule = IF(
    AND(
        "grandparent (?y) (?x)"
    ),
    THEN(
        "grandchild (?x) (?y)"
    )
)

cousin_rule = IF(
    AND(
        "grandchild (?x) (?z)",
        "grandchild (?y) (?z)",
        NOT(
            OR(
                "sibling (?x) (?y)",
                "same (?x) (?y)"
            )
        )
    ),
    THEN(
        "cousin (?x) (?y)",
        "cousin (?y) (?x)"
    )
)


# Add your rules to this list:
family_rules = [same_rule, sibling_rule, child_rule, grandparent_rule, grandchild_rule, cousin_rule ]

# Uncomment this to test your data on the Simpsons family:
# pprint(forward_chain(family_rules, simpsons_data, verbose=False))

# These smaller datasets might be helpful for debugging:
# pprint(forward_chain(family_rules, sibling_test_data, verbose=True))
# pprint(forward_chain(family_rules, grandparent_test_data, verbose=True))

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
# pprint(black_family_cousins)


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables


def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """
    consequence = [hypothesis]
    for rule in rules:
        temp = match(rule.consequent(), hypothesis)

        if temp != None:
            antecedent = rule.antecedent()

            antecedent_matches = []
            
            next_hypothesis = populate(antecedent, temp)

            if type(antecedent) == str:
                antecedent_matches.append(simplify(backchain_to_goal_tree(rules, next_hypothesis)))
            
            else:
                for antecedent in next_hypothesis:
                    antecedent_matches.append(simplify(backchain_to_goal_tree(rules, antecedent)))
            
            if type(antecedent) == OR:
                consequence.append(simplify(OR(antecedent_matches)))
            else:
                consequence.append(simplify(AND(antecedent_matches)))
    return simplify(OR(consequence))

# Uncomment this to test out your backward chainer:
# pretty_goal_tree(backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin'))


#### Survey #########################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
print("(Doing forward chaining. This may take a minute.)")
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
