from AdaptedPlayer import *
import random

class Restaurant:

    """
        Resto class that gives us information about where the resto is located and how many 
        clients are there.
        In addition, it has a method to serve randomly one and only one customer. (gain)
    """

    counter = 0 # static counter for setting the id

    def __init__(self, coord : tuple, id=None):
        assert len(coord) == 2 
        assert int(coord[0]) > 0
        assert int(coord[1]) > 0

        self.__coord = coord

        if id is None:
            self.__id = Restaurant.counter 
            Restaurant.counter += 1
        else:
            assert int(id) >= 0
            self.__id = id # need to check if other resto have the same id

        self.__clients = [] # a list of AdaptedPlayer (clients that reached this resto)
        self.__served_client = None # which client to serve

    def reset(self):
        self.__clients = [] # a list of AdaptedPlayer (clients that reached this resto)
        self.__served_client = None # which client to serve

    def get_coord(self):
        return self.__coord

    def add_client(self, player : AdaptedPlayer):
        assert isinstance(player, AdaptedPlayer)

        self.__clients.append(player)

    def get_clients(self) -> list() :
        return self.__clients # list of clients present in this resto

    def random_serve(self, gain=1) -> AdaptedPlayer :
        """
            This method serves an AdaptedPlayer, add the gain to the player and returns the
            AdaptedPlayer object.
        """
        assert int(gain) > 0

        if len(self.__clients) > 0:
            if self.__served_client is None:
                self.__served_client = self.__clients[random.choice(range(len(self.__clients)))]
                self.__served_client.add_gain(gain)
                return self.__served_client
            else:
                msg = "This resto " + str(self.__id) + " already served a client"
                raise AlreadyServedException(msg)

    def get_served_client(self) -> AdaptedPlayer:
        return self.__served_client

    def __str__(self):
        return "Resto number " + str(self.__id) + " located at " + str(self.__coord)
  

class AlreadyServedException(Exception):
    pass