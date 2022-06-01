import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Player import Player
from Round import Round
from Database import Database
from GUIGame import Desk
from GUISettings import FONT, FONTSIZE, FONTSIZE_TITLE, START_WINDOWS_WIDTH, START_WINDOWS_HEIGHT


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


class GameGUI(tk.Frame):

    __game: Game

    def __init__(self, parent, game):
        super().__init__()
        self.parent = parent
        self.parent.geometry(START_WINDOWS_WIDTH + "x" + START_WINDOWS_HEIGHT)
        self.__game = game
        self.robocze = self.parent
        self.create_start_window()

    def create_start_window(self):
        window = self.robocze
        self.robocze.title("Game: 1000")

        label_create_game = tk.Label(window, text="1000", font=(FONT, FONTSIZE_TITLE))
        label_create_game.grid(column=0, row=0)

        label_create_game = tk.Label(window, text="Create a game: ", font=(FONT, FONTSIZE))
        label_create_game.grid(column=0, row=1)
        button_create_game = tk.Button(window, text="Create", command=GameGUI.create_game)
        button_create_game.grid(column=0, row=2)

        label_join_game = tk.Label(window, text="Join a game:", font=(FONT, FONTSIZE))
        label_join_game.grid(column=0, row=3)
        entry_join_game = tk.Entry(window, width=40, justify=CENTER)
        entry_join_game.grid(column=0, row=4)

        def join_game_inner():
            self.join_game(entry_join_game.get())

        button_join_game = tk.Button(window, text="Join", command=join_game_inner)
        button_join_game.grid(column=0, row=5)

        self.robocze.mainloop()

    @staticmethod
    def create_game():
        Database.create_game()
        id_game = Database.get_game_id()
        if id_game is not None and len(id_game) == 1:
            messagebox.showinfo('Information', "The game has been created. \nGame ID: %i" % id_game[0])
        else:
            messagebox.showerror('Error', "An error has occurred. The game cannot be created.")

    def join_game(self, id_game):
        if id_game == "":
            messagebox.showwarning("Warning", "Enter game ID")
            return
        check_game_values = Database.check_game(id_game)
        if len(check_game_values) != 0:
            players, rounds = check_game_values[0]
            if rounds == 0:
                if players < 3:
                    Database.join_game(id_game)
                    self.close_start_window()
                    self.start_game(id_game, players)
                else:
                    messagebox.showinfo("Information", "The game is full")
            else:
                messagebox.showinfo("Information", "The game has alredy been started")
        else:
            messagebox.showinfo("Information", "The game with ID = %s does not exists" % id_game)

    def start_game(self, id_game, id_player):
        self.__game.id_game = id_game
        for i in range(0, id_player):
            self.__game.add_player_to_game(Player(i))
        self.__game.add_player_to_game(Player(id_player))
        self.__game.id_player = id_player
        desk = Desk(self.__game)

    def close_start_window(self):
        self.robocze.withdraw()
