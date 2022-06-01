from Game import *
from Database import Database
import tkinter as tk
import pygame

if __name__ == '__main__':

    game = Game(-1)
    Database.create_tables()
    start_window = GameGUI(tk.Tk(), game)
    # desk = Desk()
