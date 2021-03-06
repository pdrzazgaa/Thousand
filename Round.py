from Bidding import Bidding
from Card import Card
import random

from PlayerRound import PlayerRound
from Database import Database
from Settings import ACE, NINE, HEART, SPADES

# Klasa odzwierciedlająca rundę
# Runda posiada między innymi 3 rundy graczy (PlayerRound), licytację, stół (wyłożone karty przez graczy),
# kolor atutu (po meldunku), ostatni wykonany ruch (czas)


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

    # Sprawdzamy ile kart pozostało w rundzie
    def count_cards_in_round(self):
        counter = 0
        for i in range(0, len(self.__players_rounds)):
            counter += len(self.__players_rounds[i].cards)
        counter += len([card for card in self.__desk if card is not None])
        return counter

    # Zakończenie ruchu
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

    # Użycie bomby - do użycia w przyszłych wersjach
    def used_bomb(self, player_id, game):
        for pr in self.players_rounds:
            if pr.player.id_player != player_id:
                pr.player.add_points(60)
            game.points_table[pr.player.id_player].append(pr.player.points)
        self.players_rounds[player_id].player.use_bomb()

    # Sprawdzenie, czy koniec rundy (Gracze nie mają już kart)
    def check_if_end_round(self):
        return len(self.__players_rounds[0].cards) == 0 and \
               len(self.__players_rounds[1].cards) == 0 and \
               len(self.__players_rounds[2].cards) == 0

    # Metoda kończąca rundę - zlicza punkty i przypisuje je odpowiednim graczom
    def end_round(self, game):
        for pr in self.__players_rounds:
            if self.bidding.bidding_player_round == pr:
                # Gracz, który licytował
                if self.bidding.bid <= pr.points:
                    pr.player.add_points(self.bidding.bid)
                else:
                    pr.player.add_points(-self.bidding.bid)
            else:
                # Pozostali gracze
                if pr.points % 10 > 5:
                    pr.player.add_points(pr.points + (10-pr.points % 10))
                else:
                    pr.player.add_points(pr.points - pr.points % 10)
            game.points_table[pr.player.id_player].append(pr.player.points)

    # Mieszanie kart
    @staticmethod
    def shuffle_cards():
        cards = []
        for color in range(SPADES, HEART + 1):
            for value in range(NINE, ACE + 1):
                cards.append(Card(color, value))
        random.shuffle(cards)
        return cards

    # Rozdawanie kart
    def deal_cards(self):
        cards = self.shuffle_cards()
        for i_card in range(0, len(cards) - 3):
            id_player = (self.__dealing_player_id + i_card + 1) % 3
            self.__players_rounds[id_player].add_card(cards[i_card])
        for i_card in range(len(cards) - 3, len(cards)):
            self.__bidding.add_card_to_prikup(cards[i_card])

    # Wysłanie rozdania do bazy danych
    def send_dealing_to_database(self, game_id, info_label, round_id=None, if_bomb=False, if_again_dealing=False):
        dealing_player = self.dealing_player_id
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
            Database.deal_cards(str(game_id), str(dealing_player),
                                p01, p02, p03, p04, p05, p06, p07, p08,
                                p11, p12, p13, p14, p15, p16, p17, p18,
                                p21, p22, p23, p24, p25, p26, p27, p28,
                                pc1, pc2, pc3, info_label)
        else:
            Database.update_dealing(str(round_id), p01, p02, p03, p04, p05, p06, p07, p08,
                                    p11, p12, p13, p14, p15, p16, p17, p18,
                                    p21, p22, p23, p24, p25, p26, p27, p28,
                                    sql_if_bomb, sql_if_again_dealing, info_label)
