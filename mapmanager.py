from direct.showbase.ShowBase import ShowBase
from random import random
from datetime import datetime
from panda3d.core import NodePath,LineSegs,LVecBase3f
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import numpy as np
import pickle
color=(0.7,0.75,0.9,1)
color0=(0,0.28,0.5,1)
loadedmodels=['block.egg']
loadedtextures=['block.png']
playerpos=(0,0,0)
class Mapmanager():
    def __init__(self):
        #C:/Users/%USERNAME%/AppData/Local/Panda3D-1.10
        self.blockmodel='block.egg'
        self.texture='block.png'
        self.lines=LineSegs()
        self.bar=DirectWaitBar(text="",pos=(0,0,0),barTexture='bar.png',barColor=(0.4,0.3,1,1),barBorderWidth=(2,2))
        self.music=base.loader.loadSfx('aroundtheworld.ogg')
        self.music.setVolume(0.01)
        self.music.setLoop(True)
        self.image=OnscreenImage(image='fon.jpg',pos=(0,0,1),scale=5)
        self.lnodelist=[]
    def save_world(self):
        blocks=self.land.getChildren()
        with open('save.dat','wb') as f:
            pickle.dump(len(blocks),f)
            for i in blocks:
                x,y,z=i.getPos()
                r,g,b,_=i.getColor()
                pickle.dump((x,y,z,r,g,b),f)
    def load_world(self):
        #Макс сделай тут потом анимацию какую-нибудь, а то уныло
        print(len(self.land.getChildren()))
        self.clear()
        print(len(self.land.getChildren()))
        with open('save.dat','rb') as f:
            for _ in range(pickle.load(f)):
                x,y,z,r,g,b=pickle.load(f)
                self.addBlock((x,y,z),(r,g,b,1))
        print(len(self.land.getChildren()))
    def drawline(self,startpos,endpos,thcknss=1):
        self.lines=LineSegs()
        self.lines.setThickness(thcknss)
        self.lines.setColor((0.3,0.1,0.5,1))
        self.lines.moveTo(LVecBase3f(startpos))
        self.lines.drawTo(LVecBase3f(endpos))
        node=self.lines.create()
        self.linenode = NodePath(node)
        self.linenode.reparentTo(render)
        self.lnodelist.append(self.linenode)
    def startNew(self):
        self.land=render.attachNewNode("Land")
    def addBlock(self,position,color):
        self.block=loader.loadModel(self.blockmodel)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(color)
        self.block.reparentTo(self.land)
        self.block.setTag('position',str(position))
    def addCustomModel(self,position,color,filename,texture,scale_x,scale_y,scale_z):
        global loadedmodels
        global loadedtextures
        if not filename in loadedmodels:
            self.bar['text']=filename.split('/')[-1]
            loadedmodels.append(filename)
        try:
            self.model=loader.loadModel(filename)
        except:
            print(f'FAILED TO LOAD MODEL "{filename}"')
        finally:
            self.model.setHpr(90,90,-90)
            self.model.setPos(position)
            self.model.setColor(color)
            self.model.setScale(scale_x,scale_y,scale_z)
            self.model.reparentTo(self.land)
        if not texture in loadedtextures:
            self.bar['text']=texture.split('/')[-1]
            loadedtextures.append(texture)
        try:
            self.model.setTexture(loader.loadTexture(texture))
        except:
            print(f'FAILED TO LOAD TEXTURE "{texture}"')
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def loadLand(self,filename):
        self.music.play()
        global loadedmodels
        global loadedtextures
        global playerpos
        self.clear()
        self.bar['text']=filename
        self.bar['value']=0
        start_time=datetime.now()
        with open(filename) as karta:
            lines=karta.readlines()
            y_pos,x_pos=0,0
            for strokaid,stroka in enumerate(lines):
                y_pos=strokaid
                strokalist=stroka.split(' ')
                for cifraid,cimvol in enumerate(strokalist):
                    x_pos=-cifraid
                    cifra=cimvol.split('|')
                    colorid=int(cifra[0])
                    if int(cifra[0])>=len(self.colorlist):
                        for _ in range(int(cifra[0])//len(self.colorlist)):
                            colorid-=len(self.colorlist)
                    self.addBlock((x_pos,y_pos,int(cifra[0])),self.colorlist[int(colorid)])
                    if cifra[-1]=='P':
                        playerpos=(x_pos,y_pos,float(cifra[0]))
                        self.bar['text']='placed Player'
                self.bar['value']=(strokaid+1)/len(lines)*100
                self.image['r']+=3
                taskMgr.step()
        self.bar.destroy()
        self.image.destroy()
        try:
            self.music.stop()
        except:
            pass
class DynamicObject():
    def __init__(self,position,color,filename,texture):
        try:
            self.model=loader.loadModel(filename)
        except:
            print(f'FAILED TO LOAD MODEL "{filename}"')
        finally:
            self.model.setPos(position)
            self.model.setHpr(0,90,0)
            self.model.setColor(color)
            self.model.reparentTo(base.land.land)
        try:
            self.model.setTexture(loader.loadTexture(texture))
        except:
            print(f'FAILED TO LOAD TEXTURE "{texture}"')
    def updatescale(self,counter):
        x0,y0=self.model.getPos()[0],self.model.getPos()[1]
        x1,y1=base.hero.hero.getPos()[0],base.hero.hero.getPos()[1]
        distance=np.sqrt(((x0-x1)**2)+((y0-y1)**2))
        self.model.setScale(np.sin(np.cos(counter/30))*10)