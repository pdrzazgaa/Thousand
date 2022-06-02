import sys
import pygame.event
from Database import Database
from GUISettings import *
from Round import RoundGUI
from Game import Game


class BiddingScreen:
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    game: Game

    def __init__(self, game, display, control_panel):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.bidding_table = BiddingTable(display, game)

    def main(self):
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_cards(self.control_panel.end_bidding_phase, self.create_cards())
        self.bidding_table.render()
        pygame.display.update()

    def create_cards(self):
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[0].cards, self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[1].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[2].cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].bidding.prikup, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui

    def display_cards(self, hidden_bidding, cards):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui = cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)
        RoundGUI.display_oponent_cards(oponent1_cards_gui, (self.game.id_player + 1) % 3)
        RoundGUI.display_oponent_cards(oponent2_cards_gui, (self.game.id_player + 2) % 3)

        self.all_sprites.draw(self.display)
        pygame.display.update()

    def quit(self):
        Database.leave_game(self.game.id_game)
        pygame.quit()
        sys.exit()


class BiddingTable:

    # base = pygame.image.load("textures\\bidding_table.xcf")

    def __init__(self, display, game):
        self.width = WIDTH_BIDDING_TABLE
        self.height = HEIGHT_BIDDING_TABLE
        self.title = FONT_BIDDING.render("BIDDING", True, (255, 255, 255))
        self.players = [FONT_BIDDING_PLAYERS.render("Player 0", True, (255, 255, 255)),
                        FONT_BIDDING_PLAYERS.render("Player 1", True, (255, 255, 255)),
                        FONT_BIDDING_PLAYERS.render("Player 2", True, (255, 255, 255))]
        self.biddings = []
        self.players[int(game.id_player)] = FONT_BIDDING_PLAYERS.render("Me", True, (255, 255, 255))
        self.hit_box = pygame.Rect(WIDTH / 2 - WIDTH_BIDDING_TABLE / 2, 20, WIDTH_BIDDING_TABLE, HEIGHT_BIDDING_TABLE)
        self.display = display
        self.game = game

    def render(self):
        pygame.draw.rect(self.display, BIDDING_TABLE_COLOR, self.hit_box)
        self.display.blit(self.title, (WIDTH / 2 - 70, 40))
        self.display.blit(self.players[0], (WIDTH / 2 - 240, 100))
        self.display.blit(self.players[1], (WIDTH / 2 - 240, 130))
        self.display.blit(self.players[2], (WIDTH / 2 - 240, 160))
        self.display_biddings()

    def display_biddings(self):
        bid_player0 = self.game.rounds[-1].bidding.players_bidding[0]
        bid_player1 = self.game.rounds[-1].bidding.players_bidding[1]
        bid_player2 = self.game.rounds[-1].bidding.players_bidding[2]
        self.biddings = [FONT_BIDDING_PLAYERS.render(str(bid_player0), True, (255, 255, 255)),
                         FONT_BIDDING_PLAYERS.render(str(bid_player1), True, (255, 255, 255)),
                         FONT_BIDDING_PLAYERS.render(str(bid_player2), True, (255, 255, 255))]
        self.display.blit(self.biddings[0], (WIDTH / 2 - 100, 100))
        self.display.blit(self.biddings[1], (WIDTH / 2 - 100, 130))
        self.display.blit(self.biddings[2], (WIDTH / 2 - 100, 160))
