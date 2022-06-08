import sys
import pygame.event

from Button import Button
from CardGUI import CardGUI
from Database import Database
from GUISettings import *
from RoundGui import RoundGUI
from Screen import Screen


class GameScreen(Screen):
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    cards: [CardGUI]
    event_list: []
    is_done: bool

    def __init__(self, game, display, control_panel, points_table, info_label):
        super().__init__(display, control_panel, info_label, game)
        self.points_table = points_table
        self.all_sprites = pygame.sprite.Group()
        self.is_done = False
        self.clicked_card = None
        self.show_table = False
        self.cards = []
        self.buttons = []
        self.initialize_buttons()

    def main(self):
        if len(self.cards) == 0 or self.control_panel.made_move:
            self.create_cards()
            self.control_panel.made_move = False
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.card_clicked()
                    if self.game.rounds[-1].current_id_player == self.game.id_player:
                        for button in self.buttons:
                            button.do_sth()
            if event.type == pygame.QUIT:
                self.quit()
        if keys[pygame.K_p]:
            self.show_table = True
        else:
            self.show_table = False

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        if not self.control_panel.end_round_phase:
            if self.cards:
                self.display_cards()
                self.display_labels()

            if not self.control_panel.full_desk:
                if self.game.id_player == self.game.rounds[-1].current_id_player:
                    for button in self.buttons:
                        button.render(point_button_clicked=True)
            else:
                for button in self.buttons:
                    button.clicked = False

            if self.show_table:
                self.display_table()
        else:
            self.display_table()
        self.info_label.render()
        pygame.display.update()

    def create_cards(self):
        self.all_sprites.empty()
        self.cards = []
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[self.game.id_player].cards,
                                                     self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)
        desk_cards_gui = RoundGUI.create_cards_desk(self.game.rounds[-1].desk, self.all_sprites)

        self.cards = player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, desk_cards_gui

    def display_cards(self):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, desk_cards_gui = self.cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_oponent_cards(oponent1_cards_gui, True)
        RoundGUI.display_oponent_cards(oponent2_cards_gui, False)
        RoundGUI.display_desk(desk_cards_gui, self.game.id_player)
        self.all_sprites.draw(self.display)

    def display_labels(self):

        # gracz
        id_p = self.game.id_player
        message_waiting = FONT_POINTS_GAME.render(self.choose_text(id_p), True, self.choose_color(id_p),
                                                  BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH - message_waiting.get_width() - 10, HEIGHT - 40))

        # przeciwnik 1
        id_op1 = (self.game.id_player + 1) % 3
        message_waiting = FONT_INFO_AFTER_BIDDING.render(self.choose_text(id_op1), True,
                                                         self.choose_color(id_op1), BACKGROUND_COLOR)
        self.display.blit(message_waiting, (10, 30))

        # przeciwnik 2
        id_op2 = (self.game.id_player + 2) % 3
        message_waiting = FONT_INFO_AFTER_BIDDING.render(self.choose_text(id_op2), True,
                                                         self.choose_color(id_op2), BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH - message_waiting.get_width() - 10, 30))

    def choose_color(self, id_player):
        if id_player == self.game.rounds[-1].current_id_player:
            return COLOR_ORANGE
        else:
            return COLOR_WHITE

    def choose_text(self, id_p):
        points = self.game.rounds[-1].players_rounds[id_p].points
        if id_p == self.game.id_player:
            if id_p == self.game.rounds[-1].bidding.bidding_player_round.player.id_player:
                return "Points: [%i/%i]" % (points, self.game.rounds[-1].bidding.bid)
            else:
                return "Points: [%i]" % points
        else:
            if id_p == self.game.rounds[-1].bidding.bidding_player_round.player.id_player:
                return "P%i: [%i/%i]" % (id_p, points, self.game.rounds[-1].bidding.bid)
            else:
                return "P%i: [%i]" % (id_p, points)

    def display_table(self):
        self.points_table.render()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 100, HEIGHT - 60, 150, 60,
                                   FONT_BIDDING_PLAYERS.render("Make move", True, (0, 0, 0)), self.make_move,
                                   self.display))

    def make_move(self):
        if self.clicked_card is not None:
            if self.game.rounds[-1].players_rounds[self.game.id_player].check_if_can_make_move\
                    (self.clicked_card.card, self.game.rounds[-1].desk[self.game.rounds[-1].initial_move_player_id]):
                self.game.rounds[-1].players_rounds[self.game.id_player].make_move\
                    (self.clicked_card, self.game.rounds[-1].initial_move_player_id, self.game.rounds[-1].id_r,
                     self.info_label)
                self.clicked_card = None
            else:
                self.info_label.show_label("Play a card with the same color as the initial one")
                for b in self.buttons:
                    b.set_clicked = False
        else:
            self.info_label.show_label("No card has been chosen")
            for b in self.buttons:
                b.set_clicked = False

    def card_clicked(self):
        pos = pygame.mouse.get_pos()
        clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
        if len(clicked_sprites) != 0:
            clicked_sprites[len(clicked_sprites) - 1].update(pygame.MOUSEBUTTONDOWN)
            if self.clicked_card:
                self.clicked_card.update(pygame.MOUSEBUTTONDOWN)
            self.clicked_card = clicked_sprites[len(clicked_sprites) - 1]
