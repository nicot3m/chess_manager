"""
module with class ViewPlayer
"""


class ViewPlayer:
    """
    Display of the player
    """

    def __init__(self):
        pass

    def prompt_player_data(self, field):
        if field == "last name" or field == "first name":
            print("Please write a", field, "of 10 characters maximum and w/o special characters or blank spaces")
        if field == "date of birth":
            print("Please write", field, "in JJMMAAAA format w/o special characters or blank spaces")
        if field == "gender":
            print("Please write", field, "as m for masculine or f for feminine")
        if field == "global ranking":
            print("Please write", field, "as an integer between 1000 and 3000. 3000 is much better than 1000.")
        if field == "points":
            print("Please write", field, "as a decimal number between 0 and 10.")
        message = "Type " + field + " of player: "
        data = input(message)
        return data

    def show_message_player_already_added(self):
        print("Player already added. Please add another player.")

    def show_message_create_player(self):
        print("You must create a player first!")

    def show_selectable_players(self, counter, player):
        if counter == 1:
            print("\nSelectable players")
            print("{0:<8} {1:<22} {2:<15} {3:<8} {4:<15}".format("ID", "Name", "date of birth",
                                                                 "Gender", "Global ranking"))
        print("{0:<8} {1:<22} {2:<15} {3:^8} {4:^15}".format(player.id, str(player), player.date_of_birth,
                                                             player.gender, player.global_ranking))

    def show_all_players_report(self, counter, player, field):
        if counter == 1:
            print("\nAll players sorted", field)
            print("{0:<8} {1:<22} {2:<15} {3:<8} {4:<15}".format("ID", "Name", "date of birth",
                                                                 "Gender", "Global ranking"))
        print("{0:<8} {1:<22} {2:<15} {3:^8} {4:^15}".format(player.id, str(player), player.date_of_birth,
                                                             player.gender, player.global_ranking))

    def show_tournament_players_report(self, counter, player, field):
        if counter == 1:
            print("\nTournament players sorted", field)
            print("{0:<8} {1:<22} {2:<15} {3:<20} {4:<8} {5:<15}".format("ID", "Name", "date of birth",
                                                                         "Tournament ranking", "Points",
                                                                         "Global ranking"))
        print("{0:<8} {1:<22} {2:<15} {3:^20} {4:^8} {5:^15}".format(player.id, str(player), player.date_of_birth,
                                                                     player.tournament_ranking, player.points,
                                                                     player.global_ranking))
