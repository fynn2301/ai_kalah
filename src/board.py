from time import sleep
from typing import NoReturn
import pygame as pg


class Board():
    # board setiings
    FACTOR = 0.7
    POINT_DIST_FACT = int(70 * FACTOR)
    BORDER_WIDTH = int(3 * FACTOR)
    LINE_WIDTH = int(2 * FACTOR)
    FONT = 'chalkduster.ttf'

    # used color coding
    LIGHT_ORANGE = (255, 230, 205)
    ORANGE = (255, 223, 83)
    LIGHT_BLUE = (222, 222, 255)
    BLUE = (153, 153, 255)
    LIGHT_RED = (255, 222, 222)
    RED = (255, 153, 152)
    BLACK = (10, 10, 10)
    WHITE = (255, 255, 255)
    GRAY = (170, 170, 170)
    LIGHT_GREEN = (139, 230, 135)

    ENEMY_KOOR = []

    MY_KOOR = []

    def __init__(self, mold_per_player: int = 6, stone_per_mold: int = 4) -> NoReturn:
        self.SCREENSIZE_HIGHT = int(400 * self.FACTOR)
        self.SCREENSIZE_WIDTH = int(
            self.SCREENSIZE_HIGHT / 2 + mold_per_player * 150)
        self.FONT_SIZE = int(80 * self.FACTOR)
        self.RADIUS = int(50)
        for i in range(0, mold_per_player):
            self.MY_KOOR.append(
                (self.SCREENSIZE_HIGHT / 4 + self.SCREENSIZE_WIDTH * (i + 1) / 8, self.SCREENSIZE_HIGHT * 12 / 16))
            self.ENEMY_KOOR.append(
                (self.SCREENSIZE_HIGHT / 4 + self.SCREENSIZE_WIDTH * (i + 1) / 8, self.SCREENSIZE_HIGHT * 4 / 16))
        print(self.MY_KOOR)
        my_molds = [stone_per_mold] * mold_per_player
        my_molds.append(0)
        enemy_molds = [stone_per_mold] * mold_per_player
        enemy_molds.append(0)
        self.state = (my_molds, enemy_molds)
        pg.init()
        self._screen = pg.display.set_mode(
            [self.SCREENSIZE_WIDTH, self.SCREENSIZE_HIGHT])
        self._update()

    def _draw_board(self, color_ai: list = [], color_player: list = [], color_from_player: int = -1, color_from_ai: int = -1, possible_player: list = []):
        """draw board
        """
        if len(self.state[0]) - 1 in color_ai:
            ai_color = self.LIGHT_BLUE
        else:
            ai_color = self.WHITE

        if len(self.state[0]) - 1 in color_player:
            player_color = self.LIGHT_BLUE
        else:
            player_color = self.WHITE
        pg.draw.ellipse(self._screen, player_color,
                        (0, 0, self.SCREENSIZE_WIDTH / 16, self.SCREENSIZE_HIGHT))
        pg.draw.ellipse(self._screen, self.BLACK,
                        (0, 0, self.SCREENSIZE_WIDTH / 16, self.SCREENSIZE_HIGHT), self.BORDER_WIDTH)

        pg.draw.ellipse(self._screen, ai_color,
                        (self.SCREENSIZE_WIDTH - self.SCREENSIZE_HIGHT / 4, 0, self.SCREENSIZE_WIDTH / 16, self.SCREENSIZE_HIGHT))
        pg.draw.ellipse(self._screen, self.BLACK,
                        (self.SCREENSIZE_WIDTH - self.SCREENSIZE_HIGHT / 4, 0, self.SCREENSIZE_WIDTH / 16, self.SCREENSIZE_HIGHT), self.BORDER_WIDTH)
        for i, koor in enumerate(self.MY_KOOR):

            if color_from_ai == i:
                color = self.LIGHT_RED
            elif i in color_ai:
                color = self.LIGHT_BLUE
            else:
                color = self.WHITE
            pg.draw.circle(self._screen, color, koor,
                           self.RADIUS)
            pg.draw.circle(self._screen, self.BLACK, koor,
                           self.RADIUS, self.BORDER_WIDTH)
        for i, koor in enumerate(self.ENEMY_KOOR):
            if color_from_player == i:
                color = self.LIGHT_RED
            elif i in color_player:
                color = self.LIGHT_BLUE
            elif i in possible_player:
                color = self.LIGHT_GREEN
            else:
                color = self.WHITE
            pg.draw.circle(self._screen, color, koor,
                           self.RADIUS)
            pg.draw.circle(self._screen, self.BLACK, koor,
                           self.RADIUS, self.BORDER_WIDTH)

    def _draw_fields(self):
        for mold, (x, y) in zip(self.state[0], self.MY_KOOR):
            font = pg.font.SysFont(self.FONT, self.FONT_SIZE)
            text = str(mold)
            img = font.render(text, True, self.BLACK)
            self._screen.blit(
                img, (x - ((len(text)+0.5) * self.FONT_SIZE/8), y - self.FONT_SIZE/4))

        for mold, (x, y) in zip(self.state[1], self.ENEMY_KOOR):
            font = pg.font.SysFont(self.FONT, self.FONT_SIZE)
            text = str(mold)
            img = font.render(text, True, self.BLACK)
            self._screen.blit(
                img, (x - ((len(text)+0.5) * self.FONT_SIZE/8), y - self.FONT_SIZE/4))

    def _update(self, color_ai: list = [], color_player: list = [], color_from_player: int = -1, color_from_ai: int = -1, possible_player: list = []) -> None:
        """update the field by drawing the field and positions
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        self._screen.fill(self.GRAY)
        self._draw_board(color_ai, color_player,
                         color_from_player, color_from_ai)
        self._draw_fields()
        pg.display.flip()

    def turn_signal(self, possible_player: list = []) -> NoReturn:
        """update the field by drawing the field and positions
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        self._screen.fill(self.GRAY)
        self._draw_board(possible_player=possible_player)
        self._draw_fields()
        font = pg.font.Font(None, 25)
        text = font.render("Your turn", True, self.BLACK)
        text_rect = text.get_rect(
            center=(self.SCREENSIZE_WIDTH/2, self.SCREENSIZE_HIGHT/2))
        self._screen.blit(text, text_rect)
        pg.display.flip()
