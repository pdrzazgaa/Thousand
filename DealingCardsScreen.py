import sys

from Card import CardGUI
from Database import Database
from GUISettings import *
from PlayerRound import PlayerRound
from Round import Round, RoundGUI


class DealingCardsScreen:

    display: pygame.display
    all_sprites: pygame.sprite.Group()
    cards: [CardGUI]

    def __init__(self, game, display, control_panel):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.cards = self.create_cards()

    def main(self):
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.card_clicked()
            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        # message_waiting = FONT_WAITING.render("WAITING FOR OTHER PLAYERS", True, (255, 255, 255), BACKGROUND_COLOR)
        # message_players = FONT_CURRENT_PLAYERS.render("Currently in game: %i player(s)" %
        #                                               self.control_panel.current_players_in_game, True, (255, 255, 255),
        #                                               BACKGROUND_COLOR)
        # self.display.blit(message_waiting, (100, 150))
        # self.display.blit(message_players, (300, 350))
        self.display_cards(self.control_panel.end_bidding_phase, self.cards)
        pygame.display.update()

    def create_cards(self):
        # Tworzymy rundy graczy
        player0_round = PlayerRound(self.game.players[self.game.id_player])
        player1_round = PlayerRound(self.game.players[(self.game.id_player + 1) % 3])
        player2_round = PlayerRound(self.game.players[(self.game.id_player + 2) % 3])
        # Zaczynamy rundę z 3 graczami, ze wskazanym graczem rozdającym
        dealing_player = 0 if len(self.game.rounds) == 0 else \
            self.game.rounds[len(self.game.rounds) - 1].dealing_player_id
        game_round = Round([player0_round, player1_round, player2_round], dealing_player)
        self.game.add_round_to_game(game_round)
        player0_round.sort_card()
        # tworzymy karty
        player_cards_gui = RoundGUI.create_cards_gui(player0_round.cards, self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(player1_round.cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(player2_round.cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(game_round.bidding.prikup, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui

    def display_cards(self, hidden_bidding, cards):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui = cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)
        RoundGUI.display_oponent_cards(oponent1_cards_gui, (self.game.id_player + 1) % 3)
        RoundGUI.display_oponent_cards(oponent2_cards_gui, (self.game.id_player + 2) % 3)

        self.display.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.display)
        pygame.display.update()

    def card_clicked(self):
        pos = pygame.mouse.get_pos()

        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(pygame.event.get())
            pygame.display.update()

    def quit(self):
        Database.leave_game(self.game.id_game)
        pygame.quit()
        sys.exit()

