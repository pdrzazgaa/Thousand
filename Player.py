import Settings


class Player:

    __id_player = 0
    __points = 0
    __bombs = Settings.BOMBS

    def __init__(self, id_player):
        self.__id_player = id_player
        self.__points = 0
        self.__bombs = Settings.BOMBS

    @property
    def id_player(self):
        return self.__id_player

    @property
    def points(self):
        return self.__points

    def add_points(self, points):
        self.__points += points

    def use_bomb(self):
        self.__bombs -= 1

    def has_bombs(self):
        return self.__bombs > 0

    def __eq__(self, other):
        return self.__id_player == (Player(other)).__id_player


class PlayerGUI:
    ...

