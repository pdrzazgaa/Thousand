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
    __atut: int  # wiodący kolor
    __last_round: str
    __last_move: str
    __dealing_player_id: int
    __id_r: int
    __last_move_player_id: int
    __initial_move_player_id: int

    def __init__(self, players_rounds, dealing_player_id):
        self.__players_rounds = players_rounds
        self.__bidding = Bidding(players_rounds[(dealing_player_id + 1) % 3])
        self.__desk = [None, None, None]
        self.__dealing_player_id = dealing_player_id
        self.__id_r = 0
        self.__last_move_player_id = -1
        self.__last_round = ""
        self.__last_move = ""
        self.__initial_move_player_id = -1
        self.__atut = -1

    @property
    def bidding(self):
        return self.__bidding

    @property
    def desk(self):
        return self.__desk

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
    def last_move(self):
        return self.__last_move

    @last_move.setter
    def last_move(self, last_move):
        self.__last_move = last_move

    @property
    def atut(self):
        return self.__atut

    @atut.setter
    def atut(self, atut):
        self.__atut = atut

    @property
    def dealing_player_id(self):
        return self.__dealing_player_id

    @property
    def last_move_player_id(self):
        return self.__last_move_player_id

    @last_move_player_id.setter
    def last_move_player_id(self, last_move_player_id):
        self.__last_move_player_id = last_move_player_id

    @property
    def current_id_player(self):
        if self.__last_move_player_id == -1:
            return self.bidding.last_bidding_player_id
        else:
            if self.__desk.count(None) != 3:
                return (self.__last_move_player_id + 1) % 3
            else:
                return self.initial_move_player_id

    @property
    def initial_move_player_id(self):
        if self.__initial_move_player_id == -1:
            return self.bidding.last_bidding_player_id
        else:
            return self.__initial_move_player_id

    def end_move(self):
        if None not in self.__desk:
            strongest_player_index = self.__initial_move_player_id
            # Był wcześniej lub teraz meldunek
            atut_cards_on_desk = [card for card in self.__desk if card.color == self.__atut]
            if self.__atut != -1 and len(atut_cards_on_desk) != 0:
                for i in range(0, len(self.__desk)):
                    card = self.__desk[i]
                    if card.color == self.__atut:
                        if self.__desk[strongest_player_index].color != self.__atut:
                            strongest_player_index = i
                        else:
                            if card.value > self.__desk[strongest_player_index].value:
                                strongest_player_index = i
            else:
                # Nie było meldunku lub nie położono żadnych takich kart
                for i in range(0, len(self.__desk)):
                    card = self.__desk[i]
                    if card.color == self.__desk[strongest_player_index].color and \
                            card.value > self.__desk[strongest_player_index].value:
                        strongest_player_index = i
            # Oddanie graczowi kart
            self.players_rounds[strongest_player_index].take_cards(self.__desk)
            self.__desk = [None, None, None]
            self.__initial_move_player_id = strongest_player_index
        else:
            pass

    def used_bomb(self, player_id):
        for pr in self.players_rounds:
            if pr.player.id_player != player_id:
                pr.player.add_points(60)
        self.players_rounds[player_id].player.use_bomb()

    def check_if_end_round(self):
        return len(self.__players_rounds[0].cards) == 0 and \
               len(self.__players_rounds[1].cards) == 0 and \
               len(self.__players_rounds[2].cards) == 0

    def end_round(self, game):
        for pr in self.__players_rounds:
            if self.bidding.bidding_player_round == pr:
                # Gracz, który licytował
                if self.bidding.bid <= pr.points:
                    pr.player.add_points(self.bidding.bid)
                else:
                    pr.player.add_points(self.bidding.bid)
            else:
                # Pozostali gracze
                if pr.points % 10 > 5:
                    pr.player.add_points(pr.points + pr.points % 10)
                else:
                    pr.player.add_points(pr.points - pr.points % 10)
            game.points_table[pr.player.id_player].append(pr.player.points)

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

    def send_dealing_to_database(self, game_id, round_id=None, if_bomb=False, if_again_dealing=False):
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
        sql_if_bomb = "1" if if_bomb else "null"
        sql_if_again_dealing = "1" if if_again_dealing else "null"
        if round_id is None:
            Database.deal_cards(str(game_id), p01, p02, p03, p04, p05, p06, p07, p08,
                                p11, p12, p13, p14, p15, p16, p17, p18,
                                p21, p22, p23, p24, p25, p26, p27, p28,
                                pc1, pc2, pc3)
        else:
            Database.update_dealing(str(round_id), p01, p02, p03, p04, p05, p06, p07, p08,
                                    p11, p12, p13, p14, p15, p16, p17, p18,
                                    p21, p22, p23, p24, p25, p26, p27, p28,
                                    sql_if_bomb, sql_if_again_dealing)


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
    def create_cards_desk(cards, all_sprites):
        all_cards = [None, None, None]
        for i in range(0, len(cards)):
            if cards[i] is not None:
                gui_card = CardGUI(cards[i])
                all_cards[i] = gui_card
                all_sprites.add(gui_card)
        return all_cards

    @staticmethod
    def display_player_cards(player_cards_gui):
        left = WIDTH / 2 - (((len(player_cards_gui) - 1) * (CARD_WIDTH + CARD_OFFSET) + CARD_WIDTH) / 2)
        for card in player_cards_gui:
            card.card.is_reversed = False
            card.left = left
            card.top = CARD_LOCATION_TOP if not card.is_clicked else CARD_LOCATION_TOP - CARD_OFFSET_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in player_cards_gui:
            card.image = card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_oponent_cards(oponent_cards_gui, left: bool):
        top = HEIGHT / 2 - float(len(oponent_cards_gui) / 2) * (CARD_WIDTH / 2)
        for card in oponent_cards_gui:
            card.card.is_reversed = True
            card.top = top
            if left:
                card.left = OPPONENT_CARD_LOCATION_LEFT
            else:
                card.left = OPPONENT_CARD_LOCATION_RIGHT
            top += CARD_WIDTH + OPPONENT_CARD_OFFSET
        for card in oponent_cards_gui:
            card.image = card.card_back_image
            if left:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_LEFT_CARDS)
            else:
                card.image = pygame.transform.rotate(card.image, angle=PIVOT_RIGHT_CARDS)
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))

    @staticmethod
    def display_bidding_cards(bidding_cards_gui, is_covered):
        left = WIDTH / 2 - float(len(bidding_cards_gui) / 2) * (CARD_WIDTH + CARD_OFFSET / 2)
        for card in bidding_cards_gui:
            card.left = left
            card.top = BIDDING_LOCATION_TOP
            left += CARD_WIDTH + CARD_OFFSET
        for card in bidding_cards_gui:
            card.image = card.card_back_image if is_covered else card.card_image
            card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top + CARD_HEIGHT / 2))
            card.card.is_reversed = is_covered

    @staticmethod
    def display_desk(desk_cards_gui: [CardGUI], self_player_id, starting_id_player):

        # gui_desk_cards = [None, None, None]

        try:
            card_gui_me = desk_cards_gui[self_player_id]
        except:
            card_gui_me = None

        try:
            card_gui_op1 = desk_cards_gui[(self_player_id + 1) % 3]
        except:
            card_gui_op1 = None
        try:
            card_gui_op2 = desk_cards_gui[(self_player_id + 2) % 3]
        except:
            card_gui_op2 = None

        # try:
        #     # gui_desk_cards[starting_id_player] = desk_cards_gui[0]
        #     # gui_desk_cards[(starting_id_player + 1) % 3] = desk_cards_gui[1]
        #     # gui_desk_cards[(starting_id_player + 2) % 3] = desk_cards_gui[2]
        # except:
        #     ...


        top_op = 130
        top_me = 260
        left_op1 = WIDTH / 2 - 1.5 * CARD_WIDTH - 5
        left_op2 = WIDTH / 2 + 0.5 * CARD_WIDTH + 5
        left_me = WIDTH / 2 - CARD_WIDTH / 2

        if card_gui_me is not None:
            RoundGUI.display_desk_card(card_gui_me, left_me, top_me)

        if card_gui_op1 is not None:
            RoundGUI.display_desk_card(card_gui_op1, left_op1, top_op)

        if card_gui_op2 is not None:
            RoundGUI.display_desk_card(card_gui_op2, left_op2, top_op)

    @staticmethod
    def display_desk_card(card, left, top):
        card.left = left
        card.top = top
        card.image = card.card_image
        card.rect = card.image.get_rect(center=(card.left + CARD_WIDTH / 2, card.top +
                                                CARD_HEIGHT / 2))
        card.card.is_reversed = False
