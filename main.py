#!/usr/bin/env python3
import os
from random import choice
import multiprocessing as mp
from threading import Thread
import client.pykgp.algorithm as algo
from client.pykgp.kgp import Board
import client.pykgp.kgp as kgp


def print_state(state: Board):
    print("---------------------------------------------------")
    print(" ", state.north_pits[::-1])
    print(state.north, " " * (len(str(state.north_pits))), state.south)
    print(" ", state.south_pits)
    print("---------------------------------------------------")


def agent(state: Board):
    print_state(state)

    # create state
    my_pits = state.south_pits + [state.south]
    enemy_pits = state.north_pits + [state.north]
    new_state = (my_pits, enemy_pits)

    # get best move
    t = Thread(target=algo.best_move, args=(new_state, 3,))
    t.start()
    t.join(timeout=4.9)
    try:
        yield algo.BEST_MOVE[0]
    except IndexError:
        pass


if __name__ == "__main__":
    mp.set_start_method('fork')
    kgp.connect(agent, token="Agent007")
