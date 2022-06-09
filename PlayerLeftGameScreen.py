import pygame.mouse

from GUISettings import *
from Button import Button
from Screen import Screen

# Klasa przedstawiająca graficznie sytuację w momencie opuszczenia przez przeciwnika gry
# Dziedziczy po klasie Screen


class PlayerLeftGameScreen(Screen):
    display: pygame.display

    def __init__(self, game, display, control_panel, info_label):
        super().__init__(display, control_panel, info_label, game)
        self.buttons = []
        self.initialize_buttons()

    def main(self):
        self.turn_off_game()
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
        message_waiting = FONT_WAITING.render("YOUR OPPONENT LEFT THE GAME", True, (255, 255, 255), BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH / 2 - message_waiting.get_width() / 2, 150))
        for button in self.buttons:
            button.render(False)
        self.info_label.render()
        pygame.display.update()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 550, 550, 400, 80,
                                   FONT_BUTTON.render("QUIT", True, (0, 0, 0)), self.quit, self.display))

    def turn_off_game(self):
        for timer in self.control_panel.timers:
            timer.cancel()
