import pygame

from Card import Card
from Player import Player
from Settings import KING, QUEEN, NINE, HEART, DIAMONDS, CLUBS, SPADES, SPADES_POINTS, CLUBS_POINTS, DIAMONDS_POINTS, \
    HEART_POINTS


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
    def collected_cards(self):
        return self.__collected_cards

    @property
    def points(self):
        return self.__points

    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, cards):
        self.__cards = cards
        for card in self.__cards:
            if card is None:
                self.__cards.remove(card)

    @declared_points.setter
    def declared_points(self, declared_points):
        self.__declared_points = declared_points

    def check_pairs(self):
        for color in range(SPADES, HEART + 1):
            if Card(color, QUEEN) in self.__cards and Card(color, KING) in self.__cards:
                self.__pairs[color-1] = True

    def check_if_pair(self, card):
        return card.value == QUEEN and Card(card.color, KING) in self.__cards or card.value == KING and \
               Card(card.color, QUEEN) in self.__cards

    # Będą używane w późniejszych etapach rozwoju gry
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

    def play_card(self, desk, id_player, card, if_queen_king_pair):
        desk[id_player] = self.__cards.pop(self.__cards.index(card))
        if if_queen_king_pair:
            if card.color == SPADES:
                self.__points += SPADES_POINTS
            elif card.color == CLUBS:
                self.__points += CLUBS_POINTS
            elif card.color == DIAMONDS:
                self.__points += DIAMONDS_POINTS
            else:
                self.__points += HEART_POINTS

    def sort_cards(self):
        if self is not None:
            self.__cards.sort(key=lambda card: (card.color, card.value), reverse=True)