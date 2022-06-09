import ControlPanel
from EndGameScreen import EndGameScreen
from GUISettings import *
from ControlPanel import ControlPanel
from InfoLabel import InfoLabel
from PlayerLeftGameScreen import PlayerLeftGameScreen
from PointsTable import PointsTable
from WaitingForPlayersScreen import WaitingForPlayersScreen
from DealingCardsScreen import DealingCardsScreen
from BiddingScreen import BiddingScreen
from EndBiddingScreen import EndBiddingScreen
from GameScreen import GameScreen

# Klasa główna kontrolująca grę, tutaj dzieje się cała akcja.
# W zależności od stanu gry wyświetlają się odpowiednie ekrany


class Desk:
    frame_per_sec: pygame.time.Clock()
    display_surface: pygame.display

    def __init__(self, game):
        pygame.init()
        self.prepare_game()
        self.info_label = InfoLabel(self.display_surface)
        self.panel_control = ControlPanel(game, self.info_label)
        self.points_table = PointsTable(game, self.display_surface, self.panel_control)
        self.waiting_screen = WaitingForPlayersScreen(game, self.display_surface, self.panel_control, self.info_label)
        self.player_left_game_screen = PlayerLeftGameScreen(game, self.display_surface, self.panel_control,
                                                            self.info_label)
        self.end_game_screen = EndGameScreen(game, self.display_surface, self.panel_control, self.points_table,
                                             self.info_label)

        self.dealing_screen = None
        self.bidding_screen = None
        self.end_bidding_screen = None
        self.game_screen = None
        self.create_new_round(game)

        while True:
            while self.panel_control.waiting_for_players_phase:
                self.waiting_screen.main()
            while self.panel_control.dealing_phase:
                self.dealing_screen.main()
                while self.panel_control.bidding_phase:
                    if self.panel_control.player_left_game_phase:
                        self.player_left_game_screen.main()
                    else:
                        self.bidding_screen.main()
                while self.panel_control.end_bidding_phase:
                    if self.panel_control.player_left_game_phase:
                        self.player_left_game_screen.main()
                    else:
                        self.end_bidding_screen.main()
            while self.panel_control.game_phase:
                if self.panel_control.player_left_game_phase:
                    self.player_left_game_screen.main()
                else:
                    self.game_screen.main()
            while self.panel_control.end_game_phase:
                self.end_game_screen.main()
            self.create_new_round(game)

    def prepare_game(self):
        vec = pygame.math.Vector2  # 2 for two dimensional
        self.frame_per_sec = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("1000")

    def create_new_round(self, game):
        self.dealing_screen = DealingCardsScreen(game, self.display_surface, self.panel_control, self.info_label)
        self.bidding_screen = BiddingScreen(game, self.display_surface, self.panel_control, self.points_table,
                                            self.info_label)
        self.end_bidding_screen = EndBiddingScreen(game, self.display_surface, self.panel_control, self.points_table,
                                                   self.info_label)
        self.game_screen = GameScreen(game, self.display_surface, self.panel_control, self.points_table,
                                      self.info_label)

