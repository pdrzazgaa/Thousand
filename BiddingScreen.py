import pygame.event

from CardGUI import CardGUI
from GUISettings import *
from RoundGui import RoundGUI
from Game import Game
from BiddingTable import BiddingTable
from Screen import Screen

# Klasa przedstawiająca graficznie sytuację licytacji podczas rozgrywki
# Dziedziczy po klasie Screen


class BiddingScreen(Screen):
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    game: Game
    cards: [CardGUI]

    def __init__(self, game, display, control_panel, points_table, info_label):
        super().__init__(display, control_panel, info_label, game)
        self.points_table = points_table
        self.all_sprites = pygame.sprite.Group()
        self.show_table = False
        self.bidding_table = BiddingTable(display, game, control_panel, self.info_label)
        self.cards = []
        self.is_dealt = False
        self.is_redealt = False

    def main(self):
        if not self.is_dealt:
            self.cards = self.create_cards()
            self.is_dealt = True
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.control_panel.bidding_phase and \
                            self.game.rounds[-1].bidding.current_bidding_player_id == self.game.id_player:
                        for button in self.bidding_table.buttons:
                            button.do_sth()
        if keys[pygame.K_p]:
            self.show_table = True
        else:
            self.show_table = False

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_cards(self.control_panel.hidden_prikup)
        self.bidding_table.render()
        if self.show_table:
            self.points_table.render()
        self.info_label.render()
        pygame.display.update()

    def create_cards(self):
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[self.game.id_player].cards,
                                                     self.all_sprites)
        opponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        opponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].bidding.prikup, self.all_sprites)

        return player_cards_gui, opponent1_cards_gui, opponent2_cards_gui, prikup_cards_gui

    def display_cards(self, hidden_bidding):
        player_cards_gui, opponent1_cards_gui, opponent2_cards_gui, prikup_cards_gui = self.cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)

        # przeciwnik 1
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 1) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (30, 30))
        RoundGUI.display_oponent_cards(opponent1_cards_gui, True)

        # przeciwnik 2
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 2) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH - 80, 30))
        RoundGUI.display_oponent_cards(opponent2_cards_gui, False)

        self.all_sprites.draw(self.display)
