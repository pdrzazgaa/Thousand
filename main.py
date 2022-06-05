from Game import Game
from Database import Database
import tkinter as tk
from StartWindow import StartWindow

if __name__ == '__main__':

    game = Game(-1)
    Database.create_tables()
    start_window = StartWindow(tk.Tk(), game)
