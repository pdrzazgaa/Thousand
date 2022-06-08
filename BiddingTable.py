import pygame.event

from Database import Database
from GUISettings import *
from Button import Button


class BiddingTable(pygame.sprite.Sprite):

    def __init__(self, display, game, control_panel, info_label):
        super().__init__()
        self.width = WIDTH_BIDDING_TABLE
        self.height = HEIGHT_BIDDING_TABLE
        self.title = FONT_BIDDING.render("BIDDING", True, (255, 255, 255))
        self.players = [FONT_BIDDING_PLAYERS.render("Player 0", True, (255, 255, 255)),
                        FONT_BIDDING_PLAYERS.render("Player 1", True, (255, 255, 255)),
                        FONT_BIDDING_PLAYERS.render("Player 2", True, (255, 255, 255))]
        self.biddings = []
        self.buttons = []
        self.players[int(game.id_player)] = FONT_BIDDING_PLAYERS.render("Me", True, (255, 255, 255))
        self.hit_box = pygame.Rect(WIDTH / 2 - WIDTH_BIDDING_TABLE / 2, 20, WIDTH_BIDDING_TABLE, HEIGHT_BIDDING_TABLE)
        self.display = display
        self.control_panel = control_panel
        self.info_label = info_label
        self.create_buttons()
        self.game = game

    def render(self):
        pygame.draw.rect(self.display, BIDDING_TABLE_COLOR, self.hit_box)
        self.display_headers()
        self.display_biddings()
        for b in self.buttons:
            b.render(disabled=(self.game.rounds[-1].bidding.if_bidding_end() or
                     self.game.rounds[-1].bidding.current_bidding_player_id != self.game.id_player))

    def display_headers(self):
        id_player = self.game.rounds[-1].bidding.current_bidding_player_id
        for i in range(0, 3):
            if i == self.game.id_player:
                text = "Me"
            else:
                text = "Player %i" % i
            if i == id_player and self.control_panel.hidden_prikup:
                self.players[i] = FONT_BIDDING_PLAYERS.render(text, True, (255, 0, 0))
            else:
                self.players[i] = FONT_BIDDING_PLAYERS.render(text, True, (255, 255, 255))
        self.display.blit(self.title, (WIDTH/2 - self.title.get_width()/2, 40))
        self.display.blit(self.players[0], (WIDTH / 2 - 240, 100))
        self.display.blit(self.players[1], (WIDTH / 2 - 240, 130))
        self.display.blit(self.players[2], (WIDTH / 2 - 240, 160))

    def display_biddings(self):
        bid_player0 = self.game.rounds[-1].bidding.players_bidding[0]
        bid_player1 = self.game.rounds[-1].bidding.players_bidding[1]
        bid_player2 = self.game.rounds[-1].bidding.players_bidding[2]
        self.biddings = [FONT_BIDDING_PLAYERS.render("PASS" if bid_player0 == -1 else str(bid_player0), True,
                                                     (255, 255, 255)),
                         FONT_BIDDING_PLAYERS.render("PASS" if bid_player1 == -1 else str(bid_player1), True,
                                                     (255, 255, 255)),
                         FONT_BIDDING_PLAYERS.render("PASS" if bid_player2 == -1 else str(bid_player2), True,
                                                     (255, 255, 255))]
        self.display.blit(self.biddings[0], (WIDTH / 2 - 100, 100))
        self.display.blit(self.biddings[1], (WIDTH / 2 - 100, 130))
        self.display.blit(self.biddings[2], (WIDTH / 2 - 100, 160))

    def create_buttons(self):
        self.buttons.append(Button(self, (WIDTH / 2 + 175), 120, 150, 30,
                                   FONT_BIDDING_PLAYERS.render("+10", True, (0, 0, 0)), self.increase_bid,
                                   self.display))
        self.buttons.append(Button(self, (WIDTH / 2 + 175), 175, 150, 30,
                                   FONT_BIDDING_PLAYERS.render("Pass", True, (0, 0, 0)), self.pass_bid, self.display))

    def increase_bid(self):
        self.game.rounds[-1].bidding.players_declaration(self.game.rounds[-1].players_rounds[self.game.id_player])
        Database.make_bid(self.game.rounds[-1].id_r, self.game.id_player, self.game.rounds[-1].bidding.bid,
                          self.info_label)

    def pass_bid(self):
        self.game.rounds[-1].bidding.pass_bid(self.game.rounds[-1].players_rounds[self.game.id_player])
        Database.make_bid(self.game.rounds[-1].id_r, self.game.id_player, -1, self.info_label)
