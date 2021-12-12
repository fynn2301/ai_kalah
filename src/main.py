from typing import NamedTuple, NoReturn
import helpfunctions as helper
from board import Board
import pygame as pg


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

            next = helper.best_state(self.board.state, 5)
            self.board.state = next
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
        self.board.turn_signal()
        while True:  # your main loop
            # get all events
            ev = pg.event.get()
            # proceed events
            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pg.MOUSEBUTTONUP:
                    # get mouseclick position
                    pos = pg.mouse.get_pos()
                    print("clicked at: ", pos)
                    i = 0
                    # iterate the different molds to see which was clicked
                    for x, y in self.board.ENEMY_KOOR[:-1]:
                        # find out if x and y position if the click was in the koordinate of the mold
                        if pos[0] > (x - (self.board.SCREENSIZE_WIDTH / 16)) and pos[0] < (x + (self.board.SCREENSIZE_WIDTH / 16)):
                            if pos[1] > (y - (self.board.SCREENSIZE_WIDTH / 16)) and pos[1] < (y + (self.board.SCREENSIZE_WIDTH / 16)):
                                turn_again = False
                                print("clicked at ", i)
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
                                        elif stones_left <= 0 and suc_state[1][i] == 1 and i != len(suc_state[1]) - 1:
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
                                            elif stones_left <= 0 and suc_state[1][i] == 1 and i != len(suc_state[1]) - 1:
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


if __name__ == "__main__":
    Algorithm()
