from datetime import datetime
import pygame.mouse

from GUISettings import *
from Button import Button
from Screen import Screen

# Klasa przedstawiająca graficznie sytuację zakończenia gry,
# Wyświetla się tabela z wynikami i informacja o wygranej
# Dziedziczy po klasie Screen


class EndGameScreen(Screen):
    display: pygame.display

    def __init__(self, game, display, control_panel, points_table, info_label):
        super().__init__(display, control_panel, info_label, game)
        self.buttons = []
        self.points_table = points_table
        self.initialize_buttons()
        self.if_display_text = True
        self.did_not_display_yet = True
        self.start_time = datetime.now()

    def main(self):
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_table()
        self.display_text_in_time()
        for button in self.buttons:
            button.render(False)
        self.info_label.render()
        pygame.display.update()

    def initialize_buttons(self):
        self.buttons.append(Button(self, WIDTH - 140, 60, 150, 60,
                                   FONT_BUTTON_SMALL.render("QUIT", True, (0, 0, 0)), self.quit, self.display))

    def display_table(self):
        self.points_table.render()

    # Informacja o wygranej bądź przegranej
    def display_text(self):
        if self.game.player_me().check_if_winner():
            text = "YOU WON"
        else:
            text = "YOU LOST"
        message_waiting = FONT_ENDING.render(text, True, COLOR_WHITE)
        message_waiting.set_alpha(200)
        self.display.blit(message_waiting, (WIDTH / 2 - message_waiting.get_width() / 2,
                                            HEIGHT / 2 - message_waiting.get_height() / 2))

    def display_text_in_time(self):
        # Napis wyświetlamy tylko przez 5 sekund
        if not self.if_display_text and self.did_not_display_yet:
            self.if_display_text = True
            self.did_not_display_yet = False
            self.start_time = datetime.now()
        if self.if_display_text:
            self.display_text()
            if (datetime.now() - self.start_time).total_seconds() > 5:
                self.if_display_text = False
