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

    def play(self, x_days : int, no_rest=False): 
        # no_rest just for not slowing down the game when we reset it
        assert int(x_days) > 0
        assert isinstance(no_rest, bool)

        self.__x_days = x_days

        game = self.__game
        nbLignes, nbColonnes = game.spriteBuilder.rowsize, game.spriteBuilder.colsize
        goalStates = [o.get_rowcol() for o in game.layers['ramassable']]

        # constructing all players list
        players = []
        for team in self.__teams:
            players.extend(team.get_players())

        nbPlayers = len(players)
        iterations = self.__iterations_per_game
        
        # creating resto dictionnary to speed up the searching process (when affecting clients)
        restoDict = dict(zip(goalStates, self.__restaurants))
        restaurants = self.__restaurants
        self.__avg_of_occupied_resto = 0

        # creating team dictionnary, keys are players objects and value is the corresponding team
        # useful for statistics ( when serving a player, we need to know to which team he belongs to)
        team_dict = dict()
        for team in self.__teams:
            for player in team:
                team_dict[player] = team

        # gain per team dictionnary
        gain_per_team = dict(zip(self.__teams, [0] * len(self.__teams)))

        # playing the game x_days
        for day in range(x_days):
            # reset allowed positions that players can start in
            allowedStates = list(self.__original_allowedStates) # deep copy
            occupied_restos = 0 # how many restos have at least one client

            if day > 0:
                print("Reseting ...")
                # just to see that the game is restarting

                if not no_rest:
                    game.fps = 5
                
                # reseting the players, and placing them in the original positions
                i = 0
                for team in self.__teams:
                    for player in team:
                        player.reset()
                        pos = self.__initStates[i]
                        player.set_starting_position(pos)
                        game.mainiteration()
                        i += 1

                # reseting restos
                for resto in restaurants:
                    resto.reset()

            # return to the simulation speed
            self.set_speed(self.__speed)

            # randomly place the players
            for team in self.__teams:
                for player in team:
                    x,y = random.choice(allowedStates)
                    player.set_starting_position((x, y))

                    allowedStates.remove((x, y))

                    game.mainiteration()
                    
            # run the game for maximum x_iterations
            for i in range(iterations):
                # moving players sequentially 
                for j in range(nbPlayers): 

                    if players[j].reached_goal():
                        continue

                    else:
                        row, col = players[j].next_step(nbLignes, nbColonnes)
                        game.mainiteration()
                        
                        if players[j].reached_goal():
                            #o = players[j].ramasse(game.layers)
                            game.mainiteration()
                            # goalStates.remove((row,col)) # on enlève ce goalState de la liste

                            # add the current player to the correspong restaurant located at (row, col)
                            restoDict[(row, col)].add_client(players[j])
                            # print ("Le joueur ", j, " est à ", restoDict[(row, col)])

                            break

            for resto in restaurants:
                try:
                    resto.random_serve()
                    if len(resto.get_clients()) > 0:
                        occupied_restos += 1
                    # print(resto, end = ' ')
                    # print("has %d clients but served only the %s" %(len(resto.get_clients()),\
                    #                         resto.get_served_client()))
                except AlreadyServedException:
                    pass
                    # print(resto, end = ' ')
                    # print(" already served a client")

            for player in players:
                if player.ate():
                    gain_per_team[team_dict[player]] += player.get_gain()

            win_team = max(gain_per_team, key=gain_per_team.get)
            self.__avg_of_occupied_resto += occupied_restos / len(restaurants)
            print("Winning team on the round %d is %s" % (day+1, win_team))
            print("Occupied restos %d / %d " %(occupied_restos, len(restaurants)))

        self.__gain_per_team = gain_per_team
        self.__team_dict = team_dict
        self.__avg_of_occupied_resto /= x_days

    def get_teams(self):
        return self.__teams

    def get_all_players(self):
        players = []
        for team in self.__teams:
            players.extend(team.get_players())

        return players

    def summary(self):
        gain_per_team = self.__gain_per_team
        win_team = max(gain_per_team, key=gain_per_team.get)

        print("\nAfter playing for %d rounds, the winning team is %s with an overal gain of %d\n"
             %(self.__x_days, win_team, gain_per_team[win_team]))

        print("\nOther teams stats: ")
        print("Team                                      :          Gain\n")
        for team in self.__teams:
            if team == win_team:
                continue

            print(team, end='\t')
            print(gain_per_team[team])

        print("\n\nAvg gain per round for each team")
        for team in self.__teams:
            print(team, end=' :\t')
            print(gain_per_team[team] / self.__x_days)

        print("The mean of (means) occupied restos : ", self.__avg_of_occupied_resto)
