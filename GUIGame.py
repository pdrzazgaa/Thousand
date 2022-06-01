import sys
import ControlPanel
import GUISettings
from Player import Player
from Database import Database
from PlayerRound import PlayerRound
from pygame.locals import *
from GUISettings import *
from Round import RoundGUI, Round
from ControlPanel import ControlPanel
from Timer import RepeatedTimer


class Desk:
    display_surface: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    frame_per_sec: pygame.time.Clock()

    def __init__(self, game):
        pygame.init()
        self.prepare_game()
        self.waiting_screen = WaitingForPlayersScreen(game, self.display_surface)
        self.panel_control = ControlPanel()

        # Timery sprawdzające bazę - Czy są jacyś gracze
        timer_check_players = RepeatedTimer(2.0, self.panel_control.check_players, game.id_game)
        timer_check_players.start()

        # TESTOWANIE
        for i in range(len(game.players), 3):
            game.add_player_to_game(Player(i))

        cards_gui = self.create_cards(game, 0)

        while True:
            self.event_list = pygame.event.get()
            for event in self.event_list:
                if event.type == QUIT:
                    Desk.quit(game)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.card_clicked()
            while self.panel_control.waiting_for_players_phase:
                self.waiting_screen.main()
            while self.panel_control.bidding_phase:
                ...
            while self.panel_control.game_phase:
                while self.panel_control.player0_phase:
                    ...
                while self.panel_control.player1_phase:
                    ...
                while self.panel_control.player2_phase:
                    ...
            self.display_cards(game, self.panel_control.end_bidding_phase, cards_gui)

    def prepare_game(self):
        vec = pygame.math.Vector2  # 2 for two dimensional
        self.frame_per_sec = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("1000")
        self.all_sprites = pygame.sprite.Group()

    def create_cards(self, game, dealing_player):
        # Tworzymy rundy graczy
        player0_round = PlayerRound(game.players[game.id_player])
        player1_round = PlayerRound(game.players[(game.id_player + 1) % 3])
        player2_round = PlayerRound(game.players[(game.id_player + 2) % 3])
        # Zaczynamy rundę z 3 graczami, ze wskazanym graczem rozdającym
        game_round = Round([player0_round, player1_round, player2_round], dealing_player)
        player0_round.sort_card()
        # tworzymy karty
        player_cards_gui = RoundGUI.create_cards_gui(player0_round.cards, self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(player1_round.cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(player2_round.cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(game_round.bidding.prikup, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui

    def display_cards(self, game, hidden_bidding, cards):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui = cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)
        RoundGUI.display_oponent_cards(oponent1_cards_gui, (game.id_player + 1) % 3)
        RoundGUI.display_oponent_cards(oponent2_cards_gui, (game.id_player + 2) % 3)

        self.display_surface.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.display_surface)
        pygame.display.update()
        self.frame_per_sec.tick(FPS)

    def card_clicked(self):
        pos = pygame.mouse.get_pos()

        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(self.event_list)
            pygame.display.update()

    @staticmethod
    def quit(game):
        Database.leave_game(game.id_game)
        pygame.quit()
        sys.exit()


class WaitingForPlayersScreen:

    display: pygame.display

    def __init__(self, game, display):
        self.game = game
        self.display = display
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        ...
    #     self.buttons.append(Button(self, 600, 700, 400, 80, "Quit", Desk.quit, self.display))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        message = GUISettings.FONT_WAITING.render("WAITING FOR OTHER PLAYERS", True, (255, 255, 255), BACKGROUND_COLOR)
        self.display.blit(message, (100, 150))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    @staticmethod
    def go_back():
        ControlPanel.waiting_for_players_phase = False


class Button:
    # base = pygame.image.load("textures\\Button_base.xcf")
    # click = pygame.image.load("textures\\Button_click.xcf")

    def __init__(self, menu, x, y, width, height, name, function, display):
        self.menu = menu
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = name
        self.name = GUISettings.FONT_BUTTON.render(name, True, (0, 0, 0))
        self.function = function
        self.hit_box = pygame.Rect(x - width / 2, y - width / 2, width, height)
        self.clicked = False
        # self.texture = Button.base
        self.display = display

    def render(self):
        # self.choose_texture()
        pygame.draw.rect(self.display, (255, 0, 0), self.hit_box)
        # texture_copy = pygame.transform.scale(self.texture, (self.width, self.height))
        # self.display.blit(texture_copy, (self.x - self.width/2, self.y - self.height * 2.5))
        self.display.blit(self.name,
                          (self.x - self.name.get_width() / 2, self.y - self.height * 2.25))

    # def choose_texture(self):
    #     if self.hit_box.x < self.menu.mouse_x < self.hit_box.x + self.hit_box.width and\
    #        self.hit_box.y < self.menu.mouse_y < self.hit_box.y + self.hit_box.height:
    #         self.texture = Button.click
    #         self.clicked = True
    #     else:
    #         self.texture = Button.base
    #         self.clicked = False

    def do_sth(self):
        if self.clicked:
            self.function()
