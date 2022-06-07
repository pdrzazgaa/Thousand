import sys
import pygame.event
from Card import CardGUI
from Database import Database
from GUISettings import *
from RoundGui import RoundGUI


class DealingCardsScreen:

    display: pygame.display
    all_sprites: pygame.sprite.Group()
    cards: [CardGUI]
    event_list: []
    is_done: bool

    def __init__(self, game, display, control_panel, info_label):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.is_done = False
        self.cards = []
        self.info_label = info_label

    def main(self):
        if not self.is_done and self.control_panel.waiting_for_dealing_phase and \
                self.game.rounds[-1].dealing_player_id == self.game.id_player:
            self.is_done = True
            self.make_new_deal()
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.card_clicked()
            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        if self.control_panel.waiting_for_dealing_phase:
            self.display.fill(BACKGROUND_COLOR)
            message_waiting = FONT_WAITING.render("DEALING CARDS...", True, (255, 255, 255), BACKGROUND_COLOR)
            self.display.blit(message_waiting, (WIDTH/2 - message_waiting.get_width()/2, 150))
        else:
            if self.control_panel.dealing_phase and not self.cards:
                self.make_new_deal()
            if self.cards:
                self.display_cards(not self.control_panel.end_bidding_phase, self.cards)
        self.info_label.render()
        pygame.display.update()

    def make_new_deal(self):
        self.game.add_round_to_game()
        if self.game.rounds[-1].dealing_player_id == self.game.id_player:
            self.game.rounds[-1].deal_cards()
            for pr in self.game.rounds[-1].players_rounds:
                pr.sort_cards()
            self.game.rounds[-1].send_dealing_to_database(info_label=self.info_label, game_id=self.game.id_game)
            self.cards = self.create_cards()
        else:
            if self.control_panel.dealing_phase and not self.control_panel.waiting_for_dealing_phase:
                self.cards = self.create_cards()

    def create_cards(self):
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[self.game.id_player].cards,
                                                     self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].bidding.prikup, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui

    def display_cards(self, hidden_bidding, cards):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui = cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)

        # przeciwnik 1
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 1) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (30, 30))
        RoundGUI.display_oponent_cards(oponent1_cards_gui, True)

        # przeciwnik 2
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 2) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH - 80, 30))
        RoundGUI.display_oponent_cards(oponent2_cards_gui, False)

        self.display.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.display)
        pygame.display.update()

    def card_clicked(self):
        pos = pygame.mouse.get_pos()
        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(pygame.MOUSEBUTTONDOWN)
            pygame.display.update()

    def quit(self):
        Database.leave_game(self.game.id_game, self.info_label)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit()

