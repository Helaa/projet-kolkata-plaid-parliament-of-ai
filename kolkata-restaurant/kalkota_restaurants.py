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
from AdaptedPlayer import AdaptedPlayer
    
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

    #for arg in sys.argv:
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
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises#


    allowedStates = list(product(range(nbLignes), range(nbColonnes)))

    for x,y in set(chain(wallStates, goalStates)):
        allowedStates.remove((x,y))
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------
        
    posPlayers = initStates
    
    # Converting players to AdaptedPlayers 

    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j] = AdaptedPlayer(players[j], (x, y), NRS(nbRestaus), goalStates, wallStates)

        game.mainiteration()
        posPlayers[j]=(x,y)

    # for j in range(nbPlayers//2, nbPlayers):
    #     x,y = random.choice(allowedStates)
    #     players[j].set_starting_position((x,y))
    #     players[j].set_strategy(RandomStrategy(nbRestaus))

    #     players[j].set_rowcol(x,y)
    #     game.mainiteration()
    #     posPlayers[j]=(x,y)

    # #-------------------------------#
    # # chaque joueur choisit un restaurant
    # replaced by set_strategy() above

    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
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
                    print ("Le joueur ", j, " est à son restaurant.")
                    # goalStates.remove((row,col)) # on enlève ce goalState de la liste
                    break      
    

    for j in range(nbPlayers): 
        print("Player %d reached target ? %s" % (j, players[j].reached_goal()))
    pygame.quit()

if __name__ == '__main__':
    main()