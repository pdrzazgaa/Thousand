from tkinter import messagebox

import mysql.connector as db
from mysql.connector import Error

DB_USER = "db100061665"
DB_HOST = "mysql-paulina.halpress.eu"
DB_DATABASE = "db100061665"
DB_PASSWORD = "kcQb4oo2bVJrG"


class Database:
    __query_create_table_games = "CREATE TABLE IF NOT EXISTS GAMES_1000 " \
                                 "(IdG Integer not null primary key auto_increment, " \
                                 "Players Integer not null, " \
                                 "GameDateTime timestamp NOT NULL " \
                                 ")"
    __query_create_table_rounds = "CREATE TABLE IF NOT EXISTS ROUNDS_1000 " \
                                  "(IdR Integer not null primary key auto_increment, " \
                                  "IdG Integer not null, " \
                                  "P0_1 Integer not null, P0_2 Integer not null, " \
                                  "P0_3 Integer not null, P0_4 Integer not null," \
                                  "P0_5 Integer not null, P0_6 Integer not null, " \
                                  "P0_7 Integer not null, P0_8 Integer," \
                                  "P1_1 Integer not null, P1_2 Integer not null, " \
                                  "P1_3 Integer not null, P1_4 Integer not null," \
                                  "P1_5 Integer not null, P1_6 Integer not null, " \
                                  "P1_7 Integer not null, P1_8 Integer," \
                                  "P2_1 Integer not null, P2_2 Integer not null, " \
                                  "P2_3 Integer not null, P2_4 Integer not null," \
                                  "P2_5 Integer not null, P2_6 Integer not null, " \
                                  "P2_7 Integer not null, P2_8 Integer," \
                                  "PickUp1 Integer, PickUp2 Integer, PickUp3 Integer, " \
                                  "IfBomb Integer, " \
                                  "IfAgainDealing Integer, " \
                                  "RoundDateTime timestamp NOT NULL " \
                                  ")"
    __query_create_table_bids = "CREATE TABLE IF NOT EXISTS BIDS_1000 " \
                                "(IdB Integer not null primary key auto_increment, " \
                                "IdR Integer not null, " \
                                "IdP Integer not null, " \
                                "Bid Integer, " \
                                "BidDateTime timestamp NOT NULL " \
                                ")"
    __query_create_table_movements = "CREATE TABLE IF NOT EXISTS MOVEMENTS_1000 " \
                                     "(IdM Integer not null primary key auto_increment, " \
                                     "IdR Integer not null, " \
                                     "IdP Integer not null, " \
                                     "CardColor Integer, " \
                                     "CardValue Integer, " \
                                     "IfKingQueenPair Integer, " \
                                     "MoveDateTime timestamp NOT NULL " \
                                     ")"

    @staticmethod
    def connect():
        try:
            connection = db.connect(host=DB_HOST,
                                    database=DB_DATABASE,
                                    user=DB_USER,
                                    password=DB_PASSWORD)
            if connection.is_connected():
                # db_info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor()
                return cursor
                # record = cursor.fetchone()
                # print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")

    @staticmethod
    def execute_db(query):
        try:
            connection = db.connect(host=DB_HOST,
                                    database=DB_DATABASE,
                                    user=DB_USER,
                                    password=DB_PASSWORD)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
        except Error as e:
            print("Error while connecting to MySQL or creating a table", e)
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                return True

    @staticmethod
    def select_db(query):
        my_results = None
        try:
            connection = db.connect(host=DB_HOST,
                                    database=DB_DATABASE,
                                    user=DB_USER,
                                    password=DB_PASSWORD)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                my_results = cursor.fetchall()
        except Error as e:
            print("Error while connecting to MySQL or creating a table", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            return my_results

    @staticmethod
    def create_tables():
        try:
            connection = db.connect(host=DB_HOST,
                                    database=DB_DATABASE,
                                    user=DB_USER,
                                    password=DB_PASSWORD)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(Database.__query_create_table_games)
                cursor.execute(Database.__query_create_table_rounds)
                cursor.execute(Database.__query_create_table_bids)
                cursor.execute(Database.__query_create_table_movements)
        except Error as e:
            messagebox("Information", "Error while connecting to MySQL")
            print("Error while connecting to MySQL or creating a table", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    @staticmethod
    def create_game():
        query_create_game = "insert into GAMES_1000 (players) values (0)"
        Database.execute_db(query_create_game)

    @staticmethod
    def get_game_id():
        query_create_game = "select IdG from GAMES_1000 order by GameDateTime desc limit 1"
        id_game = Database.select_db(query_create_game)
        return id_game

    @staticmethod
    def check_game(id_game):
        query_check_game = "select Players, (select count(IdR) from ROUNDS_1000 where IdG = " + \
                           str(id_game) + ") from GAMES_1000 where IdG = " + str(id_game)
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def join_game(id_game):
        query_create_game = "update GAMES_1000 set Players = Players + 1 where IdG like " + str(id_game)
        return Database.execute_db(query_create_game)

    @staticmethod
    def leave_game(id_game):
        query_leave_game = "update GAMES_1000 set Players = Players - 1 where IdG like " + str(id_game)
        return Database.execute_db(query_leave_game)

    @staticmethod
    def make_move(idr, idp, i_card_color, i_card_value, b_if_king_queen_pair):
        card_color = "null" if i_card_color is None else str(i_card_color)
        card_value = "null" if i_card_value is None else str(i_card_value)
        if_king_queen_pair = "1" if b_if_king_queen_pair else "0"

        query_make_move = "insert into MOVEMENTS_1000 (IdR, IdP, CardColor, CardValue, IfKingQueenPair" \
                          ") values (" + str(idr) + ", " + str(idp) + ", " + str(card_color) + ", " + \
                          str(card_value) + ", " + str(if_king_queen_pair) + ")"

        return Database.execute_db(query_make_move)

    @staticmethod
    def deal_cards(idg, p01, p02, p03, p04, p05, p06, p07, p08, p11, p12, p13, p14, p15, p16, p17, p18,
                   p21, p22, p23, p24, p25, p26, p27, p28, pc1, pc2, pc3):
        query_deal_cards = "insert into ROUNDS_1000 " \
                           "(IdG, P0_1, P0_2, P0_3, P0_4, P0_5, P0_6, P0_7, P0_8," \
                           "P1_1, P1_2, P1_3, P1_4, P1_5, P1_6, P1_7, P1_8, " \
                           "P2_1, P2_2, P2_3, P2_4, P2_5, P2_6, P2_7, P2_8, " \
                           "PickUp1, PickUp2, PickUp3) values (" + idg + \
                           ", " + p01 + ", " + p02 + ", " + p03 + ", " + p04 + \
                           ", " + p05 + ", " + p06 + ", " + p07 + ", " + p08 + \
                           ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + \
                           ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + \
                           ", " + p21 + ", " + p22 + ", " + p23 + ", " + p24 + \
                           ", " + p25 + ", " + p26 + ", " + p27 + ", " + p28 + \
                           ", " + pc1 + ", " + pc2 + ", " + pc3 + ")"

        return Database.execute_db(query_deal_cards)

    @staticmethod
    def update_dealing(idr, p01, p02, p03, p04, p05, p06, p07, p08, p11, p12, p13, p14, p15, p16, p17, p18,
                       p21, p22, p23, p24, p25, p26, p27, p28, b_if_bomb, b_if_again_dealing):

        if_bomb = "1" if b_if_bomb is None else "0"
        if_again_dealing = "1" if b_if_again_dealing is None else "0"

        query_deal_cards = "UPDATE ROUNDS_1000 SET " \
                           "P0_1 = " + p01 + ", P0_2 = " + p02 + ", P0_3 = " + p03 + ", " \
                           "P0_4 = " + p04 + ", P0_5 = " + p05 + ", P0_6 = " + p06 + ", " \
                           "P0_7 = " + p07 + ", P0_8 = " + p08 + "," \
                           "P1_1 = " + p11 + ", P1_2 = " + p12 + ", P1_3 = " + p13 + ", " \
                           "P1_4 = " + p14 + ", P1_5 = " + p15 + ", P1_6 = " + p16 + ", " \
                           "P1_7 = " + p17 + ", P1_8 = " + p18 + "," \
                           "P2_1 = " + p21 + ", P2_2 = " + p22 + ", P2_3 = " + p23 + ", " \
                           "P2_4 = " + p24 + ", P2_5 = " + p25 + ", P2_6 = " + p26 + ", " \
                           "P2_7 = " + p27 + ", P2_8 = " + p28 + ", " \
                           "PickUp1 =  null, PickUp2 = null, PickUp3 = null, " \
                           "IfBomb = " + if_bomb + ", IfAgainDealing = " + if_again_dealing + \
                           " where IdR = "+idr

        return Database.execute_db(query_deal_cards)

    @staticmethod
    def make_bid(id_r, id_p, bid):
        query_create_game = "insert into BIDS_1000 (IdR, IdP, Bid) values (" + str(id_r) + ", " + str(id_p) + \
                            ", " + str(bid) + ")"
        Database.execute_db(query_create_game)

    @staticmethod
    def check_players(id_game):
        query_check_game = "select Players from GAMES_1000 where IdG = " + str(id_game)
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_moves(id_game):
        query_check_game = "select * from MOVEMENTS_1000 where IdR = " + str(id_game) + \
                           " order by MoveDateTime desc limit 1"
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_round(id_round):
        query_check_game = "select * from ROUNDS_1000 where IdG = " + str(id_round) + \
                           " order by RoundDateTime desc limit 1"
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_bidding(id_round):
        query_check_game = "select * from BIDS_1000 where IdR = " + str(id_round) + " order by BidDateTime desc limit 1"
        results = Database.select_db(query_check_game)
        return results
