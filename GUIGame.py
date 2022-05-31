import sys
import pygame

from Database import Database
from PlayerRound import PlayerRound
from pygame.locals import *
from GUISettings import *
from Round import RoundGUI, Round


class Desk:

    display_surface: pygame.display

    def __init__(self, game):
        pygame.init()
        vec = pygame.math.Vector2  # 2 for two dimensional
        FramePerSec = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("1000")
        all_sprites = pygame.sprite.Group()

        # TESTOWANIE
        for i in range(0, 3):
            if game.players[i] is not None:
                game.add_player_to_game(i)

        player_round0_1 = PlayerRound(game.players[0])
        player_round1_1 = PlayerRound(game.players[1])
        player_round2_1 = PlayerRound(game.players[2])
        roundgui = RoundGUI()

        round1 = Round([player_round0_1, player_round1_1, player_round2_1], 0)
        player_round0_1.sort_card()
        player_cards_gui = roundgui.create_cards_gui(player_round0_1.cards, all_sprites)
        oponent1_cards_gui = roundgui.create_cards_gui(player_round1_1.cards, all_sprites)
        oponent2_cards_gui = roundgui.create_cards_gui(player_round2_1.cards, all_sprites)
        prikup_cards_gui = roundgui.create_cards_gui(round1.bidding.prikup, all_sprites)

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == QUIT:
                    Database.leave_game(game.id_game)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                    if len(clicked_sprites) != 0:
                        clicked_sprites[len(clicked_sprites)-1].update(event_list)
                        pygame.display.update()

            self.display_surface.fill(BACKGROUND_COLOR)

            roundgui.display_player_cards(player_cards_gui)
            roundgui.display_bidding_cards(prikup_cards_gui, False)
            roundgui.display_oponent_cards(oponent1_cards_gui, 0)
            roundgui.display_oponent_cards(oponent2_cards_gui, 1)

            all_sprites.draw(self.display_surface)
            pygame.display.update()
            FramePerSec.tick(FPS)

