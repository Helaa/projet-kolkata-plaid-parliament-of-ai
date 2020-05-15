from gameclass import Game
from Team import Team
from Restaurant import *

class Simulation:
    """
        Simulation class responsable for playing a game for x_days and returns the stats.
    """

    def __init__(self, game : Game, restaurants : list(), teams : list(),\
                 allowedStates : list(), initStates : list(), iterations_per_game : int):
        assert isinstance(game, Game)
        
        assert len(teams) > 0
        for team in teams:
            assert isinstance(team, Team)

        assert len(restaurants) > 0
        for resto in restaurants:
            assert isinstance(resto, Restaurant)

        assert len(allowedStates) > 0
        for coord in allowedStates:
            assert len(coord) == 2

        # calculating how many players are passed
        h_many_players = 0
        for team in teams:
            h_many_players += len(team.get_players())

        # making sure that we have init position of all the players
        assert len(initStates) == h_many_players 

        assert int(iterations_per_game) > 0

        self.__game = game
        self.__restaurants = restaurants
        self.__teams = teams
        self.__initStates = initStates
        self.__original_allowedStates = allowedStates
        self.__iterations_per_game = iterations_per_game
        self.__speed = 5
        self.set_speed()

    def set_speed(self, fps=5):
        assert int(fps) > 0
        self.__game.fps = fps
        self.__speed = fps

    def play(self, x_days : int):
        assert int(x_days) > 0

        game = self.__game
        goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
        restoDict = dict(zip(goalStates, self.__restaurants))
        restaurants = self.__restaurants

        players = []
        for team in self.__teams:
            players.extend(team.get_players())

        nbPlayers = len(players)
        iterations = self.__iterations_per_game

        for day in range(x_days):
            allowedStates = self.__original_allowedStates

            if day > 0:
                print("Reseting ...")
                game.fps = 5
                
                i = 0
                for team in self.__teams:
                    for player in team:
                        player.reset()
                        pos = self.__initStates[i]
                        player.set_starting_position(pos)
                        game.mainiteration()
                        i += 1

            self.set_speed(self.__speed)

            # In the beginning, randomly place the players
            for team in self.__teams:
                for player in team:
                    x,y = random.choice(allowedStates)
                    player.set_starting_position((x, y))

                    allowedStates.remove((x, y))

                    game.mainiteration()
                    
            # run the game for maximum x_iterations
            for i in range(iterations):
                for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement

                    if players[j].reached_goal():
                        continue

                    else:
                        #print("Player %d (strategy = %s) is going to %d" % (j, players[j].get_strategy(),players[j].get_target()))
                        row, col = players[j].next_step() # nbLignes = nbColonnes = 20
                        game.mainiteration()
                        
                        if players[j].reached_goal():
                            #o = players[j].ramasse(game.layers)
                            game.mainiteration()
                            # goalStates.remove((row,col)) # on enlève ce goalState de la liste

                            # add the current player to the correspong restaurant located at (row, col)
                            restoDict[(row, col)].add_client(players[j])
                            print ("Le joueur ", j, " est à ", restoDict[(row, col)])

                            break

            for resto in restaurants:
                try:
                    resto.random_serve()
                    print(resto, end = ' ')
                    print("has %d clients but served only the %s" %(len(resto.get_clients()),\
                                            resto.get_served_client()))
                except AlreadyServedException:
                    print(resto, end = ' ')
                    print(" already served a client")

            for player in players:
                if player.ate():
                    print(player, end = ' ')
                    print(" has eaten ")

            for resto in restaurants:
                resto.reset()

            for player in players:
                if player.ate():
                    print(player, end = ' ')
                    print(" has eaten ")