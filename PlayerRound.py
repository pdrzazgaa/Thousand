from Card import Card
from Database import Database
from Player import Player
from Settings import KING, QUEEN, NINE, DIAMONDS, CLUBS, SPADES, SPADES_POINTS, CLUBS_POINTS, DIAMONDS_POINTS, \
    HEART_POINTS

# Klasa odzwierciedla 'rękę' i sytuację gracza w danej rundzie.
# Znajdują się w niej karty danego gracza, zebrane karty w danej rundzie czy zdobyte punkty


class PlayerRound:
    __player: Player
    __cards: [Card]
    __collected_cards: [Card]
    __points = 0
    __declared_points = 0

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

    # Sprawdzamy, czy na 'ręce' kartę, która jest parą (meldunkiem) do zagrywanej karty
    def check_if_pair(self, card):
        return card.value == QUEEN and Card(card.color, KING) in self.__cards or card.value == KING and \
               Card(card.color, QUEEN) in self.__cards

    # Będą używane w późniejszych etapach rozwoju gry
    # ---------------------------
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

    # -------------------------------

    # wykonanie ruchu przez gracza - wybranie karty i wysłanie informacji do bazy danych
    def make_move(self, chosen_card, initial_move_player_id, id_r, info_label):
        color = chosen_card.card.color
        value = chosen_card.card.value
        if_queen_king_pair = self.check_if_pair(chosen_card.card) and self.player.id_player == initial_move_player_id
        Database.make_move(id_r, self.player.id_player, color, value, if_queen_king_pair, info_label)

    # Metoda pozwalająca zagrać kartę i w przypadku meldunku dopisuje odpowiednią wartość punktową
    # (odpalana po otrzymaniu informacji z bazy danych)
    def play_card(self, desk, id_player, card, if_queen_king_pair, game, info_label):
        try:
            desk[id_player] = self.__cards.pop(self.__cards.index(card))
        except:
            game.reload_last_round(info_label)

        if if_queen_king_pair:
            if card.color == SPADES:
                self.__points += SPADES_POINTS
            elif card.color == CLUBS:
                self.__points += CLUBS_POINTS
            elif card.color == DIAMONDS:
                self.__points += DIAMONDS_POINTS
            else:
                self.__points += HEART_POINTS

    # Metoda sprawdzająca, czy można wykonać ruch po zagraniu innego gracza
    def check_if_can_make_move(self, card, init_card):
        if init_card is not None:
            if card.color == init_card.color:
                return True
            else:
                for c in self.__cards:
                    if c.color == init_card.color:
                        return False
                return True
        return True

    # Metoda sortująca karty w kolejności od największych do najmniejszych (najpierw kolor, potem wartość)
    def sort_cards(self):
        if self is not None:
            self.__cards.sort(key=lambda card: (card.color, card.value), reverse=True)
