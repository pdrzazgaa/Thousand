import pygame

pygame.font.init()

HEIGHT = 700
WIDTH = 1100
ACC = 0.5
FRIC = -0.12
FPS = 10

START_WINDOWS_WIDTH = "370"
START_WINDOWS_HEIGHT = "270"

FONT = "Helvetica"
FONTSIZE = "15"
FONTSIZE_TITLE = "100"
BACKGROUND_COLOR = (0, 74, 0)

# Oczekiwanie na graczy
FONT_WAITING = pygame.font.SysFont('Helvetica', 60)
FONT_BUTTON = pygame.font.SysFont('Helvetica', 40)
FONT_CURRENT_PLAYERS = pygame.font.SysFont('Helvetica', 40)

# Licytacje
WIDTH_BIDDING_TABLE = 600
HEIGHT_BIDDING_TABLE = 200
BIDDING_TABLE_COLOR = (222, 184, 135)
FONT_BIDDING = pygame.font.SysFont('Helvetica', 30, True)
FONT_BIDDING_PLAYERS = pygame.font.SysFont('Helvetica', 20)
FONT_INFO_AFTER_BIDDING = pygame.font.SysFont('Helvetica', 40)

#Rozdawanie kart
LEFT_CARD_POSITION = ()
RIGHT_CARD_POSITION = ()

# Karty
CARD_WIDTH = 150
CARD_HEIGHT = 216

OPPONENT_CARD_LOCATION_LEFT = -84
OPPONENT_CARD_LOCATION_RIGHT = 1050
BIDDING_LOCATION_TOP = 240
CARD_LOCATION_TOP = 550
CARD_OFFSET_TOP = 50
CARD_OFFSET = -75

PIVOT_LEFT_CARDS = 90
PIVOT_RIGHT_CARDS = -90
OPPONENT_CARD_OFFSET = -100

TABLE_WIDTH = 300
TABLE_HEIGHT = 400

# Czasy dostępu do bazy
TIME_CHECKING_PLAYERS = 3
TIME_CHECKING_DEALINGS = 4
TIME_CHECKING_BIDDINGS = 2
TIME_CHECKING_MOVES = 2
