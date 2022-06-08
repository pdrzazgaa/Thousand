import pygame
from GUISettings import BUTTON_COLOR_DISTURBED, BUTTON_COLOR_ENABLED, BUTTON_COLOR_CLICKED


class Button:

    def __init__(self, menu, x, y, width, height, name, function, display):
        self.menu = menu
        self.x = x
        self.y = y
        self.height = height
        self.text = name
        self.width = width
        self.name = name
        self.function = function
        self.hit_box = pygame.Rect(x - width / 2, y - height / 2, width, height)
        self.moved = False
        self.clicked = False
        self.button_color = BUTTON_COLOR_ENABLED
        self.display = display

    def render(self, point_button_clicked=False, disabled=False):
        self.check_if_disturbed()
        if disabled:
            self.button_color = BUTTON_COLOR_CLICKED
        elif point_button_clicked and self.clicked:
            self.button_color = BUTTON_COLOR_CLICKED
        elif self.moved:
            self.button_color = BUTTON_COLOR_DISTURBED
        else:
            self.button_color = BUTTON_COLOR_ENABLED
        pygame.draw.rect(self.display, self.button_color, self.hit_box)
        self.display.blit(self.name,
                          (self.x - self.name.get_width() / 2, self.y-self.name.get_height()/2))

    def check_if_disturbed(self):
        mouse = pygame.mouse.get_pos()
        if self.hit_box.x < mouse[0] < self.hit_box.x + self.hit_box.width and \
           self.hit_box.y < mouse[1] < self.hit_box.y + self.hit_box.height:
            self.moved = True
        else:
            self.moved = False

    def do_sth(self):
        if self.moved:
            self.clicked = not self.clicked
            if self.clicked:
                self.function()
