"""
module with class View
"""


class View:
    """
    Display of the menu
    """

    def __init__(self):
        pass

    def show_main_menu(self):
        print("\n*** Chess Manager ***\n".upper())
        print("Main menu\n".upper())
        print("1 - Create a tournament with players")
        print("2 - Begin or continue a tournament")
        print("3 - Manage players")
        print("4 - Make a report")
        print("5 - Quit the application")
        choice_main_menu = input("choice: ")
        return choice_main_menu

    def show_create_tournament_with_players_menu(self):
        print("\nCreate tournament with players menu\n".upper())
        print("1 - Create a tournament")
        print("2 - Add the players to the tournament")
        print("3 - Come back to the main menu")
        choice_sub_menu = input("choice: ")
        return choice_sub_menu

    def show_play_tournament_menu(self):
        print("\nPlay_tournament_menu\n".upper())
        print("1 - Create a new round and see the round games")
        print("2 - To enter the round results and see the player ranking")
        print("3 - To come back to the main menu")
        choice_sub_menu = input("choice: ")
        return choice_sub_menu

    def show_manage_players_menu(self):
        print("\nManage_players_menu\n".upper())
        print("1 - Update a player global ranking")
        print("2 - Update a player tournament ranking by changing its points")
        print("3 - Come back to the main menu")
        choice_sub_menu = input("choice: ")
        return choice_sub_menu

    def show_report_menu(self):
        print("\nReport menu\n".upper())
        print("1 - Make a report with all players sorted in A-Z")
        print("2 - Make a report with all players sorted in global ranking")
        print("3 - Make a report with all players of a tournament sorted in in A-Z")
        print("4 - Make a report with all players of a tournament sorted in tournament ranking")
        print("5 - Make a report with all tournaments")
        print("6 - Make a report with all rounds of a tournament")
        print("7 - Make a report with all games of a tournament")
        print("8 - Come back to the main menu")
        choice_sub_menu = input("choice: ")
        return choice_sub_menu

    def show_message_data_not_valid(self):
        print("Data not valid, please type another data")

    def show_message_create_tournament_first(self):
        print("You must create a tournament first!")

    def show_message_add_players_first(self):
        print("You must add the players to the tournament first!")

    def show_message_create_round_first(self):
        print("You must create the round first!")

    def show_message_enter_results_first(self):
        print("Enter the round results and see the player ranking first!")

    def show_message_tournament_already_in_progress(self, name):
        print("Tournament", name, "in progress. You must continue it first!")

    def show_message_all_players_already_added(self):
        print("All players already added to the tournament, continue the tournament!")

    def show_message_tournament_finished(self):
        print("Tournament is finished!")

    def show_message_quit_application(self):
        print("Bye!")

    def show_message_quit_sub_menu(self):
        print("Back to the main menu")
