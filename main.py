from Game import Game
from Database import Database
import tkinter as tk
from StartWindow import StartWindow

# plik main odpalający grę
# tworzymy w nim krę, tworzymy tabele w bazie danych oraz odpalamy okienko dołączania do gry


if __name__ == '__main__':

    game = Game(-1)
    Database.create_tables()
    start_window = StartWindow(tk.Tk(), game)
