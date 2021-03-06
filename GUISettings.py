import pygame
import sys

# Wszystkie ustawienia i stałe w grze dotyczące wyglądu aplikacji

pygame.font.init()

HEIGHT = 700
WIDTH = 1100
ACC = 0.5
FRIC = -0.12
FPS = 10

# W zależności od systemu operacyjnego okno przybiera różne wielkości
if sys.platform == "win32":
    START_WINDOWS_WIDTH = "320"
    START_WINDOWS_HEIGHT = "350"
elif sys.platform == "darwin":
    START_WINDOWS_WIDTH = "370"
    START_WINDOWS_HEIGHT = "320"
else:
    START_WINDOWS_WIDTH = "320"
    START_WINDOWS_HEIGHT = "320"


FONT = "Helvetica"
FONTSIZE = "15"
FONTSIZE_TITLE = "100"
BACKGROUND_COLOR = (0, 74, 0)

# Przyciski
BUTTON_COLOR_CLICKED = (150, 150, 150)
BUTTON_COLOR_DISTURBED = (210, 210, 210)
BUTTON_COLOR_ENABLED = (255, 255, 255)

# Oczekiwanie na graczy
FONT_WAITING = pygame.font.SysFont('Helvetica', 60)
FONT_BUTTON = pygame.font.SysFont('Helvetica', 40)
FONT_BUTTON_SMALL = pygame.font.SysFont('Helvetica', 30)
FONT_CURRENT_PLAYERS = pygame.font.SysFont('Helvetica', 40)
FONT_POINTS_GAME = pygame.font.SysFont('Helvetica', 30)

# Licytacje
WIDTH_BIDDING_TABLE = 600
HEIGHT_BIDDING_TABLE = 200
BIDDING_TABLE_COLOR = (222, 184, 135)
FONT_BIDDING = pygame.font.SysFont('Helvetica', 30, True)
FONT_BIDDING_PLAYERS = pygame.font.SysFont('Helvetica', 20)
FONT_INFO_AFTER_BIDDING = pygame.font.SysFont('Helvetica', 40)

# Rozdawanie kart
LEFT_CARD_POSITION = ()
RIGHT_CARD_POSITION = ()

# Karty
CARD_WIDTH = 150
CARD_HEIGHT = 216

OPPONENT_CARD_LOCATION_LEFT = - CARD_WIDTH/2
OPPONENT_CARD_LOCATION_RIGHT = WIDTH - CARD_WIDTH/2
BIDDING_LOCATION_TOP = 240
CARD_LOCATION_TOP = 550
CARD_OFFSET_TOP = 50
CARD_OFFSET = -75

PIVOT_LEFT_CARDS = 90
PIVOT_RIGHT_CARDS = -90
OPPONENT_CARD_OFFSET = -100

# Gra
COLOR_WHITE = 255, 255, 255
COLOR_ORANGE = 255, 204, 0

# Okienko informacyjne
INFO_BACKGROUND_COLOR = 0, 0, 0, 200
INFO_TEXT_COLOR = 255, 255, 255
INFO_WIDTH = 500
INFO_HEIGHT = 80
INFO_TOP = 0
INFO_LEFT = WIDTH/2 - INFO_WIDTH/2
FONT_INFO = pygame.font.SysFont('Helvetica', 30)


# Tabela punktów
TABLE_WIDTH = 550
TABLE_HEIGHT = 600
POINTS_TABLE_COLOR = (222, 184, 135)
FONT_POINTS = pygame.font.SysFont('Helvetica', 16)
POINT_OFFSET_HEIGHT = 16

# Koniec gry
FONT_ENDING = pygame.font.SysFont('Helvetica', 120, bold=True)

# Czasy dostępu do bazy
TIME_CHECKING_PLAYERS = 3
TIME_CHECKING_DEALINGS = 4
TIME_CHECKING_BIDDINGS = 2
TIME_CHECKING_MOVES = 2
TIME_CHECKING_BUGS = 4
