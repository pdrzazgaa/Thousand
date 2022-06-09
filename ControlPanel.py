import time
from threading import Event
from datetime import datetime

from RoundGui import RoundGUI
from Card import Card
from Database import Database
from Settings import TIME_FOR_RELOAD_MOVE
from Timer import RepeatedTimer
from GUISettings import TIME_CHECKING_PLAYERS, TIME_CHECKING_BIDDINGS, TIME_CHECKING_DEALINGS, \
    TIME_CHECKING_MOVES, TIME_CHECKING_BUGS

# Klasa koordynująca całym przebiegiem gry.
# Tutaj sprawdzany jest aktualny stan bazy oraz zadeklarowane są odpowiednie stany gry.


class ControlPanel:
    # Etapy gry
    started_game_phase = False
    player_left_game_phase = False

    waiting_for_players_phase = True
    dealing_phase = False
    waiting_for_dealing_phase = False

    bidding_phase = False
    hidden_prikup = True
    end_bidding_phase = False
    game_phase = False
    end_round_phase = False
    end_game_phase = False

    full_desk = False
    made_move = False

    checking_time = datetime.now()

    currently_players_in_game = -1

    # Timery sprawdzające bazę - czy są jacyś gracze
    timers: [RepeatedTimer]
    timer_check_players: RepeatedTimer
    timer_check_dealing: RepeatedTimer
    timer_check_bidding: RepeatedTimer
    timer_check_bugs: RepeatedTimer

    def __init__(self, game, info_label):
        self.game = game
        self.timer_check_players = RepeatedTimer(Event(), TIME_CHECKING_PLAYERS, self.check_players)
        self.timer_check_players.start()
        self.timer_check_dealing = RepeatedTimer(Event(), TIME_CHECKING_DEALINGS, self.check_dealing)
        self.timer_check_bidding = RepeatedTimer(Event(), TIME_CHECKING_BIDDINGS, self.check_bidding)
        self.timer_check_moves = RepeatedTimer(Event(), TIME_CHECKING_MOVES, self.check_moves)
        self.timer_check_bugs = RepeatedTimer(Event(), TIME_CHECKING_BUGS, self.check_if_no_bug)
        self.timers = []
        self.timers.append(self.timer_check_players)
        self.timers.append(self.timer_check_dealing)
        self.timers.append(self.timer_check_bidding)
        self.timers.append(self.timer_check_moves)
        self.timers.append(self.timer_check_bugs)
        self.info_label = info_label

    def check_players(self):
        currently_players_sb = Database.check_players(self.game.id_game, self.info_label)
        if currently_players_sb is not None:
            self.currently_players_in_game = currently_players_sb[0][0]
            if self.currently_players_in_game == 3:
                self.waiting_for_players_phase = False
                self.dealing_phase = True
                self.started_game_phase = True
                if not self.timer_check_dealing.is_running and not self.timer_check_dealing.is_stopped:
                    self.timer_check_dealing.start()
            else:
                if not self.started_game_phase:
                    self.waiting_for_players_phase = True
                else:
                    self.player_left_game_phase = True

    def check_dealing(self):
        last_dealing = None if len(self.game.rounds) == 0 else \
            Database.check_round(self.game.id_game, self.info_label)
        if last_dealing is not None and len(last_dealing) != 0:
            IdR, IdG, DealingPlayer, \
            P0_1, P0_2, P0_3, P0_4, P0_5, P0_6, P0_7, P0_8, \
            P1_1, P1_2, P1_3, P1_4, P1_5, P1_6, P1_7, P1_8, \
            P2_1, P2_2, P2_3, P2_4, P2_5, P2_6, P2_7, P2_8, \
            PickUp1, PickUp2, PickUp3, IfBomb, IfAgainDealing, RoundDateTime = last_dealing[0]
            if self.game.rounds[-1].last_round != RoundDateTime:
                if IfBomb == 1:
                    ...
                    # self.game.rounds[-1].used_bomb(self.game.rounds[-1].bidding.last_bidding_player_id, self.game)
                    # self.info_label.show_label("Player %i used bomb" %
                    #                            self.game.rounds[-1].bidding.last_bidding_player_id)
                    # self.timer_check_dealing.cancel()
                    # time.sleep(5)
                    # self.end_bidding_phase = False
                    # self.game_phase = True
                    # self.end_round_phase = True
                    # time.sleep(15)
                    # self.start_new_round()
                    # return
                elif IfAgainDealing == 1:
                    ...

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
                self.game.rounds[-1].dealing_player = DealingPlayer
                self.waiting_for_dealing_phase = False
                if not self.timer_check_bidding.is_running and not self.timer_check_bidding.is_stopped:
                    self.timer_check_bidding.start()
                if None in self.game.rounds[-1].bidding.prikup:
                    self.bidding_phase = False
                    self.end_bidding_phase = False
                    self.dealing_phase = False
                    self.game_phase = True
                    self.timer_check_dealing.cancel()
                    self.timer_check_bugs.start()
                    self.timer_check_moves.start()
                else:
                    self.bidding_phase = True
        else:
            self.waiting_for_dealing_phase = True

    def check_bidding(self):
        id_round = self.game.rounds[-1].id_r
        last_bidding = None if len(self.game.rounds) == 0 else \
            Database.check_bidding(id_round, self.info_label)
        if last_bidding is not None and len(last_bidding) != 0:
            IdB, IdR, IdP, Bid, BidDateTime = last_bidding[0]
            if self.game.rounds[-1].bidding.last_bidding_date != BidDateTime or \
                    (datetime.now() - self.checking_time).total_seconds() > TIME_FOR_RELOAD_MOVE:
                bidding = self.game.rounds[-1].bidding
                player_round = self.game.rounds[-1].players_rounds[IdP]
                if self.game.rounds[-1].bidding.last_bidding_date != BidDateTime:
                    self.checking_time = BidDateTime
                    bidding.last_bidding_date = BidDateTime
                    if Bid != -1:
                        bidding.players_declaration_value(player_round, Bid)
                    else:
                        bidding.pass_bid(player_round)
                else:
                    self.game.reload_last_round(self.info_label)
                    self.checking_time = datetime.now()
                if bidding.if_bidding_end():
                    self.hidden_prikup = False
                    self.timer_check_bidding.cancel()
                    time.sleep(8)
                    bidding.bidding_end()
                    self.bidding_phase = False
                    self.end_bidding_phase = True

    def check_moves(self):
        id_round = self.game.rounds[-1].id_r
        last_move = Database.check_moves(id_round, self.info_label)
        if last_move is not None and len(last_move) != 0:
            IdM, IdR, IdP, Color, Value, IfQueenKingPair, MoveDateTime = last_move[0]
            if self.game.rounds[-1].last_move != MoveDateTime or \
                    (datetime.now() - self.checking_time).total_seconds() > TIME_FOR_RELOAD_MOVE:
                desk = self.game.rounds[-1].desk
                current_round = self.game.rounds[-1]
                if self.game.rounds[-1].last_move != MoveDateTime:
                    self.checking_time = MoveDateTime
                    player_round = self.game.rounds[-1].players_rounds[IdP]
                    current_round.last_move = MoveDateTime
                    card = Card(Color, Value)
                    player_round.play_card(desk, IdP, card, IfQueenKingPair == 1, self.game, self.info_label)
                    RoundGUI.if_queen_king_pair_info(card, IfQueenKingPair == 1, self.info_label)
                    current_round.last_move_player_id = IdP
                    if IfQueenKingPair == 1:
                        current_round.atut = Color
                    self.made_move = True
                else:
                    self.game.reload_last_round(self.info_label)
                    self.checking_time = datetime.now()
                    self.made_move = True
                if None not in desk:
                    self.full_desk = True
                    time.sleep(4)
                    self.game.rounds[-1].end_move()
                    self.full_desk = False
                    self.made_move = True
                if current_round.check_if_end_round():
                    current_round.end_round(self.game)
                    time.sleep(2)
                    if self.game.check_end():
                        self.timer_check_players.cancel()
                        self.timer_check_moves.cancel()
                        self.end_game_phase = True
                        self.game_phase = False
                    else:
                        self.end_round_phase = True
                        time.sleep(15)
                        self.game_phase = False
                        self.start_new_round()

    # Sprawdzamy, czy wszystko zostało dobrze wczytane
    def check_if_no_bug(self):
        if self.game.rounds[-1].count_cards_in_round() % 3 != 0:
            self.game.reload_last_round(self.info_label)
            self.made_move = True

    # Rozpoczęcie nowej rundy
    def start_new_round(self):
        self.dealing_phase = True
        self.waiting_for_dealing_phase = False

        self.bidding_phase = False
        self.hidden_prikup = True
        self.end_bidding_phase = False
        self.game_phase = False
        self.end_round_phase = False

        self.full_desk = False
        self.made_move = False
        self.reset_timers()

        self.end_game_phase = False

    def reset_timers(self):
        self.timer_check_bugs.cancel()
        self.timer_check_dealing.cancel()
        self.timer_check_bidding.cancel()
        self.timer_check_moves.cancel()
        self.timer_check_dealing = RepeatedTimer(Event(), TIME_CHECKING_DEALINGS, self.check_dealing)
        self.timer_check_bidding = RepeatedTimer(Event(), TIME_CHECKING_BIDDINGS, self.check_bidding)
        self.timer_check_moves = RepeatedTimer(Event(), TIME_CHECKING_MOVES, self.check_moves)
        self.timer_check_bugs = RepeatedTimer(Event(), TIME_CHECKING_MOVES, self.check_if_no_bug)
        self.timers.append(self.timer_check_dealing)
        self.timers.append(self.timer_check_bidding)
        self.timers.append(self.timer_check_moves)
        self.timers.append(self.timer_check_bugs)
        self.timer_check_dealing.start()
