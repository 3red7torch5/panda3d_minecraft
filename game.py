from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero
import random as rd
import numpy as np
from panda3d.core import WindowProperties
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land=Mapmanager()
        self.land.startNew()
        self.land.colorlist=[
        (0.4,0.4,0.4,1),
        (0.7,0.7,0.7,1),
        (0.6,0.6,0.6,1),
        (0.43,0.2,0,1),
        (0.2,1,0.2,1),
        (1,1,1,0),
        (1,1,1,0),
        (1,1,1,0),
        (1,1,1,0),
        (1,1,1,0),
        (1,1,1,0),
        (0.2,0.8,1,1),
        (0.2,0.8,1,1),
        (0.2,0.8,1,1)
        ]
        self.land.loadLand('land.txt')
        base.camLens.setFov(100)
        self.shotgundraw=loader.loadSfx('gun.ogg')
        self.shotgundraw.setVolume(0.2)
        self.free=loader.loadSfx('bag.ogg')
        self.free.setVolume(0.15)
        from mapmanager import playerpos
        self.hero=Hero(playerpos,self.land,'player.obj','space.png')
        self.music=loader.loadSfx('eek.ogg')
        self.axedraw=loader.loadSfx('axedraw.ogg')
        self.music.setLoop(True)
        self.music.setVolume(0.05)
        self.music.play()
        self.shotsound=loader.loadSfx('punch.ogg')
        self.shotsound.setVolume(0.3)
        self.breaksound=loader.loadSfx('break.ogg')
        self.breaksound.setVolume(0.3)
        self.coun=0
        self.fovc=100
    def generate_for_graph(self):
        c=0
        for x in range(0,50):
            for y in range(0,50):
                self.land.addBlock((x,y,round(np.cos(x**2+y**2-0.5))),(1,1,1,1))
            c+=1
            print(str(c))
game=Game()
wprop=WindowProperties()
wprop.setCursorHidden(True)
game.win.requestProperties(wprop)
mousec=False
map = base.win.get_keyboard_map()
w_button=map.get_mapped_button("w")
a_button=map.get_mapped_button("a")
s_button=map.get_mapped_button("s")
d_button=map.get_mapped_button("d")
tab_button=map.get_mapped_button("tab")
space_button=map.get_mapped_button("space")
ctrl_button=map.get_mapped_button("lcontrol")
#---
counter=0
while 1:
    #movement
    if base.mouseWatcherNode.is_button_down(w_button):
        game.hero.forward()
    if base.mouseWatcherNode.is_button_down(a_button):
        game.hero.left()
    if base.mouseWatcherNode.is_button_down(s_button):
        game.hero.backward()
    if base.mouseWatcherNode.is_button_down(d_button):
        game.hero.right()
    if base.mouseWatcherNode.is_button_down(space_button):
        game.hero.jump()
    if base.mouseWatcherNode.is_button_down(ctrl_button):
        game.hero.velocity_x*=1.1
        game.hero.velocity_y*=1.1
        game.hero.velocity_z*=1.1
    if base.hero.hero.getZ()<=0:
        base.hero.velocity_x=rd.randint(-2,2)
        base.hero.velocity_y=rd.randint(-2,2)
        base.hero.velocity_z=15
    base.hero.moveplayer()
    #---
    if counter>=180:
        counter=0
    else:
        counter+=1
    try:
        base.land.shtuka.updatescale(counter)
    except:
        pass
    base.hero.indiacator.update_speedometer()
    #---
    if base.coun>0:
        base.coun-=5
    else:
        base.coun=0
    base.hero.pic.setHpr(90-base.coun,90+base.coun,90+base.coun)
    #mouselook
    if not base.mouseWatcherNode.is_button_down(tab_button):
        wprop.setCursorHidden(True)
        base.win.requestProperties(wprop)
        if mousec==1:
            base.hero.checkmouse()
            mousec=0
        else:
            mousec+=1
    else:
        wprop.setCursorHidden(False)
        base.win.requestProperties(wprop)
    if base.fovc>100:
        base.fovc-=1
    base.camLens.setFov(base.fovc)
    if base.hero.speed>0.1:
        base.hero.weapon.setZ(np.sin(base.hero.hero.getX()+base.hero.hero.getY())/12+base.hero.wpzw)
        base.hero.pic.setZ(np.cos(base.hero.hero.getX()+base.hero.hero.getY())/12+base.hero.wpzp)
    base.hero.frame()
    taskMgr.step()