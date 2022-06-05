import sys
import pygame.event

from Button import Button
from Card import CardGUI
from Database import Database
from GUISettings import *
from Round import RoundGUI


class GameScreen:
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    cards: [CardGUI]
    event_list: []
    is_done: bool

    def __init__(self, game, display, control_panel):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.is_done = False
        self.clicked_card = None
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
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.card_clicked()
                    if self.game.rounds[-1].current_id_player == self.game.id_player:
                        for button in self.buttons:
                            button.do_sth()
            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        if self.cards:
            self.display_cards()

        if self.game.id_player == self.game.rounds[-1].current_id_player:
            for button in self.buttons:
                button.render(False)
        else:
            message_waiting = FONT_INFO_AFTER_BIDDING.render \
                ("PLAYER'S %i TURN" % self.game.rounds[-1].current_id_player, True, (255, 255, 255), BACKGROUND_COLOR)
            self.display.blit(message_waiting, (WIDTH - 50, 50))
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
        desk_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].desk, self.all_sprites)

        self.cards = player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, desk_cards_gui

    def display_cards(self):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, desk_cards_gui = self.cards
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

        RoundGUI.display_desk(desk_cards_gui, self.game.id_player, self.game.rounds[-1].current_id_player)

        self.all_sprites.draw(self.display)

    def initialize_buttons(self):
        self.buttons.append(Button(self, (WIDTH / 2), 60, 150, 60,
                                   FONT_BIDDING_PLAYERS.render("Make move", True, (0, 0, 0)), self.make_move,
                                   self.display))

    def make_move(self):
        if self.clicked_card.card is not None:
            color = self.clicked_card.card.color
            value = self.clicked_card.card.value
            # Na razie domyślnie fałsz
            if_queen_king_pair = False
            Database.make_move(self.game.rounds[-1].id_r, self.game.id_player, color, value,
                               if_queen_king_pair)
            # self.game.rounds[-1].players_rounds[self.game.id_player].play_card(
            #     self.game.rounds[-1].desk, self.game.id_player, self.clicked_card.card)
            self.clicked_card = None
            # self.create_cards()
        else:
            print("Nie wybrano karty")

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
