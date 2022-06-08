import sys

import pygame

from Database import Database


class Screen:

    def __init__(self, display, control_panel, info_label, game):
        self.display = display
        self.control_panel = control_panel
        self.info_label = info_label
        self.game = game

    def main(self):
        ...

    def manage_display(self):
        ...

    def handle_clicks(self):
        ...

    def quit(self):
        Database.leave_game(self.game.id_game, self.info_label)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit(0)
