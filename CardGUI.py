import pygame

from GUISettings import CARD_HEIGHT, CARD_WIDTH, CARD_OFFSET_TOP
from Card import Card

# Klasa przedstawiająca graficznie karty na ekranie

cards_images = [[pygame.image.load("CardsIMG/card11.png"),
                 pygame.image.load("CardsIMG/card12.png"),
                 pygame.image.load("CardsIMG/card13.png"),
                 pygame.image.load("CardsIMG/card14.png"),
                 pygame.image.load("CardsIMG/card15.png"),
                 pygame.image.load("CardsIMG/card16.png")
                 ], [pygame.image.load("CardsIMG/card21.png"),
                     pygame.image.load("CardsIMG/card22.png"),
                     pygame.image.load("CardsIMG/card23.png"),
                     pygame.image.load("CardsIMG/card24.png"),
                     pygame.image.load("CardsIMG/card25.png"),
                     pygame.image.load("CardsIMG/card26.png"),
                     ], [pygame.image.load("CardsIMG/card31.png"),
                         pygame.image.load("CardsIMG/card32.png"),
                         pygame.image.load("CardsIMG/card33.png"),
                         pygame.image.load("CardsIMG/card34.png"),
                         pygame.image.load("CardsIMG/card35.png"),
                         pygame.image.load("CardsIMG/card36.png")
                         ], [pygame.image.load("CardsIMG/card41.png"),
                             pygame.image.load("CardsIMG/card42.png"),
                             pygame.image.load("CardsIMG/card43.png"),
                             pygame.image.load("CardsIMG/card44.png"),
                             pygame.image.load("CardsIMG/card45.png"),
                             pygame.image.load("CardsIMG/card46.png"),
                             ]]

card_back_img = pygame.image.load("CardsIMG/card00.png")


class CardGUI(pygame.sprite.Sprite):
    __card_back_image: pygame.image
    __card_image: pygame.image
    __is_clicked: bool
    __card: Card
    __left: int
    __top: int

    def __init__(self, card):
        super().__init__()
        self.__card = card
        v = card.value
        c = card.color
        self.surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.__card_image = cards_images[c - 1][v - 1]
        self.__card_image = pygame.transform.scale(self.__card_image, (CARD_WIDTH, CARD_HEIGHT))
        self.__card_back_image = card_back_img
        self.__card_back_image = pygame.transform.scale(self.__card_back_image, (CARD_WIDTH, CARD_HEIGHT))
        self.left = 0
        self.top = 0
        self.__is_clicked = False

    @property
    def card_image(self):
        return self.__card_image

    @property
    def card_back_image(self):
        return self.__card_back_image

    @property
    def card(self):
        return self.__card

    @property
    def is_clicked(self):
        return self.__is_clicked

    @is_clicked.setter
    def is_clicked(self, is_clicked: bool):
        self.__is_clicked = is_clicked

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left: int):
        self.__left = left

    @property
    def top(self):
        return self.__top

    @top.setter
    def top(self, top):
        self.__top = top

    def click_card(self):
        self.is_clicked = not self.is_clicked
        self.top = self.top - CARD_OFFSET_TOP if self.is_clicked else self.top + CARD_OFFSET_TOP
        self.rect = self.image.get_rect(center=(self.left + CARD_WIDTH / 2, self.top + CARD_HEIGHT / 2))

    def update(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            self.click_card()
