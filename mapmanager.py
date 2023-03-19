from direct.showbase.ShowBase import ShowBase
from random import random
from datetime import datetime
from panda3d.core import NodePath,LineSegs,LVecBase3f
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import numpy as np
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
        self.textModels=OnscreenText(text='',pos=(0,-0.5),scale=0.05)
        self.textTextures=OnscreenText(text='',pos=(0,-0.6),scale=0.05)
        self.music=base.loader.loadSfx('aroundtheworld.ogg')
        self.music.setVolume(0.01)
        self.music.setLoop(True)
        self.image=OnscreenImage(image='fon.jpg',pos=(0,0,1),scale=5)
        self.lnodelist=[]
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
                    for cifra in cimvol.split('|'):
                        try:
                            colorid=int(cifra)
                            if int(cifra)>=len(self.colorlist):
                                for _ in range(int(cifra)//len(self.colorlist)):
                                    colorid-=len(self.colorlist)
                            self.addBlock((x_pos,y_pos,int(cifra)),self.colorlist[int(colorid)])
                        except:
                            colorid=int(round(float(cifra[:-1])))-1
                            if colorid>=len(self.colorlist):
                                for _ in range(colorid//len(self.colorlist)):
                                    colorid-=len(self.colorlist)
                            if cifra[-1]=='P':
                                playerpos=(x_pos,y_pos,float(cifra[:-1]))
                                self.bar['text']='placed Player'
                            elif cifra[-1]=='A':
                                self.addCustomModel((x_pos,y_pos,float(cifra[:-1])),(0.6,0.6,0.8,1),'strangeobject.obj','block.png',1.5,2,1.5)
                            elif cifra[-1]=='B':
                                self.addCustomModel((x_pos,y_pos,float(cifra[:-1])),(0.5,0.5,0.5,1),'bomb.obj','bomb.png',3,3,3)
                            elif cifra[-1]=='C':
                                self.addCustomModel((x_pos,y_pos,float(cifra[:-1])),(0.5,0.5,0.5,1),'shotgun.obj','space.png',1.5,1.5,1.5)
                            elif cifra[-1]=='S':
                                self.addCustomModel((x_pos,y_pos,float(cifra[:-1])),(0.5,0.7,0.5,1),'smiley','block.png',1,1,1)
                            elif cifra[-1]=='H':
                                self.addCustomModel((x_pos,y_pos,float(cifra[:-1])),(0.5,0.7,0.5,1),'block.egg','block.png',0.5,1,0.5)
                            elif cifra[-1]=='D':
                                self.shtuka=DynamicObject((x_pos,y_pos,float(cifra[:-1])),(0.2,0.2,0.2,1),'bomb.obj','space.png')
                            else:
                                print(f'Wrong {cifraid+1} symbol "{cimvol}"({cifra}) in {strokaid+1} line, placed debug block')
                                self.addBlock((x_pos,y_pos,0),(1,0,1,1))
                                self.drawline((x_pos,y_pos,0),(x_pos,y_pos,100),3)
                                self.drawline((x_pos+0.2,y_pos+0.2,0),(x_pos+0.2,y_pos-0.2,100))
                                self.drawline((x_pos-0.2,y_pos-0.2,0),(x_pos+0.2,y_pos-0.2,100))
                                self.drawline((x_pos-0.2,y_pos+0.2,0),(x_pos+0.2,y_pos-0.2,100))
                                self.drawline((x_pos+0.2,y_pos-0.2,0),(x_pos+0.2,y_pos-0.2,100))
                            self.textModels['text']=str(loadedmodels)
                            self.textTextures['text']=str(loadedtextures)
                self.bar['value']=(strokaid+1)/len(lines)*100
                self.image['r']+=3
                taskMgr.step()
        self.bar.destroy()
        self.textModels.destroy()
        self.textTextures.destroy()
        self.loadtimetext=OnscreenText(text='map loaded in '+str(datetime.now()-start_time),pos=(0,0.9),scale=0.05)
        print('map loaded in '+str(datetime.now()-start_time))
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