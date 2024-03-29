import copy
import sys


def get_succesor_substate(state: tuple, turn: int) -> list:
    """Getting a state and the player thats turn it is 0 := ai, 1 := enemy and returning a list of substates

    Args:
        state (tuple): ([enemy0, enemy1, ..., enemyi, enemytarget],
                        [player0, player1, ..., playeri, playerTarget])
        my (bool, optional): [description]. Defaults to True.

    Returns:
        list: list of states. if there are multiple turns possible that substate looks like that:
            suc_states = (first_successor_state, [list_of_followup_states])
    """
    suc_substates = []
    # get the turn
    if turn == 0:
        player = 0
        enemy = 1
    elif turn == 1:
        player = 1
        enemy = 0
    else:
        return False

    # iterate the molds of the players whos turn it is
    for k, mold in enumerate(state[player][:-1]):
        # if mold is empty it cant be chosen
        if mold == 0:
            continue

        # else all the stones get distributed in the following molds
        # copy the state and manipulate it
        suc_state = copy.deepcopy(state)
        stones_left = mold
        suc_state[player][k] = 0
        dest = k + 1
        # distribute stones on the rest of the own molds
        a = False
        for i in range(dest, min(dest + stones_left, len(suc_state[player]))):
            suc_state[player][i] += 1
            stones_left -= 1
            # is the last stone put in the goal mold of the own molds
            if stones_left <= 0 and i == len(suc_state[player]) - 1:
                repeat_sucessor_state = get_succesor_substate(suc_state, turn)
                suc_substates += repeat_sucessor_state
                a = True
            # is the own side empty and the oppsit mold not empty we win all the opposit molds
            elif stones_left <= 0 and suc_state[player][i] == 1 and suc_state[enemy][len(suc_state[enemy]) - 2 - i] > 0 and i != len(suc_state[player]) - 1:
                suc_state[player][i] = 0
                opposit = len(suc_state[enemy]) - 2 - i
                won = suc_state[enemy][opposit] + 1
                suc_state[enemy][opposit] = 0
                suc_state[player][-1] += won

        # distribute the rest stones to the ai molds and then
        # again to the own molds until they are all distributed
        while stones_left > 0:
            for i in range(min(stones_left, len(suc_state[enemy]))):
                suc_state[enemy][i] += 1
                stones_left -= 1
            # is the last stone put in the goal mold of the own molds
            if stones_left <= 0:
                break
            for i in range(min(stones_left, len(suc_state[player]))):
                suc_state[player][i] += 1
                stones_left -= 1
                # is the last stone put in the goal mold of the own molds
                if stones_left <= 0 and i == len(suc_state[player]) - 1:
                    repeat_sucessor_state = get_succesor_substate(
                        suc_state, turn)
                    suc_substates += repeat_sucessor_state
                    a = True
                # is the own side empty and the target mold not empty we win all the opposit molds
                elif stones_left <= 0 and suc_state[player][i] == 1 and suc_state[enemy][len(suc_state[enemy]) - 2 - i] > 0 and i != len(suc_state[player]) - 1:
                    suc_state[player][i] = 0
                    opposit = len(suc_state[enemy]) - 2 - i
                    won = suc_state[enemy][opposit] + 1
                    suc_state[enemy][opposit] = 0
                    suc_state[player][-1] += won
        if not a:
            suc_substates.append(suc_state)

    for suc_substate in suc_substates:
        if type(suc_substate[0]) == list:
            # my row is empty and i lose the rest
            if suc_substate[player][:-1] == [player] * (len(suc_substate[player]) - 1):
                rest = sum(suc_substate[enemy][:-1])
                suc_substate[enemy][-1] += rest
                suc_substate[enemy][:-1] = [0] * \
                    ((len(suc_substate[enemy])) - 1)

            # enemy row is empty i get the rest
            elif suc_substate[enemy][:-1] == [0] * (len(suc_substate[enemy]) - 1):
                rest = sum(suc_substate[player][:-1])
                suc_substate[player][-1] += rest
                suc_substate[player][:-1] = [0] * \
                    ((len(suc_substate[player])) - 1)
    return suc_substates


def get_succesor_substate_init(state: tuple, turn: int, move_before: list = []) -> list:
    """Getting a state and the player thats turn it is 0 := ai, 1 := enemy and returning a list of substates

    Args:
        state (tuple): ([enemy0, enemy1, ..., enemyi, enemytarget],
                        [player0, player1, ..., playeri, playerTarget])
        my (bool, optional): [description]. Defaults to True.

    Returns:
        list: list of states. if there are multiple turns possible that substate looks like that:
            suc_states = (first_successor_state, [list_of_followup_states])
    """
    suc_substates = []
    moves = []
    # get the turn
    if turn == 0:
        player = 0
        enemy = 1
    elif turn == 1:
        player = 1
        enemy = 0
    else:
        return False

    # iterate the molds of the players whos turn it is
    for k, mold in enumerate(state[player][:-1]):
        # if mold is empty it cant be chosen
        move = k
        if mold == 0:
            continue

        # else all the stones get distributed in the following molds
        # copy the state and manipulate it
        suc_state = copy.deepcopy(state)
        stones_left = mold
        suc_state[player][k] = 0
        dest = k + 1
        # distribute stones on the rest of the own molds
        a = False
        for i in range(dest, min(dest + stones_left, len(suc_state[player]))):
            suc_state[player][i] += 1
            stones_left -= 1
            # is the last stone put in the goal mold of the own molds
            if stones_left <= 0 and i == len(suc_state[player]) - 1:
                repeat_sucessor_state, repeat_moves = get_succesor_substate_init(
                    suc_state, turn, move_before=move_before+[move])
                suc_substates += repeat_sucessor_state
                moves += repeat_moves
                a = True
            # is the own side empty and the oppsit mold not empty we win all the opposit molds
            elif stones_left <= 0 and suc_state[player][i] == 1 and suc_state[enemy][len(suc_state[enemy]) - 2 - i] > 0 and i != len(suc_state[player]) - 1:
                suc_state[player][i] = 0
                opposit = len(suc_state[enemy]) - 2 - i
                won = suc_state[enemy][opposit] + 1
                suc_state[enemy][opposit] = 0
                suc_state[player][-1] += won

        # distribute the rest stones to the ai molds and then
        # again to the own molds until they are all distributed
        while stones_left > 0:
            for i in range(min(stones_left, len(suc_state[enemy]))):
                suc_state[enemy][i] += 1
                stones_left -= 1
            # is the last stone put in the goal mold of the own molds
            if stones_left <= 0:
                break
            for i in range(min(stones_left, len(suc_state[player]))):
                suc_state[player][i] += 1
                stones_left -= 1
                # is the last stone put in the goal mold of the own molds
                if stones_left <= 0 and i == len(suc_state[player]) - 1:
                    repeat_sucessor_state, repeat_moves = get_succesor_substate_init(
                        suc_state, turn, move_before=move_before+[move])
                    suc_substates += repeat_sucessor_state
                    moves += repeat_moves
                    a = True
                # is the own side empty and the target mold not empty we win all the opposit molds
                elif stones_left <= 0 and suc_state[player][i] == 1 and suc_state[enemy][len(suc_state[enemy]) - 2 - i] > 0 and i != len(suc_state[player]) - 1:
                    suc_state[player][i] = 0
                    opposit = len(suc_state[enemy]) - 2 - i
                    won = suc_state[enemy][opposit] + 1
                    suc_state[enemy][opposit] = 0
                    suc_state[player][-1] += won
        if not a:
            suc_substates.append(suc_state)
            moves.append(move_before + [k])

    for suc_substate in suc_substates:
        if type(suc_substate[0]) == list:
            # my row is empty and i lose the rest
            if suc_substate[player][:-1] == [player] * (len(suc_substate[player]) - 1):
                rest = sum(suc_substate[enemy][:-1])
                suc_substate[enemy][-1] += rest
                suc_substate[enemy][:-1] = [0] * \
                    ((len(suc_substate[enemy])) - 1)

            # enemy row is empty i get the rest
            elif suc_substate[enemy][:-1] == [0] * (len(suc_substate[enemy]) - 1):
                rest = sum(suc_substate[player][:-1])
                suc_substate[player][-1] += rest
                suc_substate[player][:-1] = [0] * \
                    ((len(suc_substate[player])) - 1)
    return suc_substates, moves


def value_of_state(state: tuple) -> int:
    """getting the value by taking the value in target mold from own player and enemy

    Args:
        state (tuple): state to avalueate

    Returns:
        int: value
    """
    my_molds, enemy_molds = state
    my_target = my_molds[-1]
    enemy_target = enemy_molds[-1]
    value = my_target - enemy_target
    if state[0][:-1] == [0] * (len(state[0]) - 1) or state[1][:-1] == [1] * (len(state[1]) - 1):
        if value > 0:
            value = sys.maxsize
        elif value < 0:
            value = -sys.maxsize
    return value


def is_terminate_state(state: tuple) -> bool:
    """is the state an end state

    Args:
        state (tuple): current state

    Returns:
        bool: is the state terminate state
    """
    if state[0][:-1] == [0] * (len(state[0]) - 1) or state[1][:-1] == [0] * (len(state[1]) - 1):
        return True
    else:
        return False


def max_state(state: tuple, depth: int, min_yet) -> int:
    """max part of alpha beta search

    Args:
        state (tuple): state to expand from
        depth (int): depth yet to go if zero calculate value
        min_yet ([type]): min from layer above to terminate when needed

    Returns:
        int: return the value of the branch (max)
    """
    suc_states = get_succesor_substate(state, 0)

    max_yet = -sys.maxsize
    for suc_state in suc_states:
        if depth <= 0 or is_terminate_state(suc_state):
            value = value_of_state(suc_state)
        else:
            value = min_state(suc_state, depth - 1, max_yet)
        max_yet = max(value, max_yet)
        if value >= min_yet:
            break

    return max_yet


def min_state(state: tuple, depth: int, max_yet: int) -> int:
    """min part of alpha beta search

    Args:
        state (tuple): state to expand from
        depth (int): depth yet to go if zero calculate value
        max_yet ([type]): max from layer above to terminate when needed

    Returns:
        int: return the value of the branch (min)
    """
    suc_states = get_succesor_substate(state, 1)
    min_yet = sys.maxsize
    for suc_state in suc_states:
        if depth <= 0 or is_terminate_state(suc_state):
            value = value_of_state(suc_state)
        else:
            value = max_state(suc_state, depth - 1, min_yet)
        min_yet = min(value, min_yet)
        if value <= max_yet:
            break

    return min_yet


BEST_MOVE = None


def best_move(state: tuple, depth: int = 0) -> tuple:
    """init of alpha beta

    Args:
        state (tuple): get the starting state
        depth (int, optional): depth to expand to. Defaults to 0.

    Returns:
        tuple: returns the best state
    """
    global BEST_MOVE
    suc_states, moves = get_succesor_substate_init(state, 0)
    BEST_MOVE = moves[0]
    
    best_move = None
    max_yet = -sys.maxsize
    for suc_state, move in zip(suc_states, moves):
        if depth <= 0 or is_terminate_state(suc_state):
            value = value_of_state(suc_state)
        else:
            value = min_state(suc_state, depth - 1, max_yet)
        if value > max_yet:
            best_move = move
            BEST_MOVE = move
            max_yet = value
    return best_move
