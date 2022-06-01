from Player import Player
from Round import Round


class Game:
    __id_game: int
    __id_player: int
    __players: [Player] = []
    __rounds: [Round] = []

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

    def add_player_to_game(self, player):
        if len(self.__players) < 3:
            self.__players.append(player)
            return True
        else:
            return False

    def add_round_to_game(self, game_round):
        self.__rounds.append(game_round)

    def check_end(self):
        for player in self.__players:
            if player.points >= 1000:
                return True
        return False
