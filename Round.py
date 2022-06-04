from Bidding import Bidding
from Card import Card, CardGUI
import random
from PlayerRound import PlayerRound
from Database import Database
from GUISettings import *
from Settings import ACE, TEN, KING, QUEEN, JACK, NINE, HEART, DIAMONDS, CLUBS, SPADES


class Round:
    __players_rounds: [PlayerRound]
    __bidding: Bidding
    __desk: [Card]
    __atu: int  # wiodący kolor
    __last_round: str
    __last_move: str
    __dealing_player_id: int
    __id_r: int

    def __init__(self, players_rounds, dealing_player_id):
        self.__players_rounds = players_rounds
        self.__bidding = Bidding(players_rounds[(dealing_player_id + 1) % 3])
        self.__desk = []
        self.__dealing_player_id = dealing_player_id
        self.__id_r = 0
        self.__last_round = ""

    @property
    def bidding(self):
        return self.__bidding

    @property
    def players_rounds(self):
        return self.__players_rounds

    @property
    def id_r(self):
        return self.__id_r

    @id_r.setter
    def id_r(self, id_r):
        self.__id_r = id_r

    @property
    def last_round(self):
        return self.__last_round

    @last_round.setter
    def last_round(self, last_round):
        self.__last_round = last_round

    @property
    def dealing_player_id(self):
        return self.__dealing_player_id

    def used_bomb(self, player_id):
        for pr in self.players_rounds:
            if pr.player.id_player != player_id:
                pr.player.add_points(60)
        self.players_rounds[player_id].pla.use_bomb()

    @staticmethod
    def shuffle_cards():
        cards = []
        for color in range(SPADES, HEART + 1):
            for value in range(NINE, ACE + 1):
                cards.append(Card(color, value))
        random.shuffle(cards)
        return cards

    def deal_cards(self):
        cards = self.shuffle_cards()
        for i_card in range(0, len(cards) - 3):
            id_player = (self.__dealing_player_id + i_card + 1) % 3
            self.__players_rounds[id_player].add_card(cards[i_card])
        for i_card in range(len(cards) - 3, len(cards)):
            self.__bidding.add_card_to_prikup(cards[i_card])

    def send_dealing_to_database(self, game_id, round_id):
        p01 = self.__players_rounds[0].cards[0].card_to_sql()
        p02 = self.__players_rounds[0].cards[1].card_to_sql()
        p03 = self.__players_rounds[0].cards[2].card_to_sql()
        p04 = self.__players_rounds[0].cards[3].card_to_sql()
        p05 = self.__players_rounds[0].cards[4].card_to_sql()
        p06 = self.__players_rounds[0].cards[5].card_to_sql()
        p07 = self.__players_rounds[0].cards[6].card_to_sql()
        p08 = "null" if len(self.__players_rounds[0].cards) == 7 else self.__players_rounds[0].cards[7].card_to_sql()
        p11 = self.__players_rounds[1].cards[0].card_to_sql()
        p12 = self.__players_rounds[1].cards[1].card_to_sql()
        p13 = self.__players_rounds[1].cards[2].card_to_sql()
        p14 = self.__players_rounds[1].cards[3].card_to_sql()
        p15 = self.__players_rounds[1].cards[4].card_to_sql()
        p16 = self.__players_rounds[1].cards[5].card_to_sql()
        p17 = self.__players_rounds[1].cards[6].card_to_sql()
        p18 = "null" if len(self.__players_rounds[1].cards) == 7 else self.__players_rounds[1].cards[7].card_to_sql()
        p21 = self.__players_rounds[2].cards[0].card_to_sql()
        p22 = self.__players_rounds[2].cards[1].card_to_sql()
        p23 = self.__players_rounds[2].cards[2].card_to_sql()
        p24 = self.__players_rounds[2].cards[3].card_to_sql()
        p25 = self.__players_rounds[2].cards[4].card_to_sql()
        p26 = self.__players_rounds[2].cards[5].card_to_sql()
        p27 = self.__players_rounds[2].cards[6].card_to_sql()
        p28 = "null" if len(self.__players_rounds[2].cards) == 7 else self.__players_rounds[2].cards[7].card_to_sql()
        pc1 = "null" if len(self.__bidding.prikup) == 0 else self.__bidding.prikup[0].card_to_sql()
        pc2 = "null" if len(self.__bidding.prikup) <= 1 else self.__bidding.prikup[1].card_to_sql()
        pc3 = "null" if len(self.__bidding.prikup) <= 2 else self.__bidding.prikup[2].card_to_sql()
        if round_id == -1:
            Database.deal_cards(str(game_id), p01, p02, p03, p04, p05, p06, p07, p08,
                                p11, p12, p13, p14, p15, p16, p17, p18,
                                p21, p22, p23, p24, p25, p26, p27, p28,
                                pc1, pc2, pc3)
        else:
            Database.update_dealing(str(round_id), p01, p02, p03, p04, p05, p06, p07, p08,
                                    p11, p12, p13, p14, p15, p16, p17, p18,
                                    p21, p22, p23, p24, p25, p26, p27, p28)


class RoundGUI:

    @staticmethod
    def create_cards_gui(cards, all_sprites):
        all_cards = pygame.sprite.Group()
        for card in cards:
            if card is not None:
                gui_card = CardGUI(card)
                all_cards.add(gui_card)
                all_sprites.add(gui_card)
        return all_cards

    @staticmethod
    def display_player_cards(player_cards_gui):
        gui_cards = player_cards_gui
        left = WIDTH / 2 - (((len(player_cards_gui) - 1) * (CARD_WIDTH + CARD_OFFSET) + CARD_WIDTH) / 2)
        for card in gui_cards:
            card.card.is_reversed = False
            card.left = left
            card.top = CARD_LOCATION_TOP if not card.is_clicked else CARD_LOCATION_TOP - CARD_OFFSET_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_oponent_cards(oponent_cards_gui, left: bool):
        gui_cards = oponent_cards_gui
        top = HEIGHT / 2 - float(len(oponent_cards_gui) / 2) * (CARD_WIDTH / 2)
        for card in gui_cards:
            card.card.is_reversed = True
            card.top = top
            if left:
                card.left = OPPONENT_CARD_LOCATION_LEFT
            else:
                card.left = OPPONENT_CARD_LOCATION_RIGHT
            top += CARD_WIDTH + OPPONENT_CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_back_image
            if left:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_LEFT_CARDS)
            else:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_RIGHT_CARDS)
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_bidding_cards(bidding_cards_gui, is_covered):
        gui_cards = bidding_cards_gui
        left = WIDTH / 2 - float(len(bidding_cards_gui) / 2) * (CARD_WIDTH + CARD_OFFSET / 2)
        for card in gui_cards:
            card.left = left
            card.top = BIDDING_LOCATION_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in gui_cards:
            card.image = card.card_back_image if is_covered else card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))
            card.card.is_reversed = is_covered
