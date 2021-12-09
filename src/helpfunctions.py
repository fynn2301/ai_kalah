import copy


def get_succesor_state(state: list) -> list:
    suc_states = []  # is a list of tuples with the list of my and enemy molds
    # iterate the 6 fields that can be selected

    for i, mold in enumerate(state[0][:-1]):
        # if mold is empty it cant be chosen
        if mold == 0:
            continue

        # else all the stones get distributed in the following molds
        # copy the state and manipulate it
        suc_state = copy.deepcopy(state)
        stones_left = mold
        suc_state[0][i] = 0
        dest = i + 1
        for i in range(dest, min(dest + stones_left, len(suc_state[0]))):
            suc_state[0][i] += 1
            stones_left -= 1

        while stones_left > 0:
            for i in range(min(stones_left, len(suc_state[1]))):
                suc_state[1][i] += 1
                stones_left -= 1
            if stones_left <= 0:
                break
            for i in range(min(stones_left, len(suc_state[0]))):
                suc_state[0][i] += 1
                stones_left -= 1
        suc_states.append(suc_state)
    return suc_states
