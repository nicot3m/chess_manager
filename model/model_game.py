"""
module with class Game
"""


class Game:
    """
    Contains the model of the game
    """

    def __init__(self, opponent1, opponent2):
        # instance of opponent1
        self.opponent1 = opponent1
        # opponent1 score
        self.score1 = float()
        # instance of opponent2
        self.opponent2 = opponent2
        # opponent2 score
        self.score2 = float()
        # list withs opponent1 + opponent1 score
        self.opponent_list1 = []
        # list withs opponent2 + opponent2 score
        self.opponent_list2 = []
        # tuple with opponent_list1 and opponent_list
        self.game_tuple = ()

    def create_game_tuple(self):
        self.opponent_list1.append(self.opponent1)
        self.score1 = 0
        self.opponent_list1.append(self.score1)
        self.opponent_list2.append(self.opponent2)
        self.score2 = 0
        self.opponent_list2.append(self.score2)
        self.game_tuple = (self.opponent_list1, self.opponent_list2)
        return self.game_tuple

    def serialize_game_tuple(self):
        # serialized_opponent1 = self.opponent1.serialize_player(self.opponent1)
        serialized_opponent1 = self.opponent1.serialize_player()
        serialized_opponent_list1 = [serialized_opponent1, self.score1]
        # serialized_opponent2 = self.opponent2.serialize_player(self.opponent2)
        serialized_opponent2 = self.opponent2.serialize_player()
        serialized_opponent_list2 = [serialized_opponent2, self.score2]
        serialized_game_tuple = (serialized_opponent_list1, serialized_opponent_list2)
        return serialized_game_tuple
