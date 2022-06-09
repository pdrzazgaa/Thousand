import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Player import Player
from Database import Database
from Desk import Desk
from GUISettings import FONT, FONTSIZE, FONTSIZE_TITLE, START_WINDOWS_WIDTH, START_WINDOWS_HEIGHT
from Game import Game

# Klasa przedstawiająca okno startowe (dołączanie do gry, tworzenie gry)


class StartWindow(tk.Frame):

    __game: Game

    def __init__(self, parent, game):
        super().__init__()
        self.parent = parent
        self.parent.geometry(START_WINDOWS_WIDTH + "x" + START_WINDOWS_HEIGHT + "+500+250")
        self.__game = game
        self.working = self.parent
        self.create_start_window()

    def create_start_window(self):

        def id_text(event):
            entry_id_game.delete(0, END)

        def create_pass_text(event):
            entry_create_password.delete(0, END)

        def pass_text(event):
            entry_password.delete(0, END)

        def join_game_inner():
            self.join_game(entry_id_game.get(), entry_password.get())

        def create_game_inner():
            self.create_game(entry_create_password.get())
            entry_create_password.delete(0, END)

        window = self.working
        self.working.title("Game: 1000")

        label_create_game = tk.Label(window, text="1000", font=(FONT, FONTSIZE_TITLE))
        label_create_game.grid(column=0, row=0)

        label_create_game = tk.Label(window, text="Create a game: ", font=(FONT, FONTSIZE))
        label_create_game.grid(column=0, row=1)
        entry_create_password = tk.Entry(window, width=40, justify=CENTER)
        entry_create_password.insert(0, "Create password")
        entry_create_password.bind("<Button>", create_pass_text)
        entry_create_password.grid(column=0, row=2)
        button_create_game = tk.Button(window, text="Create", command=create_game_inner)
        button_create_game.grid(column=0, row=3)

        label_join_game = tk.Label(window, text="Join a game:", font=(FONT, FONTSIZE))
        label_join_game.grid(column=0, row=4)
        entry_id_game = tk.Entry(window, width=40, justify=CENTER)
        entry_id_game.insert(0, "Enter ID")
        entry_id_game.bind("<Button>", id_text)
        entry_id_game.grid(column=0, row=5)

        entry_password = tk.Entry(window, width=40, justify=CENTER)
        entry_password.insert(0, "Enter password")
        entry_password.bind("<Button>", pass_text)
        entry_password.grid(column=0, row=6)

        button_join_game = tk.Button(window, text="Join", command=join_game_inner)
        button_join_game.grid(column=0, row=7)

        self.working.mainloop()

    @staticmethod
    def create_game(password):
        if password == "Create password" or password == "":
            messagebox.showwarning("Warning", "Enter a new password to game")
        elif len(password) > 20:
            messagebox.showwarning("Warning", "The password is too long (max. 20 signs)")
        else:
            Database.create_game(password)
            id_game = Database.get_game_id()
            if id_game is not None and len(id_game) == 1:
                messagebox.showinfo('Information', "The game has been created. \nGame ID: %i" % id_game[0])

    def join_game(self, id_game, password):
        if id_game == "" or password == "Enter ID":
            messagebox.showwarning("Warning", "Enter game ID")
            return
        if password == "" or password == "Enter password":
            messagebox.showwarning("Warning", "Enter password to game")
            return
        check_game_values = Database.check_game(id_game)
        password_value = Database.check_password(id_game)
        if password_value is not None and password_value != []:
            if password_value[0][0] == password:
                if check_game_values is not None and check_game_values != []:
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
                            messagebox.showinfo("Information", "The game has already been started")
                else:
                    messagebox.showinfo("Information", "The game with ID = %s does not exists" % id_game)
            else:
                messagebox.showinfo("Information", "Incorrect password")
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
        self.working.withdraw()
