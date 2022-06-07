import sys

import pygame.mouse

from Database import Database
from GUISettings import *
from Button import Button


class WaitingForPlayersScreen:
    display: pygame.display

    def __init__(self, game, display, control_panel, info_label):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.info_label = info_label
        self.buttons = []
        self.initialize_buttons()

    def main(self):
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 550, 550, 400, 80,
                                   FONT_BUTTON.render("QUIT", True, (0, 0, 0)), self.quit, self.display))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()
                    self.info_label("Game created by: Paulina Drzazga")

            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        message_waiting = FONT_WAITING.render("WAITING FOR OTHER PLAYERS", True, (255, 255, 255), BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH/2 - message_waiting.get_width()/2, 150))
        if self.control_panel.currently_players_in_game != -1:
            message_players = FONT_CURRENT_PLAYERS.render("Currently in game: %i player(s)" %
                                                          self.control_panel.currently_players_in_game, True,
                                                          (255, 255, 255),
                                                          BACKGROUND_COLOR)
            self.display.blit(message_players, (WIDTH/2 - message_players.get_width()/2, 350))
        for button in self.buttons:
            button.render(False)
        self.info_label.render()
        pygame.display.update()

    def quit(self):
        Database.leave_game(self.game.id_game, self.info_label)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit()
