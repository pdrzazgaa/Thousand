import sys
import pygame.event

from Card import CardGUI
from Database import Database
from GUISettings import *
from Round import RoundGUI
from Game import Game
from Button import Button


class EndBiddingScreen:
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    game: Game
    cards: [CardGUI]

    def __init__(self, game, display, control_panel):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.clicked_card = None
        self.cards = []
        self.is_dealt = False
        self.buttons = []
        self.initialize_buttons()

    def main(self):
        if not self.is_dealt:
            self.cards = self.create_cards()
            self.is_dealt = True
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.control_panel.bidding_phase and \
                            self.game.rounds[-1].bidding.current_bidding_player_id == self.game.id_player:
                        for button in self.buttons:
                            button.do_sth()
                if self.control_panel.end_bidding_phase and \
                        self.game.rounds[-1].bidding.bidding_player_round.player.id_player == self.game.id_player:
                    self.card_clicked()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_cards()
        self.waiting_for_dealing_cards_label()
        if self.game.rounds[-1].bidding.bidding_player_round.player.id_player == self.game.id_player:
            for b in self.buttons:
                b.render(False)
        pygame.display.update()

    def create_cards(self):
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                     [self.game.id_player].cards, self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui

    def display_cards(self):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui= self.cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
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

        self.all_sprites.draw(self.display)

    def waiting_for_dealing_cards_label(self):
        if self.game.rounds[-1].bidding.bidding_player_round.player.id_player == self.game.id_player:
            message_waiting = FONT_INFO_AFTER_BIDDING.render("CHOOSE CARDS FOR YOUR OPPONENTS", True, (255, 255, 255),
                                                             BACKGROUND_COLOR)
            self.display.blit(message_waiting, (130, 50))
        else:
            message_waiting = FONT_INFO_AFTER_BIDDING.render("WINNER CHOOSES CARDS...", True, (255, 255, 255),
                                                             BACKGROUND_COLOR)
            self.display.blit(message_waiting, (280, 50))

    def initialize_buttons(self):
        self.buttons.append(Button(self, (WIDTH / 2), 160, 150, 60,
                                   FONT_BIDDING_PLAYERS.render("BOMB", True, (0, 0, 0)), self.use_bomb,
                                   self.display))
        self.buttons.append(Button(self, (WIDTH / 2 - 80), 230, 120, 60,
                                   FONT_BIDDING_PLAYERS.render("Left player", True, (0, 0, 0)),
                                   self.card_for_left_player, self.display))
        self.buttons.append(Button(self, (WIDTH / 2 + 80), 230, 120, 60,
                                   FONT_BIDDING_PLAYERS.render("Right player", True, (0, 0, 0)),
                                   self.card_for_right_player, self.display))

    def use_bomb(self):
        self.game.rounds[-1].used_bomb(self.game.id_player)

    def card_for_left_player(self):
        ...

    def card_for_right_player(self):
        ...

    def card_clicked(self):
        pos = pygame.mouse.get_pos()
        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(pygame.MOUSEBUTTONDOWN)
            if self.clicked_card:
                self.clicked_card.update(pygame.MOUSEBUTTONDOWN)
            self.clicked_card = clicked_sprites[len(clicked_sprites) - 1]

    def quit(self):
        Database.leave_game(self.game.id_game)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit()
