import sys

import pygame.mouse

from Database import Database
from GUISettings import *
from Button import Button
from InfoLabel import InfoLabel


class PlayerLeftGameScreen:
    display: pygame.display

    def __init__(self, game, display, control_panel, info_label):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.buttons = []
        self.info_label = info_label
        self.initialize_buttons()

    def main(self):
        self.turn_off_game()
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

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def turn_off_game(self):
        for timer in self.control_panel.timers:
            timer.cancel()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.info_label.render()
        message_waiting = FONT_WAITING.render("YOUR OPPONENT LEFT THE GAME", True, (255, 255, 255), BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH/2 - message_waiting.get_width()/2, 150))
        for button in self.buttons:
            button.render(False)
        pygame.display.update()

    def quit(self):
        Database.leave_game(self.game.id_game, self.info_label)
        pygame.quit()
        sys.exit()
