# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain, product
import pygame
import glo

import random 
import numpy as np
import sys

import a_star
from Strategies import *
from AdaptedPlayer import *
from Restaurant import *
from Simulation import *
    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def main():

    iterations = 20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
      
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    restaurants = [Restaurant(coord) for coord in goalStates]
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    
    # on liste toutes les positions permises pour les joueurs #
    allowedStates = list(product(range(nbLignes), range(nbColonnes)))

    for x,y in set(chain(wallStates, goalStates)):
        allowedStates.remove((x,y))
    
    # creating one Strategy object  
    nearestStrategy = LOR(restaurants)

    # Converting players to AdaptedPlayers and creating teams
    for j in range(nbPlayers // 2):
        players[j] = AdaptedPlayer(players[j], initStates[j], nearestStrategy, goalStates, wallStates)
        game.mainiteration()

    team_a = Team(players[: nbPlayers // 2])

    for j in range(nbPlayers // 2, nbPlayers):
        players[j] = AdaptedPlayer(players[j], initStates[j], nearestStrategy, goalStates, wallStates)
        game.mainiteration()

    team_b = Team(players[nbPlayers // 2: ])
    
    teams = [team_a, team_b]
    
    # Creating a simulation that will play the game multiple times
    s = Simulation(game, restaurants, teams, allowedStates, initStates, iterations)
    s.set_speed(200)
    s.play(4)

    pygame.quit()

if __name__ == '__main__':
    main()