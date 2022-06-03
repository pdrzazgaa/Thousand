import Settings
from Card import Card
from Player import Player
from PlayerRound import PlayerRound


class Bidding:
    __prikup: [Card]                        #musek (3 karty)
    __bid: int                              #max. licytowana stawka
    __players_bidding: [int]                #stawki graczy
    __bidding_player_round: PlayerRound     #gracz, który licytował (domyślnie zaczynający licytacje)
    __last_bidding_player_id: int
    __last_bidding_date: str

    def __init__(self, init_player_id):
        self.__prikup = []
        self.__bid = Settings.DEFAULT_BID
        self.__bidding_player_round = init_player_id
        self.__last_bidding_player_id = init_player_id
        self.__last_bidding_date = None
        self.__players_bidding = [0, 0, 0]
        for i in range(0, 3):
            self.players_bidding[i] = Settings.DEFAULT_BID if i == init_player_id else 0

    @property
    def prikup(self):
        return self.__prikup

    @prikup.setter
    def prikup(self, prikup):
        self.__prikup = prikup

    @property
    def bid(self):
        return self.__bid

    @bid.setter
    def bid(self, i_bid):
        if i_bid > self.__bid:
            self.__bid = i_bid

    @property
    def last_bidding_player_id(self):
        return self.__last_bidding_player_id

    @last_bidding_player_id.setter
    def last_bidding_player_id(self, last_bidding_player_id):
        if last_bidding_player_id > self.__last_bidding_player_id:
            self.__last_bidding_player_id = last_bidding_player_id

    @property
    def current_bidding_player_id(self):
        current_player_id = (self.__last_bidding_player_id + 1) % 3
        return current_player_id if self.players_bidding[current_player_id] != -1 else (current_player_id + 1) % 3

    @property
    def players_bidding(self):
        return self.__players_bidding

    @property
    def bidding_player_round(self):
        return self.__bidding_player_round

    @bidding_player_round.setter
    def bidding_player_round(self, bidding_player_round):
        self.__bidding_player_round = bidding_player_round

    @property
    def last_bidding_date(self):
        return self.__last_bidding_date

    @last_bidding_date.setter
    def last_bidding_date(self, last_bidding):
        self.__last_bidding_date = last_bidding

    def add_card_to_prikup(self, card):
        self.__prikup.append(card)

    def players_declaration(self, player_round):
        self.bid += Settings.INCREASE_OF_BIDDING
        self.__bidding_player_round = player_round
        self.__last_bidding_player_id = player_round.player.id_player
        self.__players_bidding[player_round.player.id_player] = self.bid

    def players_declaration_value(self, player_round, value):
        self.bid = value
        self.__bidding_player_round = player_round
        self.__last_bidding_player_id = player_round.player.id_player
        self.__players_bidding[player_round.player.id_player] = self.bid

    def if_bidding_end(self):
        return self.__players_bidding.count(-1) == 2

    def pass_bid(self, player_round):
        self.__players_bidding[player_round.player.id_player] = -1

    def bidding_end(self):
        self.__bidding_player_round.declared_points = self.__bid
        for i in range(len(self.__prikup)-1, -1, -1):
            if self.__prikup[i] is not None:
                self.__bidding_player_round.add_card(self.__prikup.pop(i))

    def use_bomb(self, players):
        self.__bidding_player_round.player.use_bomb()
        for player in players:
            if player != self.__bidding_player_round.player:
                player.add_points(Settings.POINTS_FROM_BOMB)

    @staticmethod
    def give_away_card(card_player1, card_player2):
        card1, player_round1 = card_player1
        card2, player_round2 = card_player2

        (PlayerRound(player_round1)).add_card(card1)
        (PlayerRound(player_round2)).add_card(card2)


