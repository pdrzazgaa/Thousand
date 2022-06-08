class Card:
    points = {1: 0, 2: 2, 3: 3, 4: 4, 5: 10, 6: 11}

    __color: int
    __value: int
    __is_showed = False
    __is_reversed = False

    def __init__(self, color, value):
        self.__color = color
        self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def color(self):
        return self.__color

    @property
    def is_reversed(self):
        return self.__is_reversed

    @is_reversed.setter
    def is_reversed(self, is_reversed):
        self.__is_reversed = is_reversed

    def card_to_sql(self):
        return str(self.color) + str(self.value)

    @staticmethod
    def card_from_sql(card_sql):
        return Card(int(card_sql / 10), (card_sql % 10)) if card_sql is not None else None

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.__color == other.__color and self.__value == other.value
        elif self is None and other is None:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.value + self.color)
