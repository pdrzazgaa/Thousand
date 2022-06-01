import sys
import ControlPanel
from Player import Player
from Database import Database
from GUISettings import *
from ControlPanel import ControlPanel
from Timer import RepeatedTimer
from WaitingForPlayersScreen import WaitingForPlayersScreen
from DealingCardsScreen import DealingCardsScreen


class Desk:
    frame_per_sec: pygame.time.Clock()
    display_surface: pygame.display
    event_list: []

    def __init__(self, game):
        pygame.init()
        self.prepare_game()
        self.panel_control = ControlPanel()
        self.waiting_screen = WaitingForPlayersScreen(game, self.display_surface, self.panel_control)
        self.dealing_screen = DealingCardsScreen(game, self.display_surface, self.panel_control)

        # Timery sprawdzające bazę - czy są jacyś gracze
        timer_check_players = RepeatedTimer(2.0, self.panel_control.check_players, game.id_game)
        timer_check_players.start()

        while True:
            while self.panel_control.waiting_for_players_phase:
                self.waiting_screen.main()
            while self.panel_control.dealing_phase:
                self.dealing_screen.main()
            while self.panel_control.bidding_phase:
                ...
            while self.panel_control.game_phase:
                while self.panel_control.player0_phase:
                    ...
                while self.panel_control.player1_phase:
                    ...
                while self.panel_control.player2_phase:
                    ...

    def prepare_game(self):
        vec = pygame.math.Vector2  # 2 for two dimensional
        self.frame_per_sec = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("1000")


    @staticmethod
    def quit(game):
        Database.leave_game(game.id_game)
        pygame.quit()
        sys.exit()
