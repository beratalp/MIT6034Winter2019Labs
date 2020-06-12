# MIT 6.034 Lab 3: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1

INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    try:
        chains = board.get_all_chains()
        lengths = [len(chain) for chain in chains]
        if max(lengths) > 3:
            return True
        columns = list(range(0, 7))
        column_status = [board.is_column_full(column) for column in columns]
        if sum(column_status) == 7:
            return True
        return False
    except:
        return False

def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    boards = []
    if is_game_over_connectfour(board):
        return boards
    columns = list(range(0, 7))
    for col in columns:
        if not board.is_column_full(col):
            boards.append(board.add_piece(col))
    return boards

def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    chains = board.get_all_chains()
    lengths = [len(chain) for chain in chains]
    if max(lengths) < 4:
        return 0
    if is_current_player_maximizer:
        return -1000
    else:
        return 1000

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    score = endgame_score_connectfour(board, is_current_player_maximizer)
    moves = board.count_pieces()
    if score == 0:
        return score
    elif score > 0:
        return score*score/moves
    else:
        return -score*score/moves

def return_point(point, is_current_player_maximizer):
    if is_current_player_maximizer:
        return -point
    else:
        return point

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    chain1 = board.get_all_chains(current_player=True)
    chain2 = board.get_all_chains(current_player=False)
    num1 = len(chain1)
    num2 = len(chain2)
    len1 = sum([len(c) for c in chain1])
    len2 = sum([len(c) for c in chain2])
    if num1 + len1 == num2 + len2:
        return 0
    if num1 == num2:
        return return_point(-10, is_current_player_maximizer)
    else:
        return return_point(500, is_current_player_maximizer)


# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    evals = 0
    stack = [[state]]
    best_path = None, None
    while len(stack) != 0:
        top = stack.pop()
        s = top[-1]
        ext = s.generate_next_states()
        
        if len(ext) != 0:
            for e in ext:
                if e not in top:
                    stack.append(top + [e])
        else:
            value = s.get_endgame_score(is_current_player_maximizer=True)
            evals += 1

            if best_path == (None, None) or value > best_path[1]:
                best_path = top, value
    
    return best_path[0], best_path[1], evals


# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

# pretty_print_dfs_type(dfs_maximizing(GAME1))


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    evals = 0
    next_states = state.generate_next_states()
    best_path = None, None
    if len(next_states) == 0:
        return [state], state.get_endgame_score(maximize), 1
    if maximize:
        for _state in next_states:
            result = minimax_endgame_search(_state, False)
            evals += result[2]

            if best_path[1] == None or result[1] > best_path[1]:
                best_path = [state] + result[0], result[1]
    else:
        for _state in next_states:
            result = minimax_endgame_search(_state, True)
            evals += result[2]

            if best_path[1] == None or result[1] < best_path[1]:
                best_path = [state] + result[0], result[1]
    return best_path[0], best_path[1], evals


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

# pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    raise NotImplementedError


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

# pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type 
    as dfs_maximizing."""
    raise NotImplementedError


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    raise NotImplementedError


# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented


#### Part 3: Multiple Choice ###################################################

ANSWER_1 = ''

ANSWER_2 = ''

ANSWER_3 = ''

ANSWER_4 = ''


#### SURVEY ###################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
