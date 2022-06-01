import pygame

from Card import Card
from Player import Player
from Settings import ACE, TEN, KING, QUEEN, JACK, NINE, HEART, DIAMONDS, CLUBS, SPADES


class PlayerRound:
    __player: Player
    __cards: [Card]
    __collected_cards: [Card]
    __points = 0
    __declared_points = 0
    __pairs: [bool]

    def __init__(self, player):
        self.__cards = []
        self.__collected_cards = []
        self.__player = player

    def take_cards(self, taken_card):
        for card in taken_card:
            self.__points += card.points[card.value]
            self.__collected_cards.append(card)

    def add_card(self, card):
        self.__cards.append(card)

    @property
    def player(self):
        return self.__player

    @property
    def declared_points(self):
        return self.__declared_points

    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, cards):
        self.__cards = cards

    @declared_points.setter
    def declared_points(self, declared_points):
        self.__declared_points = declared_points

    def check_pairs(self):
        for color in range(SPADES, HEART + 1):
            if Card(color, QUEEN) in self.__cards and Card(color, KING) in self.__cards:
                self.__pairs[color-1] = True

    def check_points(self):
        points = 0
        for card in self.__cards:
            points += Card.points[card.value]
        return points

    def check_nines(self):
        nines = 0
        for card in self.__cards:
            if card.value == NINE:
                nines += 1
        return nines == 4

    def play_card(self, card_id):
        card = self.__cards.pop(card_id)
        return card

    def sort_cards(self):
        self.__cards.sort(key=lambda card: (card.color, card.value), reverse=True)


class PlayerRoundGUI(pygame.sprite.Sprite):
    ...