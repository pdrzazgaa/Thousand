from GUISettings import *
import pygame


class Button:
    # base = pygame.image.load("textures\\Button_base.xcf")
    # click = pygame.image.load("textures\\Button_click.xcf")

    def __init__(self, menu, x, y, width, height, name, function, display):
        self.menu = menu
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = name
        self.name = FONT_BUTTON.render(name, True, (0, 0, 0))
        self.function = function
        self.hit_box = pygame.Rect(x - width / 2, y - width / 2, width, height)
        self.clicked = False
        # self.texture = Button.base
        self.display = display

    def render(self):
        # self.choose_texture()
        pygame.draw.rect(self.display, (255, 255, 255), self.hit_box)
        # texture_copy = pygame.transform.scale(self.texture, (self.width, self.height))
        # self.display.blit(texture_copy, (self.x - self.width/2, self.y - self.height * 2.5))
        self.display.blit(self.name,
                          (self.x - self.name.get_width() / 2, self.y - self.height * 2.25))

    # def choose_texture(self):
    #     if self.hit_box.x < self.menu.mouse_x < self.hit_box.x + self.hit_box.width and\
    #        self.hit_box.y < self.menu.mouse_y < self.hit_box.y + self.hit_box.height:
    #         self.texture = Button.click
    #         self.clicked = True
    #     else:
    #         self.texture = Button.base
    #         self.clicked = False

    def do_sth(self):
        self.function()
