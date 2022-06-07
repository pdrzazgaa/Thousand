from Card import Card
from Database import Database
from PlayerRound import PlayerRound
from Round import Round


class LoadRound:

    __round: Round

    def __init__(self, game, id_r, info_label):
        self.__game = game
        self.info_label = info_label
        self.__round = self.get_last_round_from_db(id_r)
        self.get_all_moves_in_round_from_db(id_r)

    @property
    def round(self):
        return self.__round

    def get_last_round_from_db(self, id_r):
        new_round = None
        last_round_db = None if len(self.__game.rounds) == 0 else \
            Database.check_round_by_id_r(id_r, self.info_label)
        if last_round_db is not None and len(last_round_db) != 0:
            IdR, IdG, DealingPlayer, \
            P0_1, P0_2, P0_3, P0_4, P0_5, P0_6, P0_7, P0_8, \
            P1_1, P1_2, P1_3, P1_4, P1_5, P1_6, P1_7, P1_8, \
            P2_1, P2_2, P2_3, P2_4, P2_5, P2_6, P2_7, P2_8, \
            PickUp1, PickUp2, PickUp3, IfBomb, IfAgainDealing, RoundDateTime = last_round_db[0]

            new_round = Round([PlayerRound(self.__game.players[0]), PlayerRound(self.__game.players[1]),
                               PlayerRound(self.__game.players[2])], DealingPlayer)

            new_round.players_rounds[0].cards = [Card.card_from_sql(P0_1), Card.card_from_sql(P0_2),
                                                 Card.card_from_sql(P0_3), Card.card_from_sql(P0_4),
                                                 Card.card_from_sql(P0_5), Card.card_from_sql(P0_6),
                                                 Card.card_from_sql(P0_7), Card.card_from_sql(P0_8)]
            new_round.players_rounds[1].cards = [Card.card_from_sql(P1_1), Card.card_from_sql(P1_2),
                                                 Card.card_from_sql(P1_3), Card.card_from_sql(P1_4),
                                                 Card.card_from_sql(P1_5), Card.card_from_sql(P1_6),
                                                 Card.card_from_sql(P1_7), Card.card_from_sql(P1_8)]
            new_round.players_rounds[2].cards = [Card.card_from_sql(P2_1), Card.card_from_sql(P2_2),
                                                 Card.card_from_sql(P2_3), Card.card_from_sql(P2_4),
                                                 Card.card_from_sql(P2_5), Card.card_from_sql(P2_6),
                                                 Card.card_from_sql(P2_7), Card.card_from_sql(P2_8)]
            new_round.bidding.prikup = [Card.card_from_sql(PickUp1), Card.card_from_sql(PickUp2),
                                        Card.card_from_sql(PickUp3)]
            new_round.id_r = IdR
            new_round.last_round = RoundDateTime

        return new_round

    def get_all_moves_in_round_from_db(self, id_r):
        all_moves = Database.get_all_moves_from_current_round(id_r, self.info_label)
        if all_moves is not None and len(all_moves) != 0:
            for i in range(0, len(all_moves)):
                IdM, IdR, IdP, Color, Value, IfQueenKingPair, MoveDateTime = all_moves[i]
                desk = self.__round.desk
                current_round = self.__round
                player_round = current_round.players_rounds[IdP]
                current_round.last_move = MoveDateTime
                card = Card(Color, Value)
                player_round.play_card(desk, IdP, card, IfQueenKingPair == 1, self.__game, self.info_label)
                current_round.last_move_player_id = IdP
                if IfQueenKingPair == 1:
                    current_round.atut = Color
                if None not in desk:
                    current_round.end_move()

    def get_all_bids_in_round_from_db(self, id_r):
        all_bids = Database.get_all_bids_from_current_round(id_r, self.info_label)
        if all_bids is not None and len(all_bids) != 0:
            for i in range(0, len(all_bids)):
                bidding = all_bids[i]
                IdB, IdR, IdP, Bid, BidDateTime = bidding[0]
                if self.__round.bidding.last_bidding_date != BidDateTime:
                    bidding = self.__round.bidding
                    player_round = self.__round.players_rounds[IdP]
                    bidding.last_bidding_date = BidDateTime
                    if Bid != -1:
                        bidding.players_declaration_value(player_round, Bid)
                    else:
                        bidding.pass_bid(player_round)
                    if bidding.if_bidding_end():
                        bidding.bidding_end()




