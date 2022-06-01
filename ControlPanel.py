from Card import Card
from Database import Database
from Timer import RepeatedTimer


class ControlPanel:
    # Etapy gry
    started_game_phase = False
    player_left_game_phase = False

    waiting_for_players_phase = True
    dealing_phase = False
    waiting_for_dealing = False

    bidding_phase = False
    end_bidding_phase = False
    game_phase = False
    player0_phase = False
    player1_phase = False
    player2_phase = False

    current_players_in_game = -1

    # Timery sprawdzające bazę - czy są jacyś gracze
    timer_check_players: RepeatedTimer
    timer_check_dealing: RepeatedTimer

    def __init__(self, game):
        self.game = game
        self.timer_check_players = RepeatedTimer(2.0, self.check_players)
        self.timer_check_dealing = None

    def check_players(self):
        self.current_players_in_game = Database.check_players(self.game.id_game)[0]
        if self.current_players_in_game == (3,):
            self.waiting_for_players_phase = False
            self.dealing_phase = True
            self.started_game_phase = True
            if self.timer_check_dealing is None:
                self.timer_check_dealing = RepeatedTimer(2.0, self.check_dealing)
        else:
            if not self.started_game_phase:
                self.waiting_for_players_phase = True
            else:
                self.player_left_game_phase = True

    def check_dealing(self):
        last_dealing = None if len(self.game.rounds) == 0 else \
            Database.check_round(self.game.id_game)
        if last_dealing is not None:
            IdR, IdG, P0_1, P0_2, P0_3, P0_4, P0_5, P0_6, P0_7, P0_8, \
            P1_1, P1_2, P1_3, P1_4, P1_5, P1_6, P1_7, P1_8, \
            P2_1, P2_2, P2_3, P2_4, P2_5, P2_6, P2_7, P2_8, \
            PickUp1, PickUp2, PickUp3, RoundDateTime = last_dealing[0]
            if self.game.rounds[-1].last_change != RoundDateTime:
                self.waiting_for_dealing = False
                self.game.rounds[-1].players_rounds[0].cards = [Card.card_from_sql(P0_1), Card.card_from_sql(P0_2),
                                                                Card.card_from_sql(P0_3), Card.card_from_sql(P0_4),
                                                                Card.card_from_sql(P0_5), Card.card_from_sql(P0_6),
                                                                Card.card_from_sql(P0_7), Card.card_from_sql(P0_8)]
                self.game.rounds[-1].players_rounds[1].cards = [Card.card_from_sql(P1_1), Card.card_from_sql(P1_2),
                                                                Card.card_from_sql(P1_3), Card.card_from_sql(P1_4),
                                                                Card.card_from_sql(P1_5), Card.card_from_sql(P1_6),
                                                                Card.card_from_sql(P1_7), Card.card_from_sql(P1_8)]
                self.game.rounds[-1].players_rounds[2].cards = [Card.card_from_sql(P2_1), Card.card_from_sql(P2_2),
                                                                Card.card_from_sql(P2_3), Card.card_from_sql(P2_4),
                                                                Card.card_from_sql(P2_5), Card.card_from_sql(P2_6),
                                                                Card.card_from_sql(P2_7), Card.card_from_sql(P2_8)]
                self.game.rounds[-1].bidding.prikup = [Card.card_from_sql(PickUp1), Card.card_from_sql(PickUp2),
                                                       Card.card_from_sql(PickUp3)]
                self.game.rounds[-1].id_r = IdR
                self.game.rounds[-1].last_change = RoundDateTime
                self.bidding_phase = True
                if None in self.game.rounds[-1].bidding.prikup and self.timer_check_dealing.is_running:
                    self.timer_check_dealing.stop()
        else:
            self.waiting_for_dealing = True

    def check_bidding(self, id_game):
        ...

    def check_moves(self, id_game):
        ...
