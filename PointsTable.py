from GUISettings import TABLE_WIDTH, TABLE_HEIGHT, WIDTH, HEIGHT, FONT_BIDDING, FONT_BIDDING_PLAYERS, \
    POINTS_TABLE_COLOR, POINT_OFFSET_HEIGHT
import pygame


class PointsTable(pygame.sprite.Sprite):
    __card_back_image: pygame.image
    __card_image: pygame.image
    __is_shown: bool
    __left: int
    __top: int

    def __init__(self, game, display, control_panel):
        super().__init__()
        self.surf = pygame.Surface((TABLE_WIDTH, TABLE_HEIGHT))
        self.__left = WIDTH/2 - TABLE_WIDTH/2
        self.__top = HEIGHT/2 - TABLE_HEIGHT/2
        self.__is_clicked = False
        self.__is_shown = False
        self.hit_box = pygame.Rect(WIDTH / 2 - TABLE_WIDTH / 2, HEIGHT / 2 - TABLE_HEIGHT / 2,
                                   TABLE_WIDTH, TABLE_HEIGHT)
        self.title = FONT_BIDDING.render("BIDDING", True, (255, 255, 255))
        self.game = game
        self.control_panel = control_panel
        self.display = display

    @property
    def is_clicked(self):
        return self.__is_clicked

    @is_clicked.setter
    def is_clicked(self, is_clicked: bool):
        self.__is_clicked = is_clicked

    def render(self):
        pygame.draw.rect(self.display, POINTS_TABLE_COLOR, self.hit_box)
        self.display_headers()
        self.display_points()

    def display_headers(self):
        players = []
        for i in range(0, 3):
            if i == self.game.id_player:
                text = "Me"
            else:
                text = "Player %i" % i
            players.append(FONT_BIDDING_PLAYERS.render(text, True, (255, 255, 255)))
        self.display.blit(self.title, (WIDTH / 2 - 70, 40))
        self.display.blit(players[0], (WIDTH / 2 - 240, 100))
        self.display.blit(players[1], (WIDTH / 2 - 50, 100))
        self.display.blit(players[2], (WIDTH / 2 - 140, 100))

    def display_points(self):
        players_points = self.game.points_table
        left = WIDTH / 2 - 240
        for player in players_points:
            top = 130
            for points in player:
                self.display.blit(points, (WIDTH / 2 - 70, 40))
                top += POINT_OFFSET_HEIGHT
            left += 190

    def click_table(self):
        if self.__is_shown:
            self.__is_shown = False

    def update(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            ...
            # tabela znika