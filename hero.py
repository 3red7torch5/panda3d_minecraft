import numpy as np
from panda3d.core import NodePath,LineSegs,LVecBase3f,Vec2F
from sys import exit
from direct.actor.Actor import Actor
from panda3d.core import Character
from mapmanager import DynamicObject
from direct.gui.OnscreenText import OnscreenText
from random import randint
def isAir(pos):
    p=(round(pos[0]),round(pos[1]),round(pos[2]))
    p0=(round(pos[0]),round(pos[1]),round(pos[2])+1)
    p1=(round(pos[0]),round(pos[1]),round(pos[2])+2)
    if len(base.land.land.findAllMatches('=position='+str(p)))!=0 or len(base.land.land.findAllMatches('=position='+str(p0)))!=0 or len(base.land.land.findAllMatches('=position='+str(p1)))!=0:
        return False
    else:
        return True
def drawbox(pos,thickness=1):
    base.land.drawline((pos[0]-0.5,pos[1]-0.5,pos[2]-0.5),(pos[0]+0.5,pos[1]-0.5,pos[2]-0.5),thickness)
    base.land.drawline((pos[0]-0.5,pos[1]-0.5,pos[2]-0.5),(pos[0]-0.5,pos[1]+0.5,pos[2]-0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]+0.5,pos[2]-0.5),(pos[0]+0.5,pos[1]-0.5,pos[2]-0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]+0.5,pos[2]-0.5),(pos[0]-0.5,pos[1]+0.5,pos[2]-0.5),thickness)
    base.land.drawline((pos[0]-0.5,pos[1]-0.5,pos[2]+0.5),(pos[0]+0.5,pos[1]-0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]-0.5,pos[1]-0.5,pos[2]+0.5),(pos[0]-0.5,pos[1]+0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]+0.5,pos[2]+0.5),(pos[0]+0.5,pos[1]-0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]+0.5,pos[2]+0.5),(pos[0]-0.5,pos[1]+0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]-0.5,pos[1]-0.5,pos[2]-0.5),(pos[0]-0.5,pos[1]-0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]-0.5,pos[2]-0.5),(pos[0]+0.5,pos[1]-0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]-0.5,pos[1]+0.5,pos[2]-0.5),(pos[0]-0.5,pos[1]+0.5,pos[2]+0.5),thickness)
    base.land.drawline((pos[0]+0.5,pos[1]+0.5,pos[2]-0.5),(pos[0]+0.5,pos[1]+0.5,pos[2]+0.5),thickness)
class Hero():
    def __init__(self,position,land,model,texture):
        self.hero=loader.loadModel(model)
        self.head=loader.loadModel('smiley')
        self.hero.setTexture(loader.loadTexture(texture))
        self.hero.setPos((position[0],position[1],position[2]))
        self.hero.setColor((0.4,0.2,1,0))
        self.hero.setScale(0.5)
        self.hero.reparentTo(render)
        self.head.reparentTo(self.hero)
        self.head.setPos((0,0,4.5))
        self.weapon=loader.loadModel('shotgun.obj')
        self.weapon.reparentTo(self.head)
        self.hero.setColor((0.2,0,0.8,1))
        self.weapon.setHpr(-90,90,90)
        self.weapon.setPos(-1,-2.6,-1024)
        self.wpzw=-1
        self.weapon.setScale(0.5,0.5,0.4)
        self.pic=loader.loadModel('axe.obj')
        self.pic.reparentTo(self.head)
        self.pic.setPos(1.7,-2.2,-1024)
        self.pic.setScale(0.05,0.05,0.05)
        self.pic.setHpr(90,90,90)
        self.wpzp=-1.3
        self.indiacator=Indiacator((0,-2.4,-1),(0.5,0,0,1),'block.egg','block.png',self)
        #crosshair
        #self.lines = LineSegs()
        #self.lines.setThickness(1)
        #self.lines.setColor((1,0.2,0.1,1))
        #self.lines.moveTo(LVecBase3f((0,-1.5,-0.01)))
        #self.lines.drawTo(LVecBase3f((0,-1.5,0.01)))
        #self.lines.moveTo(LVecBase3f((-0.01,-1.5,0)))
        #self.lines.drawTo(LVecBase3f((0.01,-1.5,0)))
        #linenode = self.lines.create()
        #NodePath(linenode).reparentTo(self.head)
        self.cameraBind()
        self.accept_events()
        self.speed=0.1
        self.mode='normal'
        self.velocity_x,self.velocity_y,self.velocity_z=0,0,0
        self.jumping=False
        self.slot=None
        self.selection(3)
        self.text=OnscreenText(text='',pos=(0,-0.9),scale=0.1)
        self.reach=30
        self.accuracy=1.5
    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.head)
        base.camera.setPos(0,-0.25,0)
        base.camera.setHpr(180,0,0)
        self.cameraOn=True
    def cameraUnbind(self):
        pos=self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0],-pos[1],-pos[2]-(1.8))
        base.camera.reparentTo(render)
        base.camera.setH(self.hero.getH()-180)
        base.camera.setP(self.hero.getP())
        base.camera.setR(self.hero.getR())
        base.enableMouse()
        self.cameraOn=False
    def toggleCamera(self):
        if self.cameraOn:
            self.cameraUnbind()
        else:
            self.cameraBind()
    def teleportCamera(self):
        pos=self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0],-pos[1],-pos[2]-(1.5))
        base.camera.setH(self.hero.getH()+180)
        base.camera.setP(self.hero.getP())
        base.camera.setR(self.hero.getR())
    def gamemode(self):
        if self.mode=='noclip':
            self.mode='normal'
        elif self.mode=='normal':
            self.mode='noclip'
        else:
            pass
    def accept_events(self):
        base.accept('escape',exit)
        base.accept('c',self.toggleCamera)
        base.accept('x',self.teleportCamera)
        base.accept('b',self.gamemode)
        base.accept('lshift',self.togglesprint)
        base.accept('1',self.selection,[1])
        base.accept('2',self.selection,[2])
        base.accept('3',self.selection,[3])
        base.accept('f',self.use)
        base.accept('f',self.use)
        base.accept('g',self.use)
        base.accept('g',self.flatplace)
    def selection(self,slot):
        if slot!=self.slot:
            self.slot=slot
            if slot==1:
                self.pic.setZ(-1024)
                self.wpzp=self.pic.getZ()
                self.weapon.setZ(-0.8)
                self.wpzw=self.weapon.getZ()
                base.shotgundraw.play()
            elif slot==2:
                self.weapon.setZ(-1024)
                self.wpzw=self.weapon.getZ()
                self.pic.setZ(-1.8)
                self.wpzp=self.pic.getZ()
                base.coun=90
                base.axedraw.play()
            elif slot==3:
                self.weapon.setZ(-1024)
                self.wpzw=self.weapon.getZ()
                self.pic.setZ(-1024)
                self.wpzp=self.pic.getZ()
                base.free.play()
    def checkmouse(self):
        fov=base.camLens.getFov()
        wp = base.win.getProperties()
        if base.mouseWatcherNode.hasMouse() and self.cameraOn:
            mousepos=(base.mouseWatcherNode.getMouseX(),base.mouseWatcherNode.getMouseY())
            self.head.setH(self.head.getH()-(mousepos[0]*fov[0])%360)
            self.head.setP(self.head.getP()-(mousepos[1]*fov[1]))
            if self.head.getP()<=-90:
                self.head.setP(-89)
            elif self.head.getP()>=90:
                self.head.setP(89)
            base.win.movePointer(0,wp.getXSize()//2,wp.getYSize()//2)
    def moveplayer(self):
        p=self.hero.getPos()
        if isAir((p[0]+(self.velocity_x*0.1),p[1]+(self.velocity_y*0.1),p[2]+(self.velocity_z*0.1))):
            if self.jumping:
                self.hero.setPos((p[0]+self.velocity_x*0.15,p[1]+self.velocity_y*0.15,p[2]+self.velocity_z*0.1))
            else:
                self.hero.setPos((p[0]+self.velocity_x*0.1,p[1]+self.velocity_y*0.1,p[2]+self.velocity_z*0.1))
            self.velocity_x-=self.velocity_x*0.1
            self.velocity_y-=self.velocity_y*0.1
            self.velocity_z-=self.velocity_z*0.1
        else:
            self.velocity_x,self.velocity_y,self.velocity_z=0,0,0
        if not self.mode=='noclip':
            self.isOnGround(self.hero.getPos())
        #print(f"X:{round(self.velocity_x,1)} Y:{round(self.velocity_y,1)} Z:{round(self.velocity_z,1)}")
    def isOnGround(self,pos):
        p=(round(pos[0]),round(pos[1]),round(pos[2]))
        if len(base.land.land.findAllMatches('=position='+str(p))):
            self.hero.setZ(self.hero.getZ()+1)
        if len(base.land.land.findAllMatches('=position='+str((p[0],p[1],p[2]-1))))!=0:
            self.velocity_z=0
            self.jumping=False
        else:
            self.velocity_z-=0.15
    def forward(self):
        x=np.sin(np.radians(self.head.getH()))*self.speed
        y=np.cos(np.radians(self.head.getH()))*self.speed
        #z=np.sin(np.radians(self.hero.getP()))*5
        pos=self.hero.getPos()
        newpos=(pos[0]+x,pos[1]-y,pos[2])#-z)
        if self.mode=='noclip':
            self.hero.setPos(newpos)
        elif isAir(newpos):
            self.velocity_x+=x
            self.velocity_y-=y
        elif not isAir(newpos):
            self.velocity_x=0
            self.velocity_y=0
        else:
            pass
    def backward(self):
        x=np.sin(np.radians(self.head.getH()))*self.speed
        y=np.cos(np.radians(self.head.getH()))*self.speed
        #z=np.sin(np.radians(self.hero.getP()))*5
        pos=self.hero.getPos()
        newpos=(pos[0]-x,pos[1]+y,pos[2])#+z)
        if self.mode=='noclip':
            self.hero.setPos(newpos)
        elif isAir(newpos):
            self.velocity_x-=x
            self.velocity_y+=y
        elif not isAir(newpos):
            self.velocity_x=0
            self.velocity_y=0
        else:
            pass
    def left(self):
        x=np.cos(np.radians(self.head.getH()))*self.speed
        y=np.sin(np.radians(self.head.getH()))*self.speed
        pos=self.hero.getPos()
        newpos=(pos[0]+x,pos[1]+y,pos[2])
        if self.mode=='noclip':
            self.hero.setPos(newpos)
        elif isAir(newpos):
            self.velocity_x+=x
            self.velocity_y+=y
        elif not isAir(newpos):
            self.velocity_x=0
            self.velocity_y=0
        else:
            pass
    def right(self):
        x=np.cos(np.radians(self.head.getH()))*self.speed
        y=np.sin(np.radians(self.head.getH()))*self.speed
        pos=self.hero.getPos()
        newpos=(pos[0]-x,pos[1]-y,pos[2])
        if self.mode=='noclip':
            self.hero.setPos(newpos)
        elif isAir(newpos):
            self.velocity_x-=x
            self.velocity_y-=y
        elif not isAir(newpos):
            self.velocity_x=0
            self.velocity_y=0
        else:
            pass
    def jump(self):
        if self.mode=='normal':
            if not self.jumping:
                self.jumping=True
                #self.hero.setZ(self.hero.getZ()+0.5)
                self.velocity_z=3
        elif self.mode=='noclip':
            self.hero.setZ(self.hero.getZ()+0.5)
        else:
            pass
    def togglesprint(self):
        if self.speed==0.1:
            self.speed=0.2
            self.weapon.setHpr(0,120,0)
        else:
            self.speed=0.1
            self.weapon.setHpr(-90,90,90)
    def use(self):
        if self.slot==3:
            self.blockplace()
        elif self.slot==2:
            self.blockremove()
        elif self.slot==1:
            self.shoot()
        else:
            pass
    def frame(self):
        for i in base.land.lnodelist:
            i.removeNode()
        pos=(self.hero.getX(),self.hero.getY(),self.hero.getZ()+(self.head.getZ()*0.5))
        x=np.sin(np.radians(self.head.getH()))/self.accuracy
        y=np.cos(np.radians(self.head.getH()))/self.accuracy
        z=-np.radians(self.head.getP())/self.accuracy
        currentpos=LVecBase3f(x,y,z)
        prepos=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]+currentpos[2]))
        for _ in range(self.reach):
            cp=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]+currentpos[2]))
            if len(base.land.land.findAllMatches('=position='+str(cp)))!=0:
                #base.land.drawline(pos,cp,5)
                if self.slot==3:
                    #base.land.drawline((prepos[0]-0.2,prepos[1]-0.2,prepos[2]-0.2),(prepos[0]+0.2,prepos[1]+0.2,prepos[2]+0.2),5)
                    #base.land.drawline((prepos[0]+0.2,prepos[1]+0.2,prepos[2]-0.2),(prepos[0]-0.2,prepos[1]-0.2,prepos[2]+0.2),5)
                    #base.land.drawline((prepos[0]-0.2,prepos[1]+0.2,prepos[2]-0.2),(prepos[0]+0.2,prepos[1]-0.2,prepos[2]+0.2),5)
                    #base.land.drawline((prepos[0]+0.2,prepos[1]-0.2,prepos[2]-0.2),(prepos[0]-0.2,prepos[1]+0.2,prepos[2]+0.2),5)
                    drawbox(prepos,5)
                else:
                    base.land.drawline((cp[0]-0.6,cp[1]-0.6,cp[2]-0.6),(cp[0]+0.6,cp[1]+0.6,cp[2]+0.6),10)
                    base.land.drawline((cp[0]+0.6,cp[1]+0.6,cp[2]-0.6),(cp[0]-0.6,cp[1]-0.6,cp[2]+0.6),10)
                    base.land.drawline((cp[0]-0.6,cp[1]+0.6,cp[2]-0.6),(cp[0]+0.6,cp[1]-0.6,cp[2]+0.6),10)
                    base.land.drawline((cp[0]+0.6,cp[1]-0.6,cp[2]-0.6),(cp[0]-0.6,cp[1]+0.6,cp[2]+0.6),10)
                break
            else:
                currentpos[0]+=x
                currentpos[1]+=y
                currentpos[2]+=z
                prepos=cp
    def blockplace(self):
        pos=(self.hero.getX(),self.hero.getY(),self.hero.getZ()+(self.head.getZ()*0.5))
        x=np.sin(np.radians(self.head.getH()))/self.accuracy
        y=np.cos(np.radians(self.head.getH()))/self.accuracy
        z=np.radians(self.head.getP())/self.accuracy
        currentpos=LVecBase3f(x,y,z)
        prepos=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
        for _ in range(self.reach):
            cp=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
            if len(base.land.land.findAllMatches('=position='+str(cp)))!=0:
                base.land.addBlock(prepos,(randint(0,100)/100,randint(0,100)/100,randint(0,100)/100,1))
                break
            else:
                currentpos[0]+=x
                currentpos[1]+=y
                currentpos[2]+=z
                prepos=cp
    def flatplace(self):
        pos=(self.hero.getX(),self.hero.getY(),self.hero.getZ()+(self.head.getZ()*0.5))
        x=np.sin(np.radians(self.head.getH()))/self.accuracy
        y=np.cos(np.radians(self.head.getH()))/self.accuracy
        z=np.radians(self.head.getP())/self.accuracy
        currentpos=LVecBase3f(x,y,z)
        prepos=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
        for _ in range(self.reach):
            cp=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
            if len(base.land.land.findAllMatches('=position='+str(cp)))!=0:
                px,py,pz=prepos
                dx_list=[1,0,-1]
                dy_list=[1,0,-1]
                for dx in dx_list:
                    for dy in dy_list:
                        base.land.addBlock((px+dx,py+dy,pz),(randint(0,100)/100,randint(0,100)/100,randint(0,100)/100,1))
                break
            else:
                currentpos[0]+=x
                currentpos[1]+=y
                currentpos[2]+=z
                prepos=cp
    def blockremove(self):
        pos=(self.hero.getX(),self.hero.getY(),self.hero.getZ()+(self.head.getZ()*0.5))
        x=np.sin(np.radians(self.head.getH()))/self.accuracy
        y=np.cos(np.radians(self.head.getH()))/self.accuracy
        z=np.radians(self.head.getP())/self.accuracy
        currentpos=LVecBase3f(x,y,z)
        for _ in range(self.reach):
            cp=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
            fam=base.land.land.findAllMatches('=position='+str(cp))
            if len(fam)!=0:
                for i in fam:
                    i.removeNode()
                break
            else:
                currentpos[0]+=x
                currentpos[1]+=y
                currentpos[2]+=z
    def shoot(self):
        base.shotsound.play()
        pos=(self.hero.getX(),self.hero.getY(),self.hero.getZ()+(self.head.getZ()*0.5))
        x=np.sin(np.radians(self.head.getH()))/self.accuracy
        y=np.cos(np.radians(self.head.getH()))/self.accuracy
        z=np.radians(self.head.getP())/self.accuracy
        currentpos=LVecBase3f(x,y,z)
        prepos=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
        for _ in range(self.reach*10):
            cp=(round(pos[0]+currentpos[0]),round(pos[1]-currentpos[1]),round(pos[2]-currentpos[2]))
            fam=base.land.land.findAllMatches('=position='+str(cp))
            if len(fam)!=0:
                for i in fam:
                    i.removeNode()
                    base.land.drawline(prepos,cp)
            else:
                currentpos[0]+=x
                currentpos[1]+=y
                currentpos[2]+=z
                prepos=cp
        self.head.setP(self.head.getP()-10)
    def multiuse(self):
        for i in range(0,375,15):
            for j in range(-60,105,15):
                self.head.setHpr(i,j,0)
                self.use()
                print(f'used, Heading:{i}, Pitch:{j}')
class Indiacator(DynamicObject):
    def __init__(self,position,color,filename,texture,parent):
        self.parent=parent
        try:
            self.model=loader.loadModel(filename)
        except:
            print(f'FAILED TO LOAD MODEL "{filename}"')
        finally:
            self.model.reparentTo(parent.head)
            self.model.setPos(position)
            self.model.setColor(color)
        try:
            self.model.setTexture(loader.loadTexture(texture))
        except:
            print(f'FAILED TO LOAD TEXTURE "{texture}"')
    def update_speedometer(self):
        a=(np.abs(base.hero.velocity_x)+np.abs(base.hero.velocity_y))/2*0.5+0.15
        self.model.setScale(a,0.1,0.1)
        if self.parent.mode=="normal":
            self.model.setColor((0.7,0.2,0.1,1))
            #a=LVecBase3f(np.tan(self.parent.hero.getZ()),np.tan(self.parent.hero.getX()),np.tan(self.parent.hero.getY()))
            #self.model.setHpr(a*10)
            self.model.setHpr(0,self.model.getP()+(a*10),0)
        elif self.parent.mode=="noclip":
            self.model.setColor((0.2,0.5,0.7,1))
            self.model.setScale(0.4,0.4,0.4)
            self.model.setR(self.model.getR()+5)
            self.model.setH(self.model.getH()+5)
        else:
            self.model.setColor((0,0,0,1))