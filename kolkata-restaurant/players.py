import pygame
from sprite import MySprite,MovingSprite,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random
from math import pi,sqrt,cos,sin,floor
import rayon
import polygons
import glo
try:
    from pygame.gfxdraw import aacircle,filled_circle
    def circle(surf,c,coord,r,w):
        x,y = coord
        x,y,r = int(x),int(y),int(r)
        filled_circle(surf,x,y,r,(20,20,60))
        aacircle(surf,x,y,r,c)
        aacircle(surf,x,y,r-1,c)
except:
    from pygame.draw import circle

from Strategies import *
import a_star

class Player(MovingSprite):
    """ cette classe modelise un sprite controlable par l'utilisateur
        soit au tile pres, soit au pixel pres
        soit au clavier directement, soit par instructions
    """
    def __init__(self, *args,**kwargs):
        MovingSprite.__init__(self,*args,**kwargs)
        self.inventory = pygame.sprite.Group()
        
        self.__called_start_method = False
        self.__called_strategy_method = False
        self.__reached_target = False

    def gen_callbacks(self,incr,gDict,mask):
        transl = self.translate_sprite
        return {
            pygame.K_LEFT:  partial(transl,x= -incr , y=0, a=0),
            pygame.K_RIGHT: partial(transl,x=  incr , y=0, a=0),
            pygame.K_UP:    partial(transl,x=  0    , y= -incr, a=0),
            pygame.K_DOWN:  partial(transl,x=  0    , y=  incr, a=0),
            pygame.K_c:     partial(self.cherche_ramassable,layers=gDict,verb=True),
            pygame.K_r:     partial(self.ramasse,layers=gDict,verb=True),
            pygame.K_d:     partial(self.depose,layers=gDict,verb=True),
            pygame.K_t:     partial(self.throw_ray,radian_angle=None,mask=mask,layers=gDict)
        }


    def cherche_ramassable(self,layers,filtre = lambda x:True,verb=False):
        for obj in layers["ramassable"]:
            if filtre(obj):
                if self.mask.overlap(obj.mask,(obj.rect.x - self.rect.x,obj.rect.y - self.rect.y)):
                    if verb: print ("j'en ai trouve un")
                    return obj
        if verb: print ("rien a ramasser")
        return None

    def ramasse(self,layers,verb=False):
        o = self.cherche_ramassable(layers)
        if o is None:
            if verb: print ("rien a ramasser")
            return None
        self.inventory.add( o )
        o.remove( layers.values() )
        return o


    def depose(self,layers,filtre = lambda x:True,verb=False):
        # remove object from existing groups displayed on the screen
        candidats = [o for o in self.inventory if filtre(o)]

        if not candidats:
            if verb: print ("rien a deposer")
            return None
        obj = candidats[0]
        self.inventory.remove( obj )
        obj.translate_sprite(self.x,self.y,0,False)
        layers['ramassable'].add( obj )
        return obj

    def throw_rays(self,radian_angle_list,mask,layers,coords=None,show_rays=False):
        mask.erase_sprite( self )
        cx,cy = coords if coords else self.get_centroid()
        w,h = mask.mask.get_size()
        r = [rayon.rayon(mask.mask,cx,cy,a,w,h) for a in radian_angle_list]
        mask.draw_sprite( self )
        if layers and show_rays:
            for h in r:
                layers["eye_candy"].add( DrawOnceSprite( pygame.draw.line , [(255,0,0),(cx,cy),h,4] ) )
        return r

    
    def set_starting_position(self, starting_position):
        assert len(starting_position) == 2
        assert int(starting_position[0]) >= 0 
        assert int(starting_position[1]) >= 0
        self.__starting_position = starting_position
        self.__current_position = starting_position

        self.__called_start_method = True

    def set_strategy(self, strategy : Strategy):
        assert isinstance(strategy, Strategy)

        self.__strategy = strategy
        self.__called_strategy_method = True

    def get_strategy(self) -> Strategy:
        return self.__strategy

    def get_target(self, goalStates=None):
        # return destination of this player ( which resto )
        if isinstance(self.__strategy, NRS):
            if not self.__called_start_method:
                raise SystemExit("This player needs to know his starting pos to use this strategy")

            if goalStates is None:
                raise SystemExit("This player needs to know all coords of restos to choose the nearest one")

            return self.__strategy.choose_resto(self.__current_position, goalStates)

        return self.__strategy.choose_resto()

    def next_step(self, goal_states, wall_states, nbLignes=20, nbColonnes=20):
        """
            @params:
                goal_states: list or tuple of coords of restos
                wall_states: list or tuple of coords of walls
        """
        if not self.__called_start_method or not self.__called_strategy_method:
            raise SystemExit("Player need to have a starting position and a strategy.")

        assert len(goal_states) > 0
        assert len(wall_states) > 0

        if isinstance(self.__strategy, NRS):
            path = a_star.a_star(self.__current_position, goal_states[self.get_target(goal_states)], wall_states, \
                            nbLignes, nbColonnes, hereustique=a_star.euc_dist)
        else:
            path = a_star.a_star(self.__current_position, goal_states[self.get_target()], wall_states, \
                            nbLignes, nbColonnes, hereustique=a_star.euc_dist)

        if len(path) > 0:
            self.__current_position = path[0]
            self.set_rowcol(path[0][0], path[0][1])

            if self.__current_position == goal_states[self.get_target()]:
                self.__reached_target = True

            return path[0]

        return self.__current_position

    def reached_goal(self) -> bool:
        # Has this player reached his target ?
        return self.__reached_target
        
class Turtle(Player):
    def __init__(self,layername,x,y,w,h):
        self.taille_geometrique, self.penwidth = 22, 1
        Player.__init__(self,layername,tileid=None,x=x,y=y,imglist=self.build_Turtle_list_images(w,h))

    def build_Turtle_list_images(self,w,h):
        """ cree 360 images de tortues (une par degre)"""
        imglist = [pygame.Surface((w,h)).convert() for a in range(360)]
        for a,img in zip(range(360),imglist):
            img.set_colorkey( (0,0,0) )
            img.fill((0,0,0))
            circle(img, glo.WHITE, (w/2,h/2), self.taille_geometrique/2 - self.penwidth,self.penwidth)
            polygons.draw_arrow(img,w/2,h/2,a * pi/180,r=self.taille_geometrique-14,clr=glo.WHITE)
            #pygame.gfxdraw.aacircle(self.image, w/2,h/2, self.taille_geometrique/2 - self.penwidth,glo.WHITE)
        return imglist
