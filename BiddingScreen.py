import sys
import pygame.event

from Card import CardGUI
from Database import Database
from GUISettings import *
from Round import RoundGUI
from Game import Game
from Button import Button


class BiddingScreen:
    display: pygame.display
    all_sprites: pygame.sprite.Group()
    event_list: []
    game: Game
    cards: [CardGUI]

    def __init__(self, game, display, control_panel):
        self.game = game
        self.display = display
        self.control_panel = control_panel
        self.all_sprites = pygame.sprite.Group()
        self.bidding_table = BiddingTable(display, game, control_panel)
        self.cards = []
        self.is_dealt = False
        self.is_redealt = False

    def main(self):
        if not self.is_dealt:
            self.cards = self.create_cards()
            self.is_dealt = True
        self.manage_display()
        self.handle_clicks()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.control_panel.bidding_phase and \
                            self.game.rounds[-1].bidding.current_bidding_player_id == self.game.id_player:
                        for button in self.bidding_table.buttons:
                            button.do_sth()

    def manage_display(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display_cards(self.control_panel.hidden_prikup)
        self.bidding_table.render()
        pygame.display.update()

    def create_cards(self):
        player_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds[self.game.id_player].cards,
                                                     self.all_sprites)
        oponent1_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 1) % 3].cards, self.all_sprites)
        oponent2_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].players_rounds
                                                       [(self.game.id_player + 2) % 3].cards, self.all_sprites)
        prikup_cards_gui = RoundGUI.create_cards_gui(self.game.rounds[-1].bidding.prikup, self.all_sprites)

        return player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui

    def display_cards(self, hidden_bidding):
        player_cards_gui, oponent1_cards_gui, oponent2_cards_gui, prikup_cards_gui = self.cards
        # rozkładamy karty
        RoundGUI.display_player_cards(player_cards_gui)
        RoundGUI.display_bidding_cards(prikup_cards_gui, hidden_bidding)

        # przeciwnik 1
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 1) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (30, 30))
        RoundGUI.display_oponent_cards(oponent1_cards_gui, True)

        # przeciwnik 2
        message_waiting = FONT_INFO_AFTER_BIDDING.render("P%i" % ((self.game.id_player + 2) % 3), True, (255, 255, 255),
                                                         BACKGROUND_COLOR)
        self.display.blit(message_waiting, (WIDTH - 80, 30))
        RoundGUI.display_oponent_cards(oponent2_cards_gui, False)

        self.all_sprites.draw(self.display)

    def quit(self):
        Database.leave_game(self.game.id_game)
        for timer in self.control_panel.timers:
            timer.cancel()
        pygame.quit()
        sys.exit()


class BiddingTable(pygame.sprite.Sprite):

    # base = pygame.image.load("textures\\bidding_table.xcf")

    def __init__(self, display, game, control_panel):
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
        self.create_buttons()
        self.game = game

    def render(self):
        pygame.draw.rect(self.display, BIDDING_TABLE_COLOR, self.hit_box)
        id_player = self.game.rounds[-1].bidding.current_bidding_player_id
        for i in range(0, 3):
            text = "Player %i" % i
            if i == self.game.id_player:
                text = "Me"
            if i == id_player:
                self.players[i] = FONT_BIDDING_PLAYERS.render(text, True, (255, 0, 0))
            else:
                self.players[i] = FONT_BIDDING_PLAYERS.render(text, True, (255, 255, 255))
        self.display.blit(self.title, (WIDTH / 2 - 70, 40))
        self.display.blit(self.players[0], (WIDTH / 2 - 240, 100))
        self.display.blit(self.players[1], (WIDTH / 2 - 240, 130))
        self.display.blit(self.players[2], (WIDTH / 2 - 240, 160))
        self.display_biddings()
        for b in self.buttons:
            b.render(self.control_panel.bidding_phase and
                     self.game.rounds[-1].bidding.current_bidding_player_id != self.game.id_player)

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

    def create_buttons(self):
        self.buttons.append(Button(self, (WIDTH / 2 + 175), 120, 150, 30,
                                   FONT_BIDDING_PLAYERS.render("+10", True, (0, 0, 0)), self.increase_bid,
                                   self.display))
        self.buttons.append(Button(self, (WIDTH / 2 + 175), 175, 150, 30,
                                   FONT_BIDDING_PLAYERS.render("Pass", True, (0, 0, 0)), self.pass_bid, self.display))

    def increase_bid(self):
        self.game.rounds[-1].bidding.players_declaration(self.game.rounds[-1].players_rounds[self.game.id_player])
        Database.make_bid(self.game.rounds[-1].id_r, self.game.id_player, self.game.rounds[-1].bidding.bid)

    def pass_bid(self):
        self.game.rounds[-1].bidding.pass_bid(self.game.rounds[-1].players_rounds[self.game.id_player])
        Database.make_bid(self.game.rounds[-1].id_r, self.game.id_player, -1)
