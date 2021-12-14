from typing import NamedTuple, NoReturn
import helpfunctions as helper
from board import Board
import pygame as pg
from time import sleep


class Algorithm():

    def __init__(self) -> NoReturn:
        """Init

        Returns:
            NoReturn: NoReturn
        """
        self.board = Board()
        self.main()

    def main(self) -> NoReturn:
        """Run main

        Returns:
            NoReturn: NoReturn
        """

        while(True):
            # ais turn

            if helper.is_terminate_state(self.board.state):
                break
            best_suc = helper.best_state(self.board.state, 5)
            self.animate_move(self.board.state, best_suc)
            self.board.state = best_suc
            self.board._update()

            # your turn
            if helper.is_terminate_state(self.board.state):
                break
            self.get_player_input()

    def get_player_input(self) -> NoReturn:
        """The player has to select a mold to distribute
        and then this is updated to the board

        Returns:
            NoReturn: NoReturn
        """
        player_possible = [i for i, mold in enumerate(
            self.board.state[1]) if mold != 0]
        self.board.turn_signal(possible_player=player_possible)

        while True:  # your main loop
            # get all events
            ev = pg.event.get()
            # proceed events
            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pg.MOUSEBUTTONUP:
                    # get mouseclick position
                    pos = pg.mouse.get_pos()
                    i = 0
                    # iterate the different molds to see which was clicked
                    for x, y in self.board.ENEMY_KOOR[:-1]:
                        # find out if x and y position if the click was in the koordinate of the mold
                        if pos[0] > (x - (self.board.SCREENSIZE_WIDTH / 16)) and pos[0] < (x + (self.board.SCREENSIZE_WIDTH / 16)):
                            if pos[1] > (y - (self.board.SCREENSIZE_WIDTH / 16)) and pos[1] < (y + (self.board.SCREENSIZE_WIDTH / 16)):
                                turn_again = False
                                # find out if state is empty
                                if self.board.state[1][i] == 0:
                                    break
                                else:
                                    # else all the stones get distributed in the following molds
                                    suc_state = self.board.state
                                    mold = suc_state[1][i]
                                    stones_left = mold
                                    suc_state[1][i] = 0
                                    dest = i + 1

                                    # distribute stones on the rest of the own molds
                                    for i in range(dest, min(dest + stones_left, len(suc_state[1]))):
                                        suc_state[1][i] += 1
                                        stones_left -= 1
                                        # is the last stone put in the goal mold of the own molds
                                        if stones_left <= 0 and i == len(suc_state[1]) - 1:
                                            turn_again = True
                                        # is the opposit side empty and the target mold empty we win all the opposit molds
                                        elif stones_left <= 0 and suc_state[1][i] == 1 and suc_state[0][len(suc_state[0]) - 2 - i] > 0 and i != len(suc_state[1]) - 1:
                                            suc_state[1][i] = 0
                                            opposit = len(
                                                suc_state[0]) - 2 - i
                                            won = suc_state[0][opposit] + 1
                                            suc_state[0][opposit] = 0
                                            suc_state[1][-1] += won
                                    # distribute the rest stones to the ai molds and then
                                    # again to the own molds until they are all distributed
                                    while stones_left > 0:
                                        for i in range(min(stones_left, len(suc_state[0]))):
                                            suc_state[0][i] += 1
                                            stones_left -= 1
                                        if stones_left <= 0:
                                            break
                                        for i in range(min(stones_left, len(suc_state[1]))):
                                            suc_state[1][i] += 1
                                            stones_left -= 1
                                            # is the last stone put in the goal mold of the own molds
                                            if stones_left <= 0 and i == len(suc_state[1]) - 1:
                                                turn_again = True
                                            # is the opposit side empty and the target mold empty we win all the opposit molds
                                            elif stones_left <= 0 and suc_state[1][i] == 1 and suc_state[0][len(suc_state[0]) - 2 - i] > 0 and i != len(suc_state[1]) - 1:
                                                suc_state[1][i] = 0
                                                opposit = len(
                                                    suc_state[0]) - 2 - i
                                                won = suc_state[0][opposit] + 1
                                                suc_state[0][opposit] = 0
                                                suc_state[1][-1] += won
                                    # set the successor state to board
                                    self.board.state = suc_state
                                    self.board._update()
                                    # play again
                                    if turn_again:

                                        if helper.is_terminate_state(self.board.state):
                                            return
                                        self.get_player_input()
                                        return
                                    else:
                                        return
                        # count up the seleceted board
                        i += 1

    def animate_move(self, state: tuple, suc_state: tuple):
        suc_substates, suc_submoves = helper.get_succesor_substate_init(
            state)

        suc_state_move = helper.substates_to_states_init(
            suc_substates, suc_submoves)
        for substates, moves in suc_state_move:
            if substates[-1] == suc_state:
                break
        current = self.board.state
        for substate, move in zip(substates, moves):
            ai_changed_index = [i for i in range(
                len(substate[0])) if substate[0][i] != current[0][i]]
            player_changed_index = [i for i in range(
                len(substate[1])) if substate[1][i] != current[1][i]]
            from_mold = move
            current = substate
            self.board._update(
                ai_changed_index, player_changed_index, -1, from_mold)
            sleep(3)
            self.board.state = substate
            self.board._update(
                ai_changed_index, player_changed_index, -1, from_mold)
            sleep(3)


if __name__ == "__main__":
    Algorithm()
