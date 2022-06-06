import pygame


class Button:
    # base = pygame.image.load("textures\\Button_base.xcf")
    # click = pygame.image.load("textures\\Button_click.xcf")

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
        self.clicked = False
        # self.texture = Button.base
        self.display = display

    def render(self, disabled):
        self.check_if_clicked()
        if disabled:
            pygame.draw.rect(self.display, (192, 192, 192), self.hit_box)
        else:
            pygame.draw.rect(self.display, (255, 255, 255), self.hit_box)
        # texture_copy = pygame.transform.scale(self.texture, (self.width, self.height))
        # self.display.blit(texture_copy, (self.x - self.width/2, self.y - self.height * 2.5))
        self.display.blit(self.name,
                          (self.x - self.name.get_width() / 2, self.y-self.name.get_height()/2))

    def check_if_clicked(self):
        mouse = pygame.mouse.get_pos()
        if self.hit_box.x < mouse[0] < self.hit_box.x + self.hit_box.width and \
           self.hit_box.y < mouse[1] < self.hit_box.y + self.hit_box.height:
            # self.texture = Button.click
            self.clicked = True
        else:
            # self.texture = Button.base
            self.clicked = False

    def do_sth(self):
        if self.clicked:
            self.function()
