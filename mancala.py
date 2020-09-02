from Move import Move
from State import State
import sys
MIN = 1  # denotes human
MAX = 0  # denotes agent


def jump(bound): #jump to next possible bin
    # there are 12 pits/bins in total
    return 12 - bound

def dropStones(state, index, minOrmax):
    mancala_location = state.whoplaying(minOrmax)
    in_hand = state.at(index)  # get stone at index
    following_pit = index + 1  # get following_pit pit
    # ensure u are not in opponent or in ur own store/mancala
    if following_pit == mancala_location:
        if mancala_location == 13:  # skipp agent mancala
            following_pit = 0
        elif mancala_location == 6:  # skip human mancala
            following_pit = 7
    state.set(index, 0)
    changed = False

    while in_hand > 0:  # pick and drop stones
        # ensure player is not in opponent mancala
        if following_pit == mancala_location:
            if mancala_location == 13:
                changed = True
                following_pit = 0
            else:
                changed = True
                following_pit = 7

        in_next_pit_stones = state.at(following_pit) #stones in following_pit pit
        state.set(following_pit, in_next_pit_stones + 1)  # drop stones
        test = in_hand - 1  # decrement stones
        if test >= 0:
            if changed:
                following_pit = following_pit + 1  # go to following_pit pit
                if following_pit == 14: # if at end, reverse
                    following_pit = 0

            elif in_hand == 1 and in_next_pit_stones == 0:
                break  # all dropped, break

            else:
                following_pit = following_pit + 1
                if following_pit == 14:
                    following_pit = 0
        in_hand = in_hand - 1
    bound = following_pit - 1
    if bound == -1:
        bound = 13
    elif bound == 7:
        bound = 6
	
	# if u at opponent store, jump to following_pit bcoz at 6,13 indexes there is mancalas of the players so we to avoid that
    if MAX == minOrmax and bound == 6:
        bound = bound + 1

    if MAX == minOrmax: 
        bound = bound + 1 #agent

    if MIN == minOrmax:
        bound = bound + 1 #human

    if bound != 13 or bound != 6: # skip stores/mancalas
        if bound > -1 and bound < 6:
            if MIN == minOrmax and state.at(bound) == 1: # human
                    jump_index = jump(bound) # jump to pit
                    if state.at(jump_index) > 0:
                        state.set(6, state.at(6)+ 1 + state.at(jump_index)) # pick stone
                        state.set(bound,0) #make pit empty (human)
                        state.set(jump_index,0) #empty bin jump_index
                        return True
                    else:
                        return False

        if bound > 6 and bound < 13:#skip stores/mancalas
            if MAX == minOrmax and state.at(bound) == 1: # agent
                    jump_index = jump(bound); # jump
                    if state.at(jump_index) > 0:
                        state.set(13, state.at(13) + 1 + state.at(jump_index)) # pick stone
                        state.set(bound,0) # make pit empty (agent)
                        state.set(jump_index,0) # make jumped pit empty
                        return True
                    else:
                        return False
    else:
        return False
    return False


def human(state):
    print("Your Mancala at Bottom (Player1)")
    user = int(input("Select from [0,1,2,3,4,5]: "))
    while user > 5 or user < 0 or state.at(user) == 0:
        print("Invalid. Pit empty/out of bound")
        user = int(input("Select from [0,1,2,3,4,5]: "))
    return user


def minmax(state, d, maxD, who_playing, alpha, beta):
    # Max denotes agent, Min denotes human
    temp_state = State([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    if validate_state(state):# if other player empty bins/pits
        if MIN == who_playing:  # agent side
            m = Move(-1, -sys.maxsize)
            return m
        elif MAX == who_playing: # human side
            m = Move(-1, sys.maxsize)
            return m

    elif d == maxD:
        m = Move(-1, heuristic_eval(state, who_playing,who_playing))#evaluate game state
        m.setScore(heuristic_eval(state, who_playing,who_playing))
        return m

    else:
        if who_playing == MIN: # MIN side
            m = Move(-1, sys.maxsize)
            for i in range(0,6):
                if state.at(i) != 0:
                    temp_state.copy(state)
                    dropStones(state, i, who_playing);  #move
                    temp_move = minmax(state, d+1, maxD, MAX, alpha, m.getScore()); #recursion step
                    if m.getScore() <= alpha:  #prunning
                        break; 

                    if temp_move.score < m.score:
                        m.setScore(temp_move.getScore())
                        m.setPit(i)
                    state.copy(temp_state)
            return m

        elif who_playing == MAX:  # Max Side (agent)
            m = Move(-1, -sys.maxsize)
            for i in range(7, 13):
                if state.at(i) != 0:
                    temp_state.copy(state)
                    dropStones(state, i, who_playing)
                    temp_move = minmax(state, d+1, maxD, MIN, m.getScore(), beta)  # recursion
                    if m.getScore() > beta:
                        break

                    if temp_move.getScore() >= m.getScore():
                        m.setScore(temp_move.getScore())
                        m.setPit(i)
                    state.copy(temp_state)
            return m



def heuristic_eval(state, who_playing, heuristic):

    successor = State([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    successor.copy(state)

    if heuristic == 1:
        left = state.eval_left_side()
        right = state.eval_right_side()
        estimation = (right - left) + 100 *(right - left)

        i = 0
        while i <= 5:
            empty = dropStones(successor, i, who_playing)
            if empty:
                estimation = estimation - (successor.at(jump(i)))
            i = i + 1

        i = 7
        while i <= 12:
            empty = dropStones(successor, i, who_playing)
            if empty:
                estimation = estimation + (successor.at(jump(i)))
            i = i + 1

        return estimation

    if heuristic == 0:

        estimation = state.eval_right_side() - state.eval_left_side()  # agent - human
        i = 0
        while i <= 5:
            empty = dropStones(successor, i, who_playing)
            if empty:
                estimation = estimation - (successor.at(jump(i)))
            i = i + 1

        i = 7
        while i <= 12:
            empty = dropStones(successor, i, who_playing)
            if empty:
                estimation = estimation + successor.at(jump(i))
            i = i + 1

        return estimation


def agent_vs_human():
    turn = 0 # 1 for computer, 0 for human
    max_depth = 4
    state = State([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
    game_end = False

    while game_end == False:
        alpha = -sys.maxsize
        beta = sys.maxsize
        if turn == MIN:# computer move
            move = minmax(state, 0, max_depth, MAX, alpha, beta)
            print("Agent played: ",move.getPit(),", State:")
            dropStones(state, move.getPit(), MAX)
            state.show()
            game_end = validate_state(state)
            if game_end:
                break
            else:
                turn = 0   # change player

        else:   # human move.
            print("Human Turn")
            state.show()
            h_move = human(state)
            dropStones(state, h_move, MIN)
            state.show()
            game_end = validate_state(state)
            if game_end:
                break
            else:
                turn = 1
    state.is_humanvsagent()
    state.show()


def agent_vs_agent():
    turn = 0 # 1 for computer, 0 for human
    max_depth = 4
    state = State([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
    game_end = False

    while game_end == False:
        alpha = -sys.maxsize
        beta = sys.maxsize
        if turn == MIN:# agent move
            print("Min Agent")
            move = minmax(state, 0, max_depth, MAX, alpha, beta)
            print("Agent played: ",move.getPit(),", state ")
            dropStones(state, move.getPit(), MAX)
            state.show()
            game_end = validate_state(state)
            if game_end:
                break
            else:
                turn = 0   #change player

        else:   # agent move.
            print("Max Agent")
            move = minmax(state, 0, max_depth, MIN, alpha, beta)
            print("Agent played: ",move.getPit(),", state ")
            dropStones(state, move.getPit(), MIN)
            state.show()
            game_end = validate_state(state)
            if game_end:
                break
            else:
                turn = 1
    state.is_agentvsagent()
    state.show()

# this function validates game state
# when either player has no more stones on his side. The opponent then takes
# all of the stones remaining on his own side and places them in his own Mancala.


def validate_state(state):

    left_side = 0
    for i in range(0, 6):
        if state.at(i) == 0:
            left_side = left_side + 1

    if left_side == 6:
        state.set(13, state.at(13) + state.count_right_side_stones())
        for i in range(7, 13):
            state.set(i, 0)  # make opponent side empty (human side)
        return True

    right_side = 0
    for i in range(7, 13):
        if state.at(i) == 0:
            right_side = right_side + 1

    if right_side == 6:
        state.set(6, state.at(6) + state.count_left_side_stones())
        for i in range(0, 6):
            state.set(i, 0)  # make opponent side empty (computer side)
        return True

    return False


if __name__ == "__main__":
    op = int(input("Enter 1 for Agent vs Human, 2 for Agent vs Agent: "))
    if op == 1:
        agent_vs_human()
    else:
        agent_vs_agent()
