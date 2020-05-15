from players import Player
import a_star

class AdaptedPlayer():
    """
        Creating an adaptedPlayer using composition and delegation
    """

    def __init__(self, player, starting_position, strategy, goalStates, wallStates, *args, **kwargs):
        from Strategies import Strategy
        assert isinstance(player, Player)

        self.__player = player
        self.__goalStates = goalStates
        self.__wallStates = wallStates
        self.set_starting_position(starting_position)
        self.set_strategy(strategy)

        self.__reached_target = False
        self.__gain = 0

    def reset(self):
        self.__reached_target = False
        self.__gain = 0

    def set_starting_position(self, starting_position):
        assert len(starting_position) == 2
        assert int(starting_position[0]) >= 0 
        assert int(starting_position[1]) >= 0

        self.__starting_position = starting_position
        self.__current_position = starting_position
        self.__player.set_rowcol(starting_position[0], starting_position[1])

    def set_strategy(self, strategy):
        from Strategies import Strategy
        assert isinstance(strategy, Strategy)

        self.__strategy = strategy

    def get_strategy(self):
        from Strategies import Strategy
        return self.__strategy

    def get_target(self):
        # return destination of this player 
        return self.__strategy.choose_resto(self.__current_position, distance=a_star.euc_dist)

    def next_step(self, nbLignes=20, nbColonnes=20) -> tuple:
        """
           Returns the next_step this player will take.
        """
        path = a_star.a_star(self.__current_position, self.get_target().get_coord(),
                             self.__wallStates, nbLignes, nbColonnes, hereustique=a_star.euc_dist)

        if len(path) > 0:
            self.__current_position = path[0]
            self.__player.set_rowcol(path[0][0], path[0][1])

            if self.__current_position == self.get_target().get_coord():
                self.__reached_target = True

            return path[0]

        return self.__current_position

    def reached_goal(self) -> bool:
        # Has this player reached his target ?
        return self.__reached_target

    def add_gain(self, g=1):
        assert int(g) > 0
        self.__gain += g

    def get_gain(self) -> int:
        return self.__gain

    def ate(self) -> bool:
        return self.__gain > 0

    def __str__(self):
        return "Player that started at " + str(self.__starting_position) \
               + " with " + str(self.__strategy)


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