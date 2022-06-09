import Settings
from Card import Card
from PlayerRound import PlayerRound

# Klasa przedstawiająca przebieg licytacji


class Bidding:
    __prikup: [Card]                        #musek (3 karty)
    __bid: int                              #max. licytowana stawka
    __players_bidding: [int]                #stawki graczy
    __bidding_player_round: PlayerRound     #gracz, który licytował (domyślnie zaczynający licytacje)
    __last_bidding_player_id: int
    __last_bidding_date: str
    __cards_for_other_players: [Card]

    def __init__(self, init_player):
        self.__prikup = []
        self.__bid = Settings.DEFAULT_BID
        self.__bidding_player_round = init_player
        self.__last_bidding_player_id = init_player.player.id_player
        self.__last_bidding_date = None
        self.__players_bidding = [0, 0, 0]
        self.__cards_for_other_players = [(), ()]
        for i in range(0, 3):
            self.players_bidding[i] = Settings.DEFAULT_BID if i == init_player.player.id_player else 0

    @property
    def cards_for_other_players(self):
        return self.__cards_for_other_players

    @cards_for_other_players.setter
    def cards_for_other_players(self, cards_for_other_players):
        self.__cards_for_other_players = cards_for_other_players

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
        self.bidding_player_round = player_round
        self.last_bidding_player_id = player_round.player.id_player
        self.players_bidding[player_round.player.id_player] = self.bid

    def players_declaration_value(self, player_round, value):
        self.bid = value
        self.bidding_player_round = player_round
        self.last_bidding_player_id = player_round.player.id_player
        self.players_bidding[player_round.player.id_player] = self.bid

    # Sprawdzamy, czy licytacja się zakończyła
    def if_bidding_end(self):
        return self.__players_bidding.count(-1) == 2

    def pass_bid(self, player_round):
        self.__players_bidding[player_round.player.id_player] = -1

    # Metoda kończąca licytację - karty z musku idą do ręki gracza
    def bidding_end(self):
        self.bidding_player_round.declared_points = self.__bid
        for i in range(len(self.prikup) - 1, -1, -1):
            if self.prikup[i] is not None:
                self.bidding_player_round.add_card(self.prikup.pop(i))
        self.bidding_player_round.sort_cards()

    # Do wykorzystania w przyszłości
    def use_bomb(self, players):
        self.__bidding_player_round.player.use_bomb()
        for player in players:
            if player != self.__bidding_player_round.player:
                player.add_points(Settings.POINTS_FROM_BOMB)

    # Metoda wyjmująca daną kartę z ręki
    def pop_card(self, popping_card):
        i_card = 0
        for card in self.bidding_player_round.cards:
            if card.__eq__(popping_card):
                return self.bidding_player_round.cards.pop(i_card)
            i_card += 1
        return None

    # Metoda oddająca po jednej karcie przeciwnikom
    def give_away_cards(self):
        card1, player_round1 = self.__cards_for_other_players[0]
        card2, player_round2 = self.__cards_for_other_players[1]

        player_round1.add_card(card1)
        player_round2.add_card(card2)

        player_round1.sort_cards()
        player_round2.sort_cards()

        self.__cards_for_other_players = [(), ()]


