"""
module with class ControlTournamentReport
"""

from operator import attrgetter


from view.view_tournament import ViewTournament
from controller.control_new_tournament import ControlNewTournament
from view.viewer import View
from view.view_player import ViewPlayer
from model.model_tournament import Tournament
from model.model_database import Database


class ControlTournamentReport:
    """
    Controls the tournament report
    """

    def __init__(self):
        self.viewed_tournament = ViewTournament()
        self.controlled_new_tournament = ControlNewTournament()
        self.view = View()
        self.viewed_player = ViewPlayer()
        self.tournament = Tournament()
        self.database = Database()

    def control_tournament_players_report(self, choice_sub_menu):
        self.tournament = Tournament()
        self.database = Database()

        # Ask for tournament name
        self.tournament.name = self.controlled_new_tournament.control_tournament_data("name")

        # Check that this tournament exists in the database
        checked_name = self.database.check_name_in_tournament_table(self.tournament.name)

        # If this tournament does not exist, show message
        if checked_name is False:
            self.view.show_message_data_not_valid()

        # If this tournament exists, get tournament from database
        else:
            self.tournament = self.database.get_tournament_from_database(self.tournament.name)

            # Sort players by name
            if choice_sub_menu == 3:
                report_player_list = sorted(self.tournament.player_list, key=attrgetter("first_name"),
                                            reverse=False)
                field = "in AZ"

            # Sort players by tournament ranking
            elif choice_sub_menu == 4:
                report_player_list = sorted(self.tournament.player_list, key=attrgetter("tournament_ranking"),
                                            reverse=False)
                field = "by tournament ranking"

            # Show players
            counter = 1
            for player in report_player_list:
                self.viewed_player.show_tournament_players_report(counter, player, field)
                counter += 1

    def control_all_tournaments_report(self):
        self.database = Database()
        all_tournament_list = self.database.get_all_tournament_from_database()

        counter = 1
        for tournament in all_tournament_list:
            self.viewed_tournament.show_all_tournaments_report(counter, tournament)
            counter += 1

    def control_rounds_games_report(self, choice_sub_menu):
        self.tournament = Tournament()
        self.database = Database()

        # Ask for tournament name
        self.tournament.name = self.controlled_new_tournament.control_tournament_data("name")

        # Check that this tournament exists in the database
        checked_name = self.database.check_name_in_tournament_table(self.tournament.name)

        # If this tournament does not exist, show message
        if checked_name is False:
            self.view.show_message_data_not_valid()

        # If this tournament exists, get tournament from database
        else:
            self.tournament = self.database.get_tournament_from_database(self.tournament.name)

            # If there are no rounds in tournament, show message
            if len(self.tournament.round_list) == 0:
                self.view.show_message_create_round_first()

            # If there are rounds in tournament, make reports
            else:
                # Show tournament rounds
                if choice_sub_menu == 6:
                    counter = 1
                    for chess_round in self.tournament.round_list:
                        self.viewed_tournament.show_tournament_all_rounds_report(counter, self.tournament, chess_round)
                        counter += 1

                # Show tournament games
                elif choice_sub_menu == 7:
                    counter = 1
                    for chess_round in self.tournament.round_list:
                        for game in chess_round.game_list:
                            self.viewed_tournament.show_tournament_all_games_report(counter, self.tournament,
                                                                                    chess_round, game)
                            counter += 1
