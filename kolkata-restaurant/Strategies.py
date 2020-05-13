from abc import ABC, abstractmethod
from random import randrange

import a_star

class Strategy(ABC):
    """
        Base class of strategies
    """

    def __init__(self, resto : int):
        assert int(resto) > 0
        self.__number_of_resto = resto

    @property
    def number_of_resto(self) -> int:
        return self.__number_of_resto

    @number_of_resto.setter
    def number_of_resto(self, resto : int):
        assert int(resto) > 0

        self.__number_of_resto = resto

    @abstractmethod
    # This signature is useless for the first 2 strategies, but we did it this way to generalize
    # the way we call it for the sake of simplicity.
    def choose_resto(self, current_player_pos=None, goalStates=None, distance=a_star.euc_dist) -> int:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

class RandomStrategy(Strategy):
    def __init__(self, resto : int):
        super().__init__(resto)

    def choose_resto(self, current_player_pos=None, goalStates=None, distance=a_star.euc_dist) -> int:
        return randrange(0, self.number_of_resto) # choice in [0, number_of_resto[

    def __str__(self) -> str:
        return "Random Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self.number_of_resto)

class StubbornStrategy(Strategy):
    def __init__(self, resto : int):
        super().__init__(resto)
        self.__chosed_resto = randrange(0, self.number_of_resto) # choice in [0, number_of_resto[

    def choose_resto(self, current_player_pos=None, goalStates=None, distance=a_star.euc_dist) -> int:
        return self.__chosed_resto

    def __str__(self) -> str:
        return "Stubborn Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self.number_of_resto)

class NRS(Strategy):
    # Nearest Resto Strategy
    def __init__(self, resto : int):
        super().__init__(resto)
        self.__chosed_resto = randrange(0, self.number_of_resto) # choice in [0, number_of_resto[

    def choose_resto(self, current_player_pos, goalStates, distance=a_star.euc_dist) -> int:
        """
            @params:
                current_player_pos: player's coord in the map ( list or tuple )
                goalStates: list of all restos coords (list of tuples or lists)

            returns the nearest resto to the player (using distance function to get the nearest one)
        """
        assert len(current_player_pos) == 2
        assert len(goalStates) > 0
        # need to check each coord, but let's just assume that all is well for now.

        distances = [distance(current_player_pos, resto_pos) for resto_pos in goalStates]

        return distances.index(min(distances))

    def __str__(self) -> str:
        return "Nearest Resto Strategy"
    
    def __repr__(self) -> str:
        return self.__str__() + " Number of Restos is " + str(self.number_of_resto)

class LOR(Strategy):
    #Less occupation Res
    def __init__(self, resto: int):
        super().__init__(resto)
        self.__chosed_resto = randrange(0, self.number_of_resto)  # choice in [0, number_of_resto[

    def choose_resto(self, current_player_pos, goalStates, distance=a_star.euc_dist) -> int:
        """
            @params:
                current_player_pos: player's coord in the map ( list or tuple )
                goalStates: list of all restos coords (list of tuples or lists)

            returns the less occupation restaurant
        """
        assert len(current_player_pos) == 2
        assert len(goalStates) > 0
        # need to check each coord, but let's just assume that all is well for now.



        return

    def __str__(self) -> str:
        return "Less Occupation Resto Strategy"


