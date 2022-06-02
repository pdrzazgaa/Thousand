import Settings
from Card import Card
from Player import Player
from PlayerRound import PlayerRound


class Bidding:
    __prikup: [Card]                        #musek (3 karty)
    __bid: int                              #max. licytowana stawka
    __players_bidding: [int]                #stawki graczy
    __bidding_player_round: PlayerRound     #gracz, który licytował (domyślnie zaczynający licytacje)
    __last_bidding: str

    def __init__(self, init_player_id):
        self.__prikup = []
        self.__bid = Settings.DEFAULT_BID
        self.__bidding_player_round = init_player_id
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
    def players_bidding(self):
        return self.__players_bidding

    @property
    def last_bidding(self):
        return self.__last_bidding

    @last_bidding.setter
    def last_bidding(self, last_bidding):
        self.__last_bidding = last_bidding

    def add_card_to_prikup(self, card):
        self.__prikup.append(card)

    def players_declaration(self, player_round, value):
        if value > self.__bid:
            self.bid = value
            self.__bidding_player_round = player_round
            self.__players_bidding[PlayerRound(player_round).player.id_player] = value
            return True
        else:
            self.__players_bidding[PlayerRound(player_round).player.id_player] = None
            return False

    def bidding_end(self):
        self.__bidding_player_round.declared_points = self.__bid
        for prikup_card in self.__prikup:
            self.__bidding_player_round.add_card(prikup_card)

    def use_bomb(self, players):
        Player(self.__bidding_player_round.player).use_bomb()
        for player in players:
            if player != self.__bidding_player_round.player:
                (Player(player)).add_points(Settings.POINTS_FROM_BOMB)

    def increase_bid(self, value):
        self.__bid += value

    @staticmethod
    def give_away_card(card_player1, card_player2):
        card1, player_round1 = card_player1
        card2, player_round2 = card_player2

        (PlayerRound(player_round1)).add_card(card1)
        (PlayerRound(player_round2)).add_card(card2)


