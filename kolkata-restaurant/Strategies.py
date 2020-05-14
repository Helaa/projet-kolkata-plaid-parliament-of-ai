from abc import ABC, abstractmethod
from random import randrange
import math
import numpy as np
from Restaurant import *
import a_star

class Strategy(ABC):
    """
        Base class of strategies
    """

    def __init__(self, restos : list()):
        # restos : list of Restaurant
        assert len(restos) > 0
        for resto in restos:
            assert isinstance(resto, Restaurant)

        self._restos = restos
        self._number_of_resto = len(restos)
        self._goalStates = [resto.get_coord() for resto in restos] # coords of all the restos
        print(self._goalStates)

    @property
    def number_of_resto(self) -> int:
        return self._number_of_resto

    @abstractmethod
    # This signature is useless for the first 2 strategies, but we did it this way to generalize
    # the way we call it for the sake of simplicity.
    def choose_resto(self, current_player_pos=None, distance=a_star.euc_dist) -> Restaurant:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

class RandomStrategy(Strategy):
    def __init__(self, restos : list()):
        super().__init__(restos)

    def choose_resto(self, current_player_pos=None, distance=a_star.euc_dist) -> Restaurant:
        return self._restos[randrange(0, self._number_of_resto)] # choice in [0, number_of_resto[

    def __str__(self) -> str:
        return "Random Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self._number_of_resto)

class StubbornStrategy(Strategy):
    def __init__(self, restos : list()):
        super().__init__(restos)
        self._chosed_resto = self._restos[randrange(0, self._number_of_resto)] # choice in [0, number_of_resto[

    def choose_resto(self, current_player_pos=None, distance=a_star.euc_dist) -> Restaurant:
        return self._chosed_resto

    def __str__(self) -> str:
        return "Stubborn Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self._number_of_resto)

class NRS(Strategy):
    # Nearest Resto Strategy
    def __init__(self, restos : list()):
        super().__init__(restos)

    def choose_resto(self, current_player_pos, distance=a_star.euc_dist) -> Restaurant:
        """
            @params:
                current_player_pos: player's coord in the map ( list or tuple )

            returns the nearest resto to the player (using distance function to get the nearest one)
        """
        assert len(current_player_pos) == 2
        # need to check each coord, but let's just assume that all is well for now.
        
        distances = [distance(current_player_pos, resto_pos) for resto_pos in self._goalStates]
        nearest_dist_index = distances.index(min(distances))
        nearest_resto = self._restos[nearest_dist_index]

        return nearest_resto

    def __str__(self) -> str:
        return "Nearest Resto Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self._number_of_resto)

class LOR(NRS):
    """
        Hybrid strategy: first get to the nearest resto, then switch to the least occupied
        restos
    """
    def __init__(self, restos : list()):
        super().__init__(restos)

    def choose_resto(self, current_player_pos, distance=a_star.euc_dist) -> Restaurant:
        """
            @params:
                current_player_pos: player's coord in the map ( list or tuple )
                goalStates: list of all restos coords (list of tuples or lists)

            returns the less occupied restaurant
        """
        assert len(current_player_pos) == 2

        occupations = [resto.get_clients() for resto in self._restos]

        if not any(occupations): # all restos are empty
            return super().choose_resto(current_player_pos, distance)
        else:
            # Look for the nearest empty resto
            distances = [distance(current_player_pos, resto_pos) for resto_pos in self._goalStates]

            for dist in sorted(distances): # nearest
                if len(self._restos[distances.index(dist)].get_clients()) == 0: # empty
                    return self._restos[distances.index(dist)]

        # if all are full, might as well try the nearst resto
        return super().choose_resto(current_player_pos, distance)

    def __str__(self) -> str:
        return "Less Occupation Resto Strategy"

    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self._number_of_resto)
""""
class StocasticChoice(Strategy):

    def choose_resto(self, current_player_pos=None, distance=a_star.euc_dist) -> Restaurant:
        z=0
        for i in range(self._number_of_resto):
            # Z is the factor of choice in Stochastic agent
            z += math.exp(-occupation[i])

        p = []
        for i in range (self._number_of_resto):
            p.append(math.exp(-occupation[i])/z)


        return np.random.choice(range(n), p=p)
"""