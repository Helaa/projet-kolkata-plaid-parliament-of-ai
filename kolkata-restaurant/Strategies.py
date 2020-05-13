from abc import ABC, abstractmethod
from random import randrange

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
    def choose_resto(self) -> int:
        ...

class RandomStrategy(Strategy):
    def __init__(self, resto : int):
        super().__init__(resto)

    def choose_resto(self) -> int:
        return randrange(0, self.number_of_resto) # choice in [0, number_of_resto[

class StubbornStrategy(Strategy):
    def __init__(self, resto : int):
        super().__init__(resto)
        self.__chosed_resto = randrange(0, self.number_of_resto) # choice in [0, number_of_resto[

    def choose_resto(self) -> int:
        return self.__chosed_resto

