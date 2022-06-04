import time
from threading import Event

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
    hidden_prikup = True
    end_bidding_phase = False
    game_phase = False
    player0_phase = False
    player1_phase = False
    player2_phase = False

    current_players_in_game = -1

    # Timery sprawdzające bazę - czy są jacyś gracze
    timers: [RepeatedTimer]
    timer_check_players: RepeatedTimer
    timer_check_dealing: RepeatedTimer
    timer_check_bidding: RepeatedTimer

    def __init__(self, game):
        self.game = game
        self.timer_check_players = RepeatedTimer(Event(), 2, self.check_players)
        self.timer_check_players.start()
        self.timer_check_dealing = RepeatedTimer(Event(), 2, self.check_dealing)
        self.timer_check_bidding = RepeatedTimer(Event(), 2, self.check_bidding)
        self.timers = []
        self.timers.append(self.timer_check_players)
        self.timers.append(self.timer_check_dealing)
        self.timers.append(self.timer_check_bidding)

    def check_players(self):
        self.current_players_in_game = Database.check_players(self.game.id_game)[0]
        if self.current_players_in_game == (3,):
            self.waiting_for_players_phase = False
            self.dealing_phase = True
            self.started_game_phase = True
            if not self.timer_check_dealing.is_running:
                self.timer_check_dealing.start()
        else:
            if not self.started_game_phase:
                self.waiting_for_players_phase = True
            else:
                self.player_left_game_phase = True

    def check_dealing(self):
        last_dealing = None if len(self.game.rounds) == 0 else \
            Database.check_round(self.game.id_game)
        if last_dealing is not None and len(last_dealing) != 0:
            IdR, IdG, P0_1, P0_2, P0_3, P0_4, P0_5, P0_6, P0_7, P0_8, \
            P1_1, P1_2, P1_3, P1_4, P1_5, P1_6, P1_7, P1_8, \
            P2_1, P2_2, P2_3, P2_4, P2_5, P2_6, P2_7, P2_8, \
            PickUp1, PickUp2, PickUp3, RoundDateTime = last_dealing[0]
            if self.game.rounds[-1].last_round != RoundDateTime:
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
                self.game.rounds[-1].last_round = RoundDateTime
                self.bidding_phase = True
                if not self.timer_check_bidding.is_running:
                    self.timer_check_bidding.start()
                if None in self.game.rounds[-1].bidding.prikup:
                    self.timer_check_dealing.cancel()
        else:
            self.waiting_for_dealing = True

    def check_bidding(self):
        id_round = self.game.rounds[-1].id_r
        last_bidding = None if len(self.game.rounds) == 0 else \
            Database.check_bidding(id_round)
        if last_bidding is not None and len(last_bidding) != 0:
            IdB, IdR, IdP, Bid, BidDateTime = last_bidding[0]
            if self.game.rounds[-1].bidding.last_bidding_date != BidDateTime:
                bidding = self.game.rounds[-1].bidding
                player_round = self.game.rounds[-1].players_rounds[IdP]
                # bidding.last_bidding_player_id = IdP
                bidding.last_bidding_date = BidDateTime
                if Bid != -1:
                    bidding.players_declaration_value(player_round, Bid)
                else:
                    bidding.pass_bid(player_round)
                if bidding.if_bidding_end():
                    self.hidden_prikup = False
                    time.sleep(8)
                    bidding.bidding_end()
                    self.bidding_phase = False
                    self.end_bidding_phase = True

    def check_moves(self, id_game):
        ...
