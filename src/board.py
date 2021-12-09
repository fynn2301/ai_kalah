import pygame as pg


class Board():
    # board setiings
    FACTOR = 0.7
    POINT_DIST_FACT = int(70 * FACTOR)
    SCREENSIZE_WIDTH = int(1000 * FACTOR)
    SCREENSIZE_HIGHT = int(400 * FACTOR)
    EMPTY_RADIUS = int(16 * FACTOR)
    POINT_RADIUS = int(16 * FACTOR)
    BORDER_WIDTH = int(3 * FACTOR)
    LINE_WIDTH = int(2 * FACTOR)
    FONT = 'chalkduster.ttf'
    FONT_SIZE = int(80 * FACTOR)

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

    ENEMY_KOOR = [(SCREENSIZE_WIDTH * 13 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 11 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 9 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 7 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 5 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 3 / 16, SCREENSIZE_WIDTH / 16),
                  (SCREENSIZE_WIDTH * 1 / 16, SCREENSIZE_HIGHT / 2)]

    MY_KOOR = [(SCREENSIZE_WIDTH * 3 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 5 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 7 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 9 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 11 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 13 / 16, SCREENSIZE_HIGHT * 14 / 16),
               (SCREENSIZE_WIDTH * 15 / 16, SCREENSIZE_HIGHT / 2)]

    def __init__(self, mold_per_player: int = 6, stone_per_mold: int = 3) -> None:
        """init the board

        Args:
            mold_per_player (int, optional): number molds on each side. Defaults to 6.
            stone_per_mold (int, optional): number of stones in each mold at start. Defaults to 3.
        """
        my_molds = [stone_per_mold] * mold_per_player
        my_molds.append(0)
        enemy_molds = [stone_per_mold] * mold_per_player
        enemy_molds.append(0)
        self.state = (my_molds, enemy_molds)
        pg.init()
        self._screen = pg.display.set_mode(
            [self.SCREENSIZE_WIDTH, self.SCREENSIZE_HIGHT])
        self._update()

    def _draw_board(self):
        """draw board
        """
        pg.draw.ellipse(self._screen, self.WHITE,
                        (0, 0, self.SCREENSIZE_WIDTH / 8, self.SCREENSIZE_HIGHT))
        pg.draw.ellipse(self._screen, self.BLACK,
                        (0, 0, self.SCREENSIZE_WIDTH / 8, self.SCREENSIZE_HIGHT), self.BORDER_WIDTH)

        pg.draw.ellipse(self._screen, self.WHITE,
                        (self.SCREENSIZE_WIDTH - self.SCREENSIZE_WIDTH/8, 0, self.SCREENSIZE_WIDTH / 8, self.SCREENSIZE_HIGHT))
        pg.draw.ellipse(self._screen, self.BLACK,
                        (self.SCREENSIZE_WIDTH - self.SCREENSIZE_WIDTH/8, 0, self.SCREENSIZE_WIDTH / 8, self.SCREENSIZE_HIGHT), self.BORDER_WIDTH)
        for koor in self.MY_KOOR[:-1]:
            pg.draw.circle(self._screen, self.WHITE, koor,
                           self.SCREENSIZE_WIDTH / 16)
            pg.draw.circle(self._screen, self.BLACK, koor,
                           self.SCREENSIZE_WIDTH / 16, self.BORDER_WIDTH)
        for koor in self.ENEMY_KOOR[:-1]:
            pg.draw.circle(self._screen, self.WHITE, koor,
                           self.SCREENSIZE_WIDTH / 16)
            pg.draw.circle(self._screen, self.BLACK, koor,
                           self.SCREENSIZE_WIDTH / 16, self.BORDER_WIDTH)

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

    def _update(self) -> None:
        """update the field by drawing the field and positions
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        self._screen.fill(self.GRAY)
        self._draw_board()
        self._draw_fields()
        pg.display.flip()
