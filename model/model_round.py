"""
module with class Round
"""


from model.model_game import Game
from view.view_tournament import ViewTournament


class Round:
    """
    Contains the model of the round
    """

    def __init__(self, round_name, round_id):
        # Round1, Round2, Round3, Round4
        self.id = round_id
        self.name = round_name
        # It fills up automatically when the user create a new round
        self.start_date_time = ""
        # It fills up automatically when the user close a round
        self.end_date_time = ""
        # list of 4 games
        self.game_list = []
        # list of 4 game tuples
        self.game_tuple_list = []
        self.round_in_progress = False
        self.serialized_game_tuple_list = []
        self.serialized_round = {}
        self.viewed_tournament = ViewTournament()

    def create_games_first_round(self, nb_of_players, player_list, pair_set_list):
        for i in range(int(nb_of_players / 2)):
            opponent1 = player_list[i]
            opponent2 = player_list[i + int(nb_of_players / 2)]
            set1 = {opponent1, opponent2}
            pair_set_list.append(set1)
            game = Game(opponent1, opponent2)
            self.game_list.append(game)
        return pair_set_list

    def create_games_next_round(self, nb_of_players, player_list, pair_set_list):
        opponent_list = []
        for i in range(int(nb_of_players - 1)):
            opponent1 = player_list[i]
            if opponent1 in opponent_list:
                pass
            else:
                opponent_list.append(opponent1)
                j = 1
                opponent2 = player_list[i + j]
                while ({opponent1, opponent2} in pair_set_list or
                       opponent2 in opponent_list) and (i + j) <= int(nb_of_players - 1):
                    j += 1
                    if (i + j) <= int(nb_of_players - 1):
                        opponent2 = player_list[i + j]
                opponent_list.append(opponent2)
                set1 = {opponent1, opponent2}
                if set1 in pair_set_list:
                    self.viewed_tournament.show_message_game_already_played(opponent1, opponent2)
                pair_set_list.append(set1)
                game = Game(opponent1, opponent2)
                self.game_list.append(game)
        return pair_set_list

    def create_game_tuple_list(self):
        for game in self.game_list:
            game_tuple = game.create_game_tuple()
            self.game_tuple_list.append(game_tuple)
        return self.game_tuple_list

    def serialize_round(self):
        self.serialized_game_tuple_list = []
        for game in self.game_list:
            self.serialized_game_tuple_list.append(game.serialize_game_tuple())
        self.serialized_round = {"id": self.id,
                                 "name": self.name,
                                 "startDateTime": self.start_date_time,
                                 "endDateTime": self.end_date_time,
                                 "roundInProgress": self.round_in_progress,
                                 "games": self.serialized_game_tuple_list}
        return self.serialized_round
