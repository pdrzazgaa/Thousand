from Database import Database

class ControlPanel:

    # Etapy gry
    waiting_for_players_phase = True
    dealing_phase = False
    bidding_phase = False
    end_bidding_phase = False
    game_phase = False
    player0_phase = False
    player1_phase = False
    player2_phase = False

    current_players_in_game = -1

    def check_players(self, id_game):
        self.current_players_in_game = Database.check_players(id_game)[0]
        if self.current_players_in_game == (3,):
            self.waiting_for_players_phase = False
            self.dealing_phase = True
        else:
            self.waiting_for_players_phase = True

    def check_bidding(self, id_game):
        ...

    def check_moves(self, id_game):
        ...
