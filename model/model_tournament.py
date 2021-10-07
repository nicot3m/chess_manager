"""
module with class Tournament
"""


from operator import attrgetter
from datetime import datetime


from model.model_round import Round
from controller.control_tournament import ControlTournament


class Tournament:
    """
    Contains the model of the tournament
    """

    def __init__(self):
        self.id = int()
        self.name = ""
        # Default value = 8
        self.nb_of_players = 8
        # Default value = 4
        self.nb_of_rounds = 4
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        # Bullet rating or Blitz rating or Rapid rating
        self.rating = ""
        # Tournament director remark
        self.description = ""
        self.tournament_in_progress = False
        self.player_list = []
        # list of 4 rounds
        self.round_list = []
        self.pair_set_list = []
        self.serialized_player_list = []
        self.serialized_round_list = []
        self.controlled_tournament = ControlTournament()

    def __repr__(self):
        return "{}".format(self.name)

    def sort_player_list(self):
        self.player_list = sorted(self.player_list, key=attrgetter("points", "global_ranking"), reverse=True)

        # Update tournament_ranking
        for i in range(self.nb_of_players):
            self.player_list[i].tournament_ranking = i + 1

    def create_round(self, round_id):
        # Sort the players
        self.sort_player_list()

        # Instantiate a new round
        round_name = "Round " + str(round_id + 1)
        chess_round = Round(round_name, round_id)

        # Mark the round in progress
        chess_round.round_in_progress = True

        # Define start date time
        chess_round.start_date_time = datetime.now().isoformat(timespec='seconds').replace("T", " at ")

        # Create games for the first round
        if round_id == 0:
            self.pair_set_list = chess_round.create_games_first_round(self.nb_of_players, self.player_list,
                                                                      self.pair_set_list)

        # Create games for the next round
        else:
            self.pair_set_list = chess_round.create_games_next_round(self.nb_of_players, self.player_list,
                                                                     self.pair_set_list)
        chess_round.create_game_tuple_list()
        self.round_list.append(chess_round)

        # Show round games
        counter_game = 0
        for game in (self.round_list[round_id]).game_list:
            self.controlled_tournament.control_show_round_games(game.opponent1, game.opponent2, counter_game, round_id)
            counter_game += 1

    def model_game_results(self, round_id):
        # Manage the round game results
        # Ask for the round scores
        counter_game = 0
        for game in (self.round_list[round_id]).game_list:
            game_result = self.controlled_tournament.control_game_result(game.opponent1, game.opponent2, counter_game,
                                                                         round_id)

            if game_result == "1":
                game.score1 = 1
                game.opponent1.points += 1
            elif game_result == "2":
                game.score2 = 1
                game.opponent2.points += 1
            elif game_result == "0.5":
                game.score1 = 0.5
                game.opponent1.points += 0.5
                game.score2 = 0.5
                game.opponent2.points += 0.5
            counter_game += 1

        # sort the players
        self.sort_player_list()

        # show the player ranking
        self.controlled_tournament.control_show_player_ranking(self.player_list)

        # Terminate the round
        (self.round_list[round_id]).round_in_progress = False
        (self.round_list[round_id]).end_date_time = datetime.now().isoformat(timespec='seconds').replace("T", " at ")

        # Terminate the tournament
        if len(self.round_list) == self.nb_of_rounds:
            self.tournament_in_progress = False
            end_date = datetime.now().date()
            self.end_date = end_date

    def serialize_player_list(self):
        self.serialized_player_list = []
        for player in self.player_list:
            serialized_player = player.serialize_player()
            self.serialized_player_list.append(serialized_player)

    def serialize_round_list(self):
        self.serialized_round_list = []
        for chess_round in self.round_list:
            serialized_round = chess_round.serialize_round()
            self.serialized_round_list.append(serialized_round)

    def serialize_tournament(self):
        self.serialize_round_list()
        self.serialize_player_list()
        serialized_tournament = {
            "id": self.id,
            "name": self.name,
            "numberOfPlayers": self.nb_of_players,
            "numberOfRounds": self.nb_of_rounds,
            "location": self.location,
            "startDate": str(self.start_date),
            "endDate": str(self.end_date),
            "rating": self.rating,
            "description": self.description,
            "tournamentInProgress": self.tournament_in_progress,
            "playerList": self.serialized_player_list,
            "roundList": self.serialized_round_list
        }
        return serialized_tournament
