"""
module with class Controller
"""

import os.path
import os


from view.viewer import View
from view.view_player import ViewPlayer
from controller.control_new_tournament import ControlNewTournament
from controller.control_tournament_report import ControlTournamentReport
from controller.control_player import ControlPlayer
from model.model_tournament import Tournament
from model.model_database import Database


class Controller:
    """
    Controls the menus
    """

    def __init__(self):
        self.view = View()
        self.viewed_player = ViewPlayer()
        self.controlled_new_tournament = ControlNewTournament()
        self.control_tournament_report = ControlTournamentReport()
        self.controlled_player = ControlPlayer()
        self.tournament = Tournament()
        self.choice_main_menu = int()
        self.choice_sub_menu = int()
        self.nb_of_players = self.tournament.nb_of_players
        self.nb_of_rounds = self.tournament.nb_of_rounds
        self.database = Database()

    def clear_terminal(self):
        # Clear the terminal
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def control_choice_main_menu(self):
        self.choice_main_menu = int()
        check_choice = False
        while check_choice is False:
            self.choice_main_menu = self.view.show_main_menu()
            if self.choice_main_menu.isdigit() is True and int(self.choice_main_menu) in range(1, 6):
                check_choice = True
                self.choice_main_menu = int(self.choice_main_menu)
                self.clear_terminal()
            else:
                self.view.show_message_data_not_valid()

    def control_choice_sub_menu(self, field):
        self.choice_sub_menu = int()
        check_choice = False
        while check_choice is False:
            if field == "create_tournament_with_players":
                self.choice_sub_menu = self.view.show_create_tournament_with_players_menu()
                menu_items = 4
            elif field == "play_tournament":
                self.choice_sub_menu = self.view.show_play_tournament_menu()
                menu_items = 4
            elif field == "manage_players":
                self.choice_sub_menu = self.view.show_manage_players_menu()
                menu_items = 4
            elif field == "reports":
                self.choice_sub_menu = self.view.show_report_menu()
                menu_items = 9
            if self.choice_sub_menu.isdigit() is True and int(self.choice_sub_menu) in range(1, menu_items):
                check_choice = True
                self.choice_sub_menu = int(self.choice_sub_menu)
                self.clear_terminal()
            else:
                self.view.show_message_data_not_valid()

    # Check if the database is empty
    def check_if_database_empty(self):
        self.database = Database()
        #  Check if the database is empty for the first time the application is used
        path = "database/database.json"
        database_size = os.path.getsize(path)
        return database_size

    def run(self):
        while self.choice_main_menu != 5:
            self.choice_sub_menu = 0
            self.control_choice_main_menu()

            # Create a tournament with players
            if self.choice_main_menu == 1:
                self.choice_main_menu = 0
                while self.choice_sub_menu != 3:
                    self.database = Database()
                    self.control_choice_sub_menu("create_tournament_with_players")

                    # Create a tournament
                    if self.choice_sub_menu == 1:
                        # Check if the database is empty for the first time the application is used
                        database_size = self.check_if_database_empty()

                        # If the database empty, create a tournament
                        if database_size == 0:
                            self.tournament = self.controlled_new_tournament.create_tournament()

                        # If the database not empty
                        else:
                            #  Check if tournament in progress in the database
                            control_tournament_in_progress, name = self.database.find_tournament_in_progress()

                            # If tournament in progress, show message
                            if control_tournament_in_progress is True:
                                self.view.show_message_tournament_already_in_progress(name)

                            # If no tournament in progress, create a tournament
                            else:
                                self.tournament = self.controlled_new_tournament.create_tournament()

                    # Add the players to the tournament
                    elif self.choice_sub_menu == 2:
                        # Check if the database is empty for the first time the application is used

                        database_size = self.check_if_database_empty()

                        # If the database empty, show message
                        if database_size == 0:
                            self.view.show_message_create_tournament_first()

                        # If the database not empty, check if tournament in progress in the database
                        else:
                            control_tournament_in_progress, name = self.database.find_tournament_in_progress()

                            # If no tournament in progress, show message
                            if control_tournament_in_progress is False:
                                self.view.show_message_create_tournament_first()

                            # If tournament in progress, deserialize tournament in progress
                            else:
                                self.tournament = self.controlled_new_tournament.continue_tournament(name)

                                # If all players already added, show message
                                if len(self.tournament.player_list) == self.nb_of_players:
                                    self.view.show_message_all_players_already_added()

                                # If all players not in tournament, add players
                                else:
                                    self.controlled_new_tournament.add_players(self.nb_of_players, self.tournament)

                    # Come back to the main menu
                    elif self.choice_sub_menu == 3:
                        self.view.show_message_quit_sub_menu()

            # Begin or continue to play a tournament
            elif self.choice_main_menu == 2:
                self.choice_main_menu = 0

                # Check if the database is empty for the first time the application is used
                database_size = self.check_if_database_empty()

                # If the database empty, show message
                if database_size == 0:
                    self.view.show_message_create_tournament_first()

                # If the database not empty, check if tournament in progress in the database
                else:
                    control_tournament_in_progress, name = self.database.find_tournament_in_progress()

                    # If no tournament in progress, show message
                    if control_tournament_in_progress is False:
                        self.view.show_message_create_tournament_first()

                    # If tournament in progress, deserialize tournament in progress
                    else:
                        self.tournament = self.controlled_new_tournament.continue_tournament(name)

                        # If all players not already added, show message
                        if len(self.tournament.player_list) < self.nb_of_players:
                            self.view.show_message_add_players_first()

                        # If all players already added show play tournament menu
                        else:
                            while self.choice_sub_menu != 3:
                                self.control_choice_sub_menu("play_tournament")
                                self.database = Database()

                                # Create a new round and see the round games
                                if self.choice_sub_menu == 1:

                                    # Check if round already in progress
                                    control_round_in_progress = self.database.find_round_in_progress()

                                    # If round in progress, show message
                                    if control_round_in_progress is True:
                                        self.view.show_message_enter_results_first()

                                    # If no round in progress, check the number of rounds
                                    else:

                                        # If all rounds created, show message
                                        if len(self.tournament.round_list) >= self.nb_of_rounds:
                                            self.view.show_message_tournament_finished()

                                        # If all rounds not created, create round
                                        else:
                                            round_id = len(self.tournament.round_list)
                                            self.tournament.create_round(round_id)

                                            # Add round in the database
                                            self.database.update_database(self.tournament)

                                # Enter the round results and see the player ranking
                                elif self.choice_sub_menu == 2:
                                    # Check if round already in progress
                                    control_round_in_progress = self.database.find_round_in_progress()

                                    # If no round in progress
                                    if control_round_in_progress is False:
                                        self.view.show_message_create_round_first()

                                    # If round already in progress, enter the results
                                    else:
                                        round_id = len(self.tournament.round_list) - 1
                                        self.tournament.model_game_results(round_id)

                                        # Add round in the database
                                        self.database.update_database(self.tournament)

                                        # Show a message if tournament finished
                                        if len(self.tournament.round_list) == self.nb_of_rounds:
                                            self.view.show_message_tournament_finished()
                                            self.choice_sub_menu = 3

                                # Come back to the main menu
                                elif self.choice_sub_menu == 3:
                                    self.view.show_message_quit_sub_menu()

            # Manage players
            elif self.choice_main_menu == 3:
                self.choice_main_menu = 0

                # Check if the database is empty for the first time the application is used
                database_size = self.check_if_database_empty()

                # If the database empty, show message
                if database_size == 0:
                    self.view.show_message_create_tournament_first()

                # If the database not empty, check if the player table is empty
                else:
                    table_player_length = self.database.get_table_player_length()

                    # If table player length empty, show message
                    if table_player_length == 0:
                        self.viewed_player.show_message_create_player()

                    # If table player length not empty show manage players menu
                    else:
                        while self.choice_sub_menu != 3:
                            self.database = Database()
                            self.control_choice_sub_menu("manage_players")

                            # Update a player global ranking
                            if self.choice_sub_menu == 1:

                                self.controlled_player.control_update_player_global_ranking()

                            # Update a player tournament ranking by changing its points
                            elif self.choice_sub_menu == 2:
                                # Check if tournament in progress in the database
                                control_tournament_in_progress, name = self.database.find_tournament_in_progress()

                                # If no tournament in progress, show message
                                if control_tournament_in_progress is False:
                                    self.view.show_message_create_tournament_first()

                                # If tournament in progress, deserialize tournament in progress
                                else:
                                    self.tournament = self.controlled_new_tournament.continue_tournament(name)

                                    # If all players not in tournament, show message
                                    if len(self.tournament.player_list) < self.nb_of_players:
                                        self.view.show_message_add_players_first()

                                    # If all players in tournament, modify player points
                                    else:
                                        self.controlled_player.modify_player_points(self.tournament)

                            # Come back to the main menu
                            elif self.choice_sub_menu == 3:
                                self.view.show_message_quit_sub_menu()

            #  Make a report
            elif self.choice_main_menu == 4:
                self.database = Database()
                self.choice_main_menu = 0

                # Check if the database is empty for the first time the application is used
                database_size = self.check_if_database_empty()

                # If the database empty, show message
                if database_size == 0:
                    self.view.show_message_create_tournament_first()

                # If the database not empty, check if the player table is empty
                else:
                    table_player_length = self.database.get_table_player_length()

                    # If table player length empty, show message
                    if table_player_length == 0:
                        self.viewed_player.show_message_create_player()

                    # If table player length not empty show report menu
                    else:
                        while self.choice_sub_menu != 8:
                            self.control_choice_sub_menu("reports")

                            # Make a report with all players sorted in A-Z or by global ranking
                            if self.choice_sub_menu == 1 or self.choice_sub_menu == 2:
                                self.controlled_player.control_all_players_report(self.choice_sub_menu)

                            # Make a report with tournament players sorted in A-Z or by global ranking
                            elif self.choice_sub_menu == 3 or self.choice_sub_menu == 4:
                                self.control_tournament_report.control_tournament_players_report(self.choice_sub_menu)

                            # Make a report with all tournaments
                            elif self.choice_sub_menu == 5:
                                self.control_tournament_report.control_all_tournaments_report()

                            # Make a report with all rounds or all games of a tournament
                            elif self.choice_sub_menu == 6 or self.choice_sub_menu == 7:
                                self.control_tournament_report.control_rounds_games_report(self.choice_sub_menu)

                            # Come back to the main menu
                            elif self.choice_sub_menu == 8:
                                self.view.show_message_quit_sub_menu()
                                self.tournament.name = ""

            #  Quit the application
            elif self.choice_main_menu == 5:
                self.view.show_message_quit_application()
