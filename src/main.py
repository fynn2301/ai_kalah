from typing import NamedTuple
import helpfunctions as helper
from board import Board
from time import sleep
import random


class Algorithm():

    def __init__(self) -> None:
        self.board = Board()
        self.main()

    def main(self):
        while(True):
            suc_states = helper.get_succesor_state(self.board.state)
            next = random.choice(suc_states)
            self.board.state = next
            self.board._update()
            sleep(3)


if __name__ == "__main__":
    Algorithm()
