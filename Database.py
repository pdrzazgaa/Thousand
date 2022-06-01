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
                                  "P0_1 Integer not null, P0_2 Integer not null, P0_3 Integer not null, P0_4 Integer not null," \
                                  "P0_5 Integer not null, P0_6 Integer not null, P0_7 Integer not null, P0_8 Integer not null," \
                                  "P1_1 Integer not null, P1_2 Integer not null, P1_3 Integer not null, P1_4 Integer not null," \
                                  "P1_5 Integer not null, P1_6 Integer not null, P1_7 Integer not null, P1_8 Integer not null," \
                                  "P2_1 Integer not null, P2_2 Integer not null, P2_3 Integer not null, P2_4 Integer not null," \
                                  "P2_5 Integer not null, P2_6 Integer not null, P2_7 Integer not null, P2_8 Integer not null," \
                                  "PickUp1 Integer not null, PickUp2 Integer not null, PickUp3 Integer not null, " \
                                  "Bid Integer, " \
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
                                     "IfBomb Integer, " \
                                     "IfAgainDealing Integer, " \
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
                print("MySQL connection is closed")

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
                        str(id_game)+") from GAMES_1000 where IdG = "+str(id_game)
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def join_game(id_game):
        query_create_game = "update GAMES_1000 set Players = Players + 1 where IdG like "+str(id_game)
        return Database.execute_db(query_create_game)

    @staticmethod
    def leave_game(id_game):
        query_leave_game = "update GAMES_1000 set Players = Players - 1 where IdG like "+str(id_game)
        return Database.execute_db(query_leave_game)

    @staticmethod
    def make_move(idg, idr, idp, i_card_color, i_card_value, b_if_king_queen_pair, b_if_bomb, b_if_again_dealing):
        card_color = "null" if i_card_color is None else str(i_card_color)
        card_value = "null" if i_card_value is None else str(i_card_value)
        if_king_queen_pair = "1" if b_if_king_queen_pair is None else "0"
        if_bomb = "1" if b_if_bomb is None else "0"
        if_again_dealing = "1" if b_if_again_dealing is None else "0"

        query_make_move = "insert into MOVEMENTS_1000 (IdG, IdR, IdP, CardColor, CardValue, IfKingQueenPair, IfBomb, " \
                            "IfAgainDealing) values (" + idg + \
                            ", " + idr + ", " + idp + ", " + card_color + ", " + card_value + ", " + if_king_queen_pair \
                            + ", " + if_bomb + ", " + if_again_dealing + ")"

        return Database.execute_db(query_make_move)

    @staticmethod
    def check_players(id_game):
        query_check_game = "select Players from GAMES_1000 where IdG = " + str(id_game)
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_moves(id_game):
        query_check_game = "select * from MOVEMENTS_1000 where IdG = " + str(id_game) + \
                           " limit 1 order by MoveDateTime desc"
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_round(id_game):
        query_check_game = "select * from ROUNDS_1000 where IdG = " + str(id_game) + \
                           " limit 1 order by RoundDateTime desc"
        results = Database.select_db(query_check_game)
        return results

    @staticmethod
    def check_bidding(id_game):
        query_check_game = "select * from BIDS_1000 where IdG = " + str(id_game) + " limit 1 order by BidDateTime desc"
        results = Database.select_db(query_check_game)
        return results