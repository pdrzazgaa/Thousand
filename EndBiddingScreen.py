import sys
import pygame.event

from CardGUI import CardGUI
from Database import Database
from GUISettings import *
from RoundGui import RoundGUI
from Game import Game
from Button import Button


class EndBiddingScreen:
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    game: Game
    cards: [CardGUI]
    card_for_player_left: ()
    card_for_player_right: ()

    def __init__(self, game, display, control_panel, info_label):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.clicked_card = None
        self.cards = []
        self.is_dealt = False
        self.info_label = info_label
        self.buttons = []
        self.initialize_buttons()

    def main(self):
        if not self.is_dealt:
            self.create_cards()
            self.is_dealt = True
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game.rounds[-1].bidding.last_bidding_player_id == self.game.id_player:
                        self.card_clicked()
                        for button in self.buttons:
                            button.do_sth()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_cards()
        self.waiting_for_dealing_cards_label()
        if self.game.rounds[-1].bidding.bidding_player_round.player.id_player == self.game.id_player:
            for b in self.buttons:
                b.render(point_button_clicked=True)
        self.info_label.render()
        pygame.display.update()

    def create_cards(self):
        self.all_sprites.empty()
        self.cards = []

        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                     [self.game.id_player].cards, self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)

        left_player_card_for = self.game.rounds[-1].bidding.cards_for_other_players[0]
        right_player_card_for = self.game.rounds[-1].bidding.cards_for_other_players[1]

        card_for_left_player = RoundGUI.create_cards_gui([left_player_card_for[0]], self.all_sprites) if \
            left_player_card_for != () else -1
        card_for_right_player = RoundGUI.create_cards_gui([right_player_card_for[0]], self.all_sprites) if \
            right_player_card_for != () else -1

        self.cards = player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, card_for_left_player, \
                     card_for_right_player

    def display_cards(self):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, card_for_left_player, card_for_right_player = \
            self.cards

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

        # Karta dla lewego gracza
        if card_for_left_player != -1:
            RoundGUI.display_card(card_for_left_player.sprites()[0], 200, 250)

        # Karta dla prawego gracza
        if card_for_right_player != -1:
            RoundGUI.display_card(card_for_right_player.sprites()[0], WIDTH - 200 - CARD_WIDTH, 250)

        self.all_sprites.draw(self.display)

    def waiting_for_dealing_cards_label(self):
        if self.game.rounds[-1].bidding.bidding_player_round.player.id_player == self.game.id_player:
            message_waiting = FONT_INFO_AFTER_BIDDING.render("CHOOSE CARDS FOR YOUR OPPONENTS", True, (255, 255, 255),
                                                             BACKGROUND_COLOR)
            self.display.blit(message_waiting, (WIDTH / 2 - message_waiting.get_width() / 2, 150))
        else:
            message_waiting = FONT_INFO_AFTER_BIDDING.render("WINNER CHOOSES CARDS...", True, (255, 255, 255),
                                                             BACKGROUND_COLOR)
            self.display.blit(message_waiting, (WIDTH / 2 - message_waiting.get_width() / 2, 150))

    def initialize_buttons(self):
        # self.buttons.append(Button(self, (WIDTH / 2), 160, 150, 60,
        #                            FONT_BIDDING_PLAYERS.render("BOMB", True, (0, 0, 0)), self.use_bomb,
        #                            self.display))
        self.buttons.append(Button(self, (WIDTH / 2 - 80), 280, 120, 60,
                                   FONT_BIDDING_PLAYERS.render("Left player", True, (0, 0, 0)),
                                   self.card_for_left_player, self.display))
        self.buttons.append(Button(self, (WIDTH / 2 + 80), 280, 120, 60,
                                   FONT_BIDDING_PLAYERS.render("Right player", True, (0, 0, 0)),
                                   self.card_for_right_player, self.display))
        self.buttons.append(Button(self, (WIDTH / 2), 350, 170, 60,
                                   FONT_BIDDING_PLAYERS.render("Accept", True, (0, 0, 0)),
                                   self.accept, self.display))

    def use_bomb(self):
        self.game.rounds[-1].used_bomb(self.game.id_player)

    def card_for_left_player(self):
        card_for_player_left = self.game.rounds[-1].bidding.cards_for_other_players[0]
        if card_for_player_left == ():
            if self.clicked_card.card is not None:
                bidding = self.game.rounds[-1].bidding
                self.game.rounds[-1].bidding.cards_for_other_players[0] = (bidding.pop_card(self.clicked_card.card),
                                                                           self.game.rounds[-1].players_rounds[
                                                                               (self.game.id_player + 1) % 3])
            else:
                self.info_label.show_label("No card has been chosen")
        else:
            self.game.rounds[-1].players_rounds[self.game.id_player].add_card(card_for_player_left[0])
            self.game.rounds[-1].bidding.cards_for_other_players[0] = ()
        self.create_cards()

    def card_for_right_player(self):
        card_for_player_right = self.game.rounds[-1].bidding.cards_for_other_players[1]
        if card_for_player_right == ():
            if self.clicked_card.card is not None:
                bidding = self.game.rounds[-1].bidding
                self.game.rounds[-1].bidding.cards_for_other_players[1] = (bidding.pop_card(self.clicked_card.card),
                                                                           self.game.rounds[-1].players_rounds[
                                                                               (self.game.id_player + 2) % 3])
            else:
                self.info_label.show_label("No card has been chosen")
        else:
            self.game.rounds[-1].players_rounds[self.game.id_player].add_card(card_for_player_right[0])
            self.game.rounds[-1].bidding.cards_for_other_players[1] = ()
        self.create_cards()

    def accept(self):
        if self.game.rounds[-1].bidding.cards_for_other_players[0] != () and \
                self.game.rounds[-1].bidding.cards_for_other_players[1] != ():
            self.game.rounds[-1].bidding.give_away_cards()
            self.game.rounds[-1].send_dealing_to_database(info_label=self.info_label, game_id=self.game.id_game,
                                                          round_id=self.game.rounds[-1].id_r)
        else:
            self.info_label.show_label("Cards for the opponents haven't been chosen")

    def card_clicked(self):
        pos = pygame.mouse.get_pos()
        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(pygame.MOUSEBUTTONDOWN)
            if self.clicked_card:
                self.clicked_card.update(pygame.MOUSEBUTTONDOWN)
            self.clicked_card = clicked_sprites[len(clicked_sprites) - 1]

    def quit(self):
        Database.leave_game(self.game.id_game, self.info_label)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit()
