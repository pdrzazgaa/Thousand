from datetime import datetime

import pygame
from GUISettings import INFO_WIDTH, INFO_HEIGHT, INFO_LEFT, INFO_TOP, INFO_BACKGROUND_COLOR, INFO_TEXT_COLOR, FONT_INFO, \
    WIDTH


class InfoLabel:

    def __init__(self, display, width=INFO_WIDTH, height=INFO_HEIGHT):
        self.x = INFO_LEFT
        self.y = INFO_TOP
        self.height = height
        self.width = width
        self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.moved = False
        self.display = display
        self.visible = True
        self.if_display_text = True
        self.start_time = datetime.now()
        self.visible = False
        self.message = None

    def show_label(self, text):
        self.visible = True
        self.message = FONT_INFO.render(text, True, INFO_TEXT_COLOR)

    def render(self):
        self.display_label_in_time()

    def display_label_in_time(self):
        # Napis wyświetlamy tylko przez 5 sekund
        if self.visible:
            if not self.if_display_text:
                self.if_display_text = True
                self.start_time = datetime.now()
            if self.if_display_text:
                self.display_rectangle()
                self.display_label()
                if (datetime.now() - self.start_time).total_seconds() > 5:
                    self.if_display_text = False
                    self.visible = False

    def display_label(self):
        self.message.set_alpha(240)
        self.display.blit(self.message, (WIDTH/2 - self.message.get_width()/2, self.height/2 - self.message.get_height()/2))

    def display_rectangle(self):
        transparent_rect = pygame.Surface((self.message.get_width() + 50, self.height))
        transparent_rect.set_alpha(128)
        transparent_rect.fill(INFO_BACKGROUND_COLOR)
        self.display.blit(transparent_rect, (self.x, self.y))

    def check_if_disturbed(self):
        mouse = pygame.mouse.get_pos()
        if self.hit_box.x < mouse[0] < self.hit_box.x + self.hit_box.width and \
           self.hit_box.y < mouse[1] < self.hit_box.y + self.hit_box.height:
            self.moved = True
        else:
            self.moved = False

    def do_sth(self):
        if self.moved:
            self.if_display_text = False
            self.visible = False
