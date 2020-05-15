from AdaptedPlayer import AdaptedPlayer
from Strategies import *

class Team:
    """
        Team of AdaptedPlayers, useful for comparing 2 or more strategies.
    """

    def __init__(self, *args, **kwargs):
        """
            The players in the team must have the same strategy.
        """
        if len(args) == 1: # passed the list of players to be in the team
            players = args[0]
            self.__init_from_players(players)

        elif len(args) == 2: # passed how many players to construct with which strategy
            number_of_players = args[0]
            strategy = args[1]
            self.__init_from_number(number_of_players, strategy)

    def __init_from_players(self, players : list()):
        assert len(players) > 0

        for player in players:
            assert isinstance(player, AdaptedPlayer)

        strategy = players[0].get_strategy()

        for i in range(1, len(players)):
            assert strategy.__str__() == players[i].get_strategy().__str__()

        self.__players = players
   
    def __init_from_number(self, n_players : int, strategy : Strategy):
        """
            Needs more code adaption to use this
        """
        raise NotImplementedError("This method needs more code adaption. Not implemented yet")

   
    def get_players(self) -> list():
        return self.__players

    def count(self) -> int:
        return len(self.__players)

    def set_strategy(self, strategy : Strategy):
        for player in self.__players:
            player.set_strategy(strategy)

    def get_strategy(self) -> Strategy:
        return self.__players[0].get_strategy()

    def __iter__(self):
        return iter(self.__players)

    def __str__(self):
        return "Team that has " + str(len(self.__players)) + " playing with " + \
                self.__players[0].get_strategy() if len(self.__players) > 0 else "Empty team"