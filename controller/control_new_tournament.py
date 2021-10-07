"""
module with class ControlNewTournament
"""

from datetime import datetime


from view.viewer import View
from view.view_tournament import ViewTournament
from model.model_tournament import Tournament
from controller.control_player import ControlPlayer
from model.model_database import Database


class ControlNewTournament:
    """
    Controls the creation of a new  tournament
    """

    def __init__(self):
        self.controlled_player = ControlPlayer()
        self.view = View()
        self.viewed_tournament = ViewTournament()
        self.database = Database()
        self.choice_add_player = int()

    def control_tournament_data(self, field):
        check_data = False

        while check_data is False:
            new_tournament_data = (self.viewed_tournament.prompt_tournament_data(field))

            if field == "id":
                if new_tournament_data.isdigit() is True and 0 <= int(new_tournament_data) <= 99:
                    data = int(new_tournament_data)
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            elif field == "name":
                if new_tournament_data.isprintable() is True and 1 <= len(new_tournament_data) <= 15:
                    data = new_tournament_data
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            elif field == "location":
                new_tournament_data = new_tournament_data.strip()
                if new_tournament_data.isalpha() is True and 1 <= len(new_tournament_data) <= 15:
                    data = new_tournament_data
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            if field == "rating":
                if new_tournament_data.isdigit() is True and 1 <= int(new_tournament_data) <= 3:
                    if new_tournament_data == "1":
                        data = "Bullet"
                    elif new_tournament_data == "2":
                        data = "Blitz"
                    elif new_tournament_data == "3":
                        data = "Rapid"
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            elif field == "description":
                if new_tournament_data.isprintable() is True and 1 <= len(new_tournament_data) <= 50:
                    data = new_tournament_data
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

        return data

    def create_tournament(self):
        self.database = Database()
        tournament = Tournament()
        tournament.id = self.database.get_table_tournament_length() + 1
        tournament.name = self.control_tournament_data("name")
        tournament.location = self.control_tournament_data("location")
        tournament.rating = self.control_tournament_data("rating")
        tournament.description = self.control_tournament_data("description")
        tournament.tournament_in_progress = True
        start_date = datetime.now().date()
        tournament.start_date = start_date

        # Add tournament to the database
        self.database.add_tournament_in_database(tournament)

        return tournament

    def continue_tournament(self, name):
        self.database = Database()
        tournament = self.database.get_tournament_from_database(name)
        return tournament

    def control_choice_add_player(self):
        self.choice_add_player = False
        check_choice = False
        while check_choice is False:
            self.choice_add_player = self.viewed_tournament.show_add_player_menu()
            if self.choice_add_player.isdigit() is True and int(self.choice_add_player) in range(1, 4):
                check_choice = True
                self.choice_add_player = int(self.choice_add_player)
            else:
                self.view.show_message_data_not_valid()

    def add_players(self, nb_of_players, tournament):
        self.database = Database()
        self.choice_add_player = int()
        while self.choice_add_player != 3:

            # If all players not registered
            if len(tournament.player_list) < nb_of_players:
                self.control_choice_add_player()
                if self.choice_add_player == 1 or self.choice_add_player == 2:
                    # Add a player from the database
                    if self.choice_add_player == 1:
                        new_player, check_new_player = self.controlled_player.add_player_from_database(tournament)

                    # Or create a new player
                    elif self.choice_add_player == 2:
                        new_player, check_new_player = self.controlled_player.create_player(tournament)

                    if check_new_player is not False:
                        # Add player in tournament.player_list
                        tournament.player_list.append(new_player)

                        # Add player in database
                        self.database.add_player_in_database(tournament, new_player, self.choice_add_player)

                        # Show message new player registered
                        nb_of_player_added = len(tournament.player_list)
                        self.viewed_tournament.show_message_new_player_registered(new_player, nb_of_player_added)

                elif self.choice_add_player == 3:
                    self.viewed_tournament.show_message_quit_add_player_menu()

            # If all players registered
            else:
                self.view.show_message_all_players_already_added()
                self.choice_add_player = 3
