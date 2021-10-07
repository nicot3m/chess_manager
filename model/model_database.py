"""
module with class Database
"""

from tinydb import TinyDB, Query


# from model_player import Player
from model.model_player import Player
from model.model_tournament import Tournament
from model.model_round import Round
from model.model_game import Game


class Database:
    """
    Contains the model of the database
    """

    def __init__(self):
        self.database = TinyDB("database/database.json")
        self.tournament_table = self.database.table("tournament")
        self.player_table = self.database.table("players")

    def add_tournament_in_database(self, tournament):
        serialized_tournament = tournament.serialize_tournament()
        self.tournament_table.insert(serialized_tournament)

    def add_player_in_database(self, tournament, player, field_choice):

        serialized_player = player.serialize_player()

        # Add player in player table
        if field_choice == 2:
            self.player_table.insert(serialized_player)

        # Update tournament player list
        tournament.serialized_player_list.append(serialized_player)
        T = Query()
        self.tournament_table.update({"playerList": tournament.serialized_player_list},
                                     T.name == tournament.name)

    def update_database(self, tournament):
        serialized_tournament = tournament.serialize_tournament()
        T = Query()
        self.tournament_table.remove(T.name == tournament.name)
        self.tournament_table.insert(serialized_tournament)

    def get_tournament_from_database(self, name):
        User = Query()
        serialized_tournament = self.tournament_table.search(User.name == name)
        tournament = self.deserialize_tournament(serialized_tournament)
        return tournament

    def deserialize_player(self, serialized_player):
        player = Player()
        player.id = serialized_player[0]['id']
        player.first_name = serialized_player[0]['firstName']
        player.last_name = serialized_player[0]['lastName']
        player.date_of_birth = serialized_player[0]['dateOfBirth']
        player.gender = serialized_player[0]['gender']
        player.global_ranking = serialized_player[0]["globalRanking"]
        player.tournament_ranking = serialized_player[0]["tournamentRanking"]
        player.points = serialized_player[0]["points"]
        return player

    def deserialize_tournament(self, serialized_tournament):
        tournament = Tournament()
        tournament.id = serialized_tournament[0]["id"]
        tournament.name = serialized_tournament[0]["name"]
        tournament.location = serialized_tournament[0]["location"]
        tournament.start_date = serialized_tournament[0]["startDate"]
        tournament.end_date = serialized_tournament[0]["endDate"]
        tournament.rating = serialized_tournament[0]["rating"]
        tournament.description = serialized_tournament[0]["description"]
        tournament.tournament_in_progress = serialized_tournament[0]["tournamentInProgress"]
        tournament.serialized_player_list = serialized_tournament[0]["playerList"]
        tournament.serialized_round_list = serialized_tournament[0]["roundList"]
        # Deserialize player list
        for serialized_player in tournament.serialized_player_list:
            serialized_player = [serialized_player]
            player = self.deserialize_player(serialized_player)
            tournament.player_list.append(player)

        for serialized_round in tournament.serialized_round_list:
            chess_round = Round("", int())
            chess_round.id = serialized_round["id"]
            chess_round.name = serialized_round["name"]
            chess_round.start_date_time = serialized_round["startDateTime"]
            chess_round.end_date_time = serialized_round["endDateTime"]
            chess_round.round_in_progress = serialized_round["roundInProgress"]
            chess_game_tuple_list = serialized_round["games"]
            tournament.round_list.append(chess_round)

            # Deserialize games
            for serialized_game_tuple in chess_game_tuple_list:
                game = Game("", "")
                chess_round.game_list.append(game)
                serialized_opponent_list1 = serialized_game_tuple[0]
                serialized_opponent_list2 = serialized_game_tuple[1]
                game.score1 = serialized_opponent_list1[1]
                game.score2 = serialized_opponent_list2[1]
                serialized_opponent1 = [serialized_opponent_list1[0]]
                serialized_opponent2 = [serialized_opponent_list2[0]]
                opponent1 = self.deserialize_player(serialized_opponent1)
                opponent2 = self.deserialize_player(serialized_opponent2)

                # Player and opponent matching
                for player in tournament.player_list:
                    if opponent1 == player:
                        game.opponent1 = player
                    if opponent2 == player:
                        game.opponent2 = player

                game.opponent_list1 = [game.opponent1, game.score1]
                game.opponent_list2 = [game.opponent2, game.score2]
                game.game_tuple = (game.opponent_list1, game.opponent_list2)
                chess_round.game_tuple_list.append(game.game_tuple)
                set1 = {game.opponent1, game.opponent2}
                tournament.pair_set_list.append(set1)
        return tournament

    def update_player_global_ranking(self, player_id, global_ranking):
        User = Query()
        self.player_table.update({"globalRanking": global_ranking}, User.id == player_id)

    def get_all_player_from_database(self):
        serialized_players = self.player_table.all()
        all_player_list = []
        for serialized_player in serialized_players:
            all_player_list.append(self.deserialize_player([serialized_player]))
        return all_player_list

    def find_tournament_in_progress(self):
        T = Query()
        serialized_tournament_in_progress = self.tournament_table.search(T.tournamentInProgress == True)  # noqa: E712

        if serialized_tournament_in_progress == []:
            found_tournament_in_progress = False
            name = ""
        else:
            found_tournament_in_progress = True
            name = serialized_tournament_in_progress[0]["name"]
        return found_tournament_in_progress, name

    def find_round_in_progress(self):
        T = Query()
        serialized_tournament_in_progress = self.tournament_table.search(T.tournamentInProgress == True)  # noqa: E712
        serialized_round_list = serialized_tournament_in_progress[0]["roundList"]
        if serialized_round_list == []:
            found_round_in_progress = False
        else:
            found_round_in_progress = serialized_round_list[-1]["roundInProgress"]
        return found_round_in_progress

    def check_name_in_tournament_table(self, name):
        T = Query()
        checked_name_in_tournament_table = self.tournament_table.search(T.name == name)
        if len(checked_name_in_tournament_table) == 0:
            checked_name = False
        else:
            checked_name = True
        return checked_name

    def get_all_tournament_from_database(self):
        serialized_tournaments = self.tournament_table.all()
        all_tournament_list = []
        for serialized_tournament in serialized_tournaments:
            all_tournament_list.append(self.deserialize_tournament([serialized_tournament]))
        return all_tournament_list

    def get_table_player_length(self):
        table_player_length = len(self.player_table)
        return table_player_length

    def get_table_tournament_length(self):
        table_tournament_length = len(self.tournament_table)
        return table_tournament_length
