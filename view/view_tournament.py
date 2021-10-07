"""
module with class ViewTournament
"""


class ViewTournament:
    """
    Display of the tournament
    """

    def __init__(self):
        pass

    def prompt_tournament_data(self, field):
        message = "Type " + field + " of tournament: "
        if field == "name":
            print("Please write a", field, "of 15 characters maximum")
        if field == "location":
            print("Please write a", field, "of 15 characters maximum and w/o special characters or blank spaces")
        if field == "description":
            print("Please write a", field, "of 50 characters maximum")
        if field == "rating":
            print("Type 1 for Bullet, 2 for for Blitz or 3 for Rapid")
        new_tournament_data = input(message)
        return new_tournament_data

    def show_message_new_player_registered(self, player, nb_of_player_added):
        print("New player", player.id, "is registered. There are now", nb_of_player_added, "registered.")

    def show_message_game_already_played(self, opponent1, opponent2):
        print("Attention, game ", opponent1.first_name, " vs ", opponent2.first_name, " has been already played")

    def show_round_games(self, opponent1, opponent2, counter, round_id):
        if counter == 0:
            print("\nThe games of round", round_id + 1, "are:")
        print(opponent1, "vs", opponent2)

    def prompt_game_result(self, opponent1, opponent2, counter, round_id):
        if counter == 0:
            print("\nGame result menu for round", round_id + 1)
            print("Score is 1 if first opponent wins, 2 if second opponent wins or 0.5 if draw")
        message = str(opponent1) + " vs " + str(opponent2) + ", type result 1, 2 or 0.5: "
        game_result = input(message)
        return game_result

    def show_add_player_menu(self):
        print("\nAdd player menu\n".upper())
        print("To add a player from the database, type 1")
        print("To create a new player, type 2")
        print("To quit, type 3")
        choice_add_player = input("choice: ")
        return choice_add_player

    def show_message_quit_add_player_menu(self):
        print("Back to the create tournament with players menu")

    def show_all_tournaments_report(self, counter, tournament):
        if tournament.tournament_in_progress is True:
            end_date = "in progress"
        else:
            end_date = tournament.end_date

        if counter == 1:
            print("\nAll tournaments")
            print("{0:<8} {1:<16} {2:<14} {3:<13} {4:<16} {5:<7} {6:<11} {7:<11} {8:<11}"
                  .format("Ranking", "Name", "Nb of players", "Nb of rounds", "Location",
                          "Rating", "Start", "Finish", "Description"))
        print("{0:<8} {1:16} {2:^14} {3:^13} {4:<16} {5:<7} {6:<11} {7:<11} {8:<11}"
              .format(counter, tournament.name, tournament.nb_of_players,
                      tournament.nb_of_rounds, tournament.location, tournament.rating,
                      tournament.start_date, end_date, tournament.description))

    def show_tournament_all_rounds_report(self, counter, tournament, chess_round):
        if chess_round.round_in_progress is True:
            end_date_time = "in progress"
        else:
            end_date_time = chess_round.end_date_time

        if counter == 1:
            print("\nAll rounds of tournaments", tournament.name)
            print("{0:<8} {1:<10} {2:<23} {3:<23}".format("Round", "Name", "Start", "Finish"))
        print("{0:<8} {1:<10} {2:<23} {3:<23}".format(chess_round.id, chess_round.name,
                                                      chess_round.start_date_time, end_date_time))

    def show_tournament_all_games_report(self, counter, tournament, chess_round, game):
        if chess_round.round_in_progress is True:
            result = "in progress"
        else:
            result = str(game.score1) + "-" + str(game.score2)

        if counter == 1:
            print("\nAll games of tournament", tournament.name)
            print("{0:<8} {1:<12} {2:<22} {3:^12} {4:<22}".format("Game", "Round name", "Opponent 1",
                                                                  "Result", "Opponent 2"))

        print("{0:<8} {1:<12} {2:<22} {3:^12} {4:<22}".format(counter, chess_round.name, str(game.opponent1),
                                                              result, str(game.opponent2)))
