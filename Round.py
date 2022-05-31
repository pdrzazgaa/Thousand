from Bidding import Bidding
from Card import Card, CardGUI
import random
from PlayerRound import PlayerRound
import pygame
from GUISettings import *
from Settings import ACE, TEN, KING, QUEEN, JACK, NINE, HEART, DIAMONDS, CLUBS, SPADES


class Round:
    __players_rounds: [PlayerRound]
    __bidding: Bidding
    __desk: [Card]
    __atu: int  # wiodący kolor

    def __init__(self, players_rounds, dealing_player_id):
        self.__players_rounds = players_rounds
        self.__bidding = Bidding((dealing_player_id + 1) % 3)
        self.__desk = []

        self.deal_cards(dealing_player_id)

    #   licytacja
    #   gra

    @property
    def bidding(self):
        return self.__bidding

    @staticmethod
    def shuffle_cards():
        cards = []
        for color in range(SPADES, HEART + 1):
            for value in range(NINE, ACE + 1):
                cards.append(Card(color, value))
        random.shuffle(cards)
        return cards

    def deal_cards(self, dealing_player_id):
        cards = self.shuffle_cards()
        for i_card in range(0, len(cards) - 3):
            id_player = (dealing_player_id + i_card + 1) % 3
            self.__players_rounds[id_player].add_card(cards[i_card])
        for i_card in range(len(cards) - 3, len(cards)):
            self.__bidding.add_card_to_prikup(cards[i_card])


class RoundGUI:

    @staticmethod
    def create_cards_gui(cards, all_sprites):
        all_cards = pygame.sprite.Group()
        for card in cards:
            gui_card = CardGUI(card)
            all_cards.add(gui_card)
            all_sprites.add(gui_card)
        return all_cards

    @staticmethod
    def display_player_cards(player_cards_gui):
        gui_cards = player_cards_gui
        left = WIDTH/2 - (((len(player_cards_gui) - 1) * (CARD_WIDTH + CARD_OFFSET) + CARD_WIDTH)/2)
        for card in gui_cards:
            card.card.is_reversed = False
            card.left = left
            card.top = CARD_LOCATION_TOP if not card.is_clicked else CARD_LOCATION_TOP - CARD_OFFSET_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_image
            card.rect = card.image.get_rect(center=(card.left+CARD_WIDTH/2, card.top+CARD_HEIGHT/2))

    @staticmethod
    def display_oponent_cards(oponent_cards_gui, player: int):
        gui_cards = oponent_cards_gui
        top = HEIGHT / 2 - float(len(oponent_cards_gui) / 2) * (CARD_WIDTH / 2)
        for card in gui_cards:
            card.card.is_reversed = True
            card.top = top
            if player % 2 == 0:
                card.left = OPPONENT_CARD_LOCATION_LEFT
            else:
                card.left = OPPONENT_CARD_LOCATION_RIGHT
            top += CARD_WIDTH + OPPONENT_CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_back_image
            if player % 2 == 0:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_LEFT_CARDS)
            else:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_RIGHT_CARDS)
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_bidding_cards(bidding_cards_gui, is_covered):
        gui_cards = bidding_cards_gui
        left = WIDTH / 2 - float(len(bidding_cards_gui) / 2) * (CARD_WIDTH + CARD_OFFSET/2)
        for card in gui_cards:
            card.left = left
            card.top = BIDDING_LOCATION_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_back_image if is_covered else card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))
            card.card.is_reversed = is_covered

