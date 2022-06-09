from LoadRound import LoadRound
from Player import Player
from PlayerRound import PlayerRound
from Round import Round
from Settings import END_GAME

# Klasa przedstawiająca stan gry


class Game:
    __id_game: int
    __id_player: int
    __players: [Player] = []
    __rounds: [Round] = []
    __points_table = [[0], [0], [0]]

    def __init__(self, id_game):
        self.__id_game = id_game
        for i in range(0, 3):
            self.add_player_to_game(Player(i))

    @property
    def id_game(self):
        return self.__id_game

    @property
    def rounds(self):
        return self.__rounds

    @id_game.setter
    def id_game(self, id_game):
        self.__id_game = id_game

    @property
    def id_player(self):
        return self.__id_player

    @id_player.setter
    def id_player(self, id_player):
        self.__id_player = id_player

    @property
    def players(self):
        return self.__players

    @property
    def points_table(self):
        return self.__points_table

    def player_me(self):
        return self.players[self.id_player]

    def add_player_to_game(self, player):
        if len(self.__players) < 3:
            self.__players.append(player)
            return True
        else:
            return False

    # Odświeżenie rundy
    def reload_last_round(self, info_label):
        reloaded_round = LoadRound(self, self.rounds[-1].id_r, info_label)
        self.rounds[-1] = reloaded_round.round
        info_label.show_label("The round has been reloaded")

    def add_round_to_game(self):
        # Tworzymy rundy graczy
        player0_round = PlayerRound(self.players[0])
        player1_round = PlayerRound(self.players[1])
        player2_round = PlayerRound(self.players[2])
        # Jeżeli jesteśmy graczem tasującym, to tworzymy karty i wysyłamy je do bazy
        dealing_player = 0 if len(self.rounds) == 0 else (self.rounds[-1].dealing_player_id + 1) % 3
        self.__rounds.append(Round([player0_round, player1_round, player2_round], dealing_player))

    def check_end(self):
        for player in self.__players:
            if player.points >= END_GAME:
                return True
        return False
