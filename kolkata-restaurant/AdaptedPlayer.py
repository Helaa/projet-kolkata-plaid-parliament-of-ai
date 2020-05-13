from players import Player
from Strategies import *
import a_star

class AdaptedPlayer():
    """
        Creating an adaptedPlayer using composition and delegation
    """

    def __init__(self, player, starting_position, strategy, goalStates, wallStates, *args, **kwargs):
        assert isinstance(player, Player)

        self.__player = player
        self.__set_starting_position(starting_position)
        self.__set_strategy(strategy)
        self.__goalStates = goalStates
        self.__wallStates = wallStates

        self.__reached_target = False

    def __set_starting_position(self, starting_position):
        assert len(starting_position) == 2
        assert int(starting_position[0]) >= 0 
        assert int(starting_position[1]) >= 0

        self.__starting_position = starting_position
        self.__current_position = starting_position
        self.__player.set_rowcol(starting_position[0], starting_position[1])

    def __set_strategy(self, strategy : Strategy):
        assert isinstance(strategy, Strategy)

        self.__strategy = strategy

    def get_strategy(self) -> Strategy:
        return self.__strategy

    def get_target(self) -> int:
        # return destination of this player ( which resto )
        return self.__strategy.choose_resto(self.__current_position, self.__goalStates, \
                                            distance=a_star.euc_dist)

    def next_step(self, nbLignes=20, nbColonnes=20) -> tuple:
        """
           Returns the next_step this player will take.
        """
        path = a_star.a_star(self.__current_position, self.__goalStates[self.get_target()],
                             self.__wallStates, nbLignes, nbColonnes, hereustique=a_star.euc_dist)

        if len(path) > 0:
            self.__current_position = path[0]
            self.__player.set_rowcol(path[0][0], path[0][1])

            if self.__current_position == self.__goalStates[self.get_target()]:
                self.__reached_target = True

            return path[0]

        return self.__current_position

    def reached_goal(self) -> bool:
        # Has this player reached his target ?
        return self.__reached_target


    ######################### DELEGATION #################################

    def gen_callbacks(self, incr, gDict, mask):
        return self.__player(incr, gDict, mask)


    def cherche_ramassable(self,layers,filtre = lambda x:True,verb=False):
        return self.__player(layers, filtre, verb)

    def ramasse(self,layers,verb=False):
        return self.__player(layers, verb)


    def depose(self,layers,filtre = lambda x:True,verb=False):
        return self.__player(layers, filtre, verb)

    def throw_rays(self,radian_angle_list,mask,layers,coords=None,show_rays=False):
        return self.__player(radian_angle_list, mask, layers, coords, show_rays)