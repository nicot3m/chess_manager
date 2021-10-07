"""
module with class Player
"""


class Player:
    """
    Contains the model of the player
    """

    def __init__(self):
        self.id = int()
        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.global_ranking = ""
        self.tournament_ranking = ""
        self.points = float()

    def __hash__(self):
        return hash((self.last_name, self.first_name, self.date_of_birth))

    def __eq__(self, other_player):
        return (self.last_name, self.first_name, self.date_of_birth) == \
               (other_player.last_name, other_player.first_name, other_player.date_of_birth)

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)

    # def serialize_player(self, player)
    def serialize_player(self):
        serialized_player = {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "dateOfBirth": self.date_of_birth,
            "gender": self.gender,
            "globalRanking": self.global_ranking,
            "tournamentRanking": self.tournament_ranking,
            "points": self.points
        }
        return serialized_player
