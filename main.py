"""
main(version 1.0.0)
Auteur: nicot3m
Date: 15/03/2021
This application is a chess tournament manager.
Create your tournament, add the players and the application will automatically.
display the games of the round to play.
After you write the results, the application will show the ranking of the players.
The application data are saved in a local file database.json in directory database (not to be deleted).
It uses tinydb.

Input:
    from user and from database.json
Output:
    database.json
"""

from controller.controller import Controller


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
