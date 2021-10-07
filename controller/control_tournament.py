"""
module with class ControlTournament
"""

from view.viewer import View
from view.view_tournament import ViewTournament
from view.view_player import ViewPlayer


class ControlTournament:
    """
    Controls the model of the tournament
    """

    def __init__(self):
        self.view = View()
        self.viewed_tournament = ViewTournament()
        self.viewed_player = ViewPlayer()

    def control_show_round_games(self, opponent1, opponent2, counter, round_id):
        self.viewed_tournament.show_round_games(opponent1, opponent2, counter, round_id)

    def control_game_result(self, opponent1, opponent2, counter, round_id):
        check_data = False

        while check_data is False:
            game_result = self.viewed_tournament.prompt_game_result(opponent1, opponent2, counter, round_id)
            if game_result == "1" or game_result == "2" or game_result == "0.5":
                check_data = True
            else:
                self.view.show_message_data_not_valid()
        return game_result

    def control_show_player_ranking(self, player_list):
        counter = 1
        field = "by tournament ranking"
        for player in player_list:
            self.viewed_player.show_tournament_players_report(counter, player, field)
            counter += 1
