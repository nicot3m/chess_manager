"""
module with class ControlPlayer
"""

from operator import attrgetter


from view.viewer import View
from view.view_player import ViewPlayer
from model.model_player import Player
from model.model_database import Database


class ControlPlayer:
    """
    Controls the model of the player
    """

    def __init__(self):
        self.view = View()
        self.viewed_player = ViewPlayer()
        self.database = Database()
        self.all_player_list = []
        self.selectable_player_list = []
        self.selectable_player_id_list = []

    def control_player_data(self, field):
        check_data = False

        while check_data is False:
            data = (self.viewed_player.prompt_player_data(field))
            if field == "id":
                if data.isdigit() is True and int(data) in self.selectable_player_id_list:
                    data = int(data)
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            elif field == "last name" or field == "first name":
                data = data.strip()
                if data.isalpha() is True and 1 <= len(data) <= 10:
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            elif field == "date of birth":
                if (data.isdigit() is True and
                        len(data) == 8 and
                        1 <= int(data[0:2]) <= 31 and
                        1 <= int(data[2:4]) <= 12 and
                        1900 <= int(data[4:8]) <= 2100):
                    data = data[0:2]+"-"+data[2:4]+"-"+data[4:8]
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            if field == "gender":
                data = data.lower()
                if data == "m" or data == "f":
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            if field == "global ranking":
                if data.isdigit() is True and 1000 <= int(data) <= 3000:
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()

            if field == "points":
                try:
                    float(data)
                    check_data = True
                except ValueError:
                    check_data = False

                if check_data is True and 0 <= float(data) <= 10:
                    data = float(data)
                    check_data = True
                else:
                    self.view.show_message_data_not_valid()
                    check_data = False

        return data

    def create_player(self, tournament):
        self.database = Database()
        new_player = Player()
        new_player.id = self.database.get_table_player_length() + 1
        new_player.first_name = self.control_player_data("first name")
        new_player.last_name = self.control_player_data("last name")
        new_player.date_of_birth = self.control_player_data("date of birth")
        new_player.gender = self.control_player_data("gender")
        new_player.global_ranking = self.control_player_data("global ranking")
        new_player.points = 0

        # Check if new player not in player_list and not in database
        self.all_player_list = self.database.get_all_player_from_database()
        if new_player not in tournament.player_list and new_player not in self.all_player_list:
            check_new_player = True
        else:
            check_new_player = False
            new_player = ""
            self.viewed_player.show_message_player_already_added()
        return new_player, check_new_player

    def add_player_from_database(self, tournament):
        self.database = Database()
        # Get all player from database
        self.all_player_list = self.database.get_all_player_from_database()

        # Add player to selectable player list and id to selectable player id list
        self.selectable_player_list = []
        self.selectable_player_id_list = []
        for player in self.all_player_list:
            if player not in tournament.player_list:
                self.selectable_player_list.append(player)
                self.selectable_player_id_list.append(player.id)

        # If no player in selectable player list, show message
        if self.selectable_player_list == []:
            self.viewed_player.show_message_create_player()
            new_player = ""
            check_new_player = False

        else:
            # Show selectable players
            counter = 1
            for player in self.selectable_player_list:
                field = "in AZ"
                self.viewed_player.show_all_players_report(counter, player, field)
                counter += 1

            # Ask for player ID
            new_player_id = self.control_player_data("id")

            # Instantiate new player
            new_player = next((player for player in self.selectable_player_list if player.id == new_player_id), None)
            check_new_player = True

        return new_player, check_new_player

    def control_update_player_global_ranking(self):
        self.database = Database()
        # Get all player from database
        self.all_player_list = self.database.get_all_player_from_database()

        # Add id to selectable player id list and show all players in database
        self.selectable_player_id_list = []
        counter = 1
        field = "in AZ"
        for player in self.all_player_list:
            self.selectable_player_id_list.append(player.id)
            self.viewed_player.show_all_players_report(counter, player, field)
            counter += 1

        # Ask for player ID
        player_id = self.control_player_data("id")

        # Ask for global rankink
        global_ranking = self.control_player_data("global ranking")

        # Update player global ranking in the table player
        self.database.update_player_global_ranking(player_id, global_ranking)

    def modify_player_points(self, tournament):
        self.database = Database()
        # Add id to selectable player id list and show all players in database
        self.selectable_player_id_list = []
        counter = 1
        field = "by tournament ranking"
        for player in tournament.player_list:
            self.selectable_player_id_list.append(player.id)
            self.viewed_player.show_tournament_players_report(counter, player, field)
            counter += 1

        # Ask for player ID
        player_id = self.control_player_data("id")

        # Ask for player points
        points = self.control_player_data("points")

        # Modify player points
        player = next((player for player in tournament.player_list if player.id == player_id), None)
        player.points = points

        # Sort players
        tournament.sort_player_list()

        # Show tournament player ranking
        counter = 1
        for player in tournament.player_list:
            self.viewed_player.show_tournament_players_report(counter, player, field)
            counter += 1

        # Update the database
        self.database.update_database(tournament)

    def control_all_players_report(self, choice_sub_menu):
        self.database = Database()
        # Get players from database player list
        self.all_player_list = self.database.get_all_player_from_database()

        # Sort players by name
        if choice_sub_menu == 1:
            self.all_player_list = sorted(self.all_player_list, key=attrgetter("first_name"), reverse=False)
            field = "in AZ"

        # Sort players by global ranking
        elif choice_sub_menu == 2:
            self.all_player_list = sorted(self.all_player_list, key=attrgetter("global_ranking"), reverse=True)
            field = "by global ranking"

        # Show players
        counter = 1
        for player in self.all_player_list:
            self.viewed_player.show_all_players_report(counter, player, field)
            counter += 1
