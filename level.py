#coding: -utf-8-
import os,math

import pygame
from pygame.locals import *

from cnst import *

from pgu import engine

INV_W = 71
INV_H = 71

class Obj:
    def __init__(self,l,name,src,pos,scale=100):
        self.level = l
        self.name = name
        self.talking = False
        self.src = src
        self.rect = pygame.Rect(0,0,1,1)
        self.rect.centerx, self.rect.bottom = pos
        self.pos = pos
        
        self.path = []
        self._path_stop = None
        
        self.focus = None
        
        self.text = None
        self.text_color = "#ffffffff"
        self.text_timer = 0
        
        self.frame = 0
        self.state = 'default'
        self.facing = None
        self.data = {}
        self.scale = scale
        self.images = []
        self._rect = None
        self.can_walk = True

        self.animating = False
        
        self.load()

    def animate(self,state):
        self.animating = True
        self.frame = 0
        self.state = state
        
    def loop(self):
        #KALLE: Not setting state to "stand" if standing still every loop
        #Special case for player (need to fix for NPCS as well. self.can_walk ?)
        #All this need to go somewhere else!

        #For the player
        if self.name == "player":
            if self.animating == False:
                if len(self.path):
                    self.state = "walk"
                elif not len(self.path) and not self.talking:
                    self.state = "stand"
                elif self.state == "":
                    self.state = "stand"

        #For talking characters
        if self.talking and self.state != "talk":
            self.state = "talk"
        if not self.talking and self.state == "talk":
            self.state = "default"
        
#         if self.state == 'stand':
#             for o in self.level.objs.values():
#                 if o != self and o.text != None and o.text_timer > 0:
#                     if self.rect.centerx < o.rect.centerx:
#                         self.facing = 'right'
#                     else:
#                         self.facing = 'left'
            
            
        #KALLE: All directions!
        #KALLE: _rect > rect == E/N
        #KALLE: _rect < rect == W/S
            
        if self._rect != None:
            if self._rect.x < self.rect.x and self._rect.y == self.rect.y:
                self.facing = 'e'
            elif self._rect.x > self.rect.x and self._rect.y == self.rect.y:
                self.facing = 'w'
            elif self._rect.x == self.rect.x and self._rect.y < self.rect.y:
                self.facing = 's'
            elif self._rect.x == self.rect.x and self._rect.y > self.rect.y:
                self.facing = 'n'
            elif self._rect.x < self.rect.x and self._rect.y < self.rect.y:
                self.facing = 'se'
            elif self._rect.x > self.rect.x and self._rect.y > self.rect.y:
                self.facing = 'nw'
            elif self._rect.x < self.rect.x and self._rect.y > self.rect.y:
                self.facing = 'ne'
            elif self._rect.x > self.rect.x and self._rect.y < self.rect.y:
                self.facing = 'sw'

            #KALLE: Sätt scale om den är ändrad.
            #(Galen matematik, behöver rumsspecifika grejer här. Det är ju dessutom bara spelaren som ska skalas!)
            #if self.name == "player":
             #   self.scale = math.ceil((self.rect.y + 181)/3.7)
        state_facing = '%s_%s'%(self.state,self.facing)
        state_regular = '%s'%(self.state)


        #KALLE: Needs cleaning up. Badly
        cls = '%s_%s'%(self.state,self.facing)
        if cls not in self.data:
            cls = '%s'%(self.state)
        if cls not in self.data:
            cls = 'default'
        if cls in self.data:
            r = self.data[cls]

            #KALLE: For debugging puzzle states
            #if self.name != "player":
            #    print self.state

            self.image = self._scale(r[self.frame%r['frames']])
                #print r,self.frame%r['frames'],r['frames']-1
            if self.animating and self.frame%r['frames'] == r['frames']-1:
                self.animating = False

            #KALLE: To push to next frame or not:
            if self.state == "walk" or self.state == "talk":
                loop = True
            elif self.animating == False:
                loop = False
            else:
                loop = True

            if loop and r['speed'] != 0 and self.level.frame%r['speed'] == 0:
                self.frame += 1

        self._rect = pygame.Rect(self.rect)
                
    def _scale(self,img):
        
        #return pygame.transform.scale(img,(img.get_width()*self.scale/100,img.get_height()*self.scale/100))
        
        return pygame.transform.rotozoom(img,0,self.scale/100.0)
        
    def load(self):
        src = self.src
        
        self.data = {}
        
        try:
            import ConfigParser
            cfg = ConfigParser.ConfigParser()
            cfg.read(os.path.join('data',src,'ani.ini'))
            for sect in cfg.sections():
                self.data[sect] = {}
                for k in cfg.options(sect):
                    key = k
                    try:
                        key = int(k)
                    except:
                        pass
                    if k in ('speed','frames','loop'):
                        self.data[sect][key] = cfg.getint(sect,k)
                    else:
                        try:
                            self.data[sect][key] = self._scale( pygame.image.load(os.path.join('data',src,cfg.get(sect,k))).convert_alpha())
                        except:
                            import traceback; traceback.print_exc()
        except:
            import traceback; traceback.print_exc()
            print 'no ani.ini for',src
            
        #print self.data
        
        self.image = None
        self.frame = 0
        self.state = 'default'
        self.facing = None
        self.loop()
        
        if self.image == None:
        
            try:
                self.image = self._scale(pygame.image.load(os.path.join('data',src,"default.png")))
            except:
                try:
                    self.image = self._scale(pygame.image.load(os.path.join('data','inv','%s.png'%src)))
                except:
                    self.image = self._scale(pygame.image.load(os.path.join('data','default','%s.png'%src)))
                    
        try:
            shape = self._scale(pygame.image.load(os.path.join('data',src,"shape.png")))
            r = pygame.Rect(0xfff,0xfff,-0xfff,-0xfff)
        
            x = shape.get_width()/2
            for y in xrange(0,shape.get_height()):
                _r,g,b,a = shape.get_at((x,y))
                if a > 128:
                    minx,maxx,miny,maxy = min(x,r.left),max(x+1,r.right),min(y,r.top),max(y+1,r.bottom)
                    r = pygame.Rect(minx,miny,maxx-minx,maxy-miny)
    
            y = shape.get_height()/2
            for x in xrange(0,shape.get_width()):
                _r,g,b,a = shape.get_at((x,y))
                if a > 128:
                    minx,maxx,miny,maxy = min(x,r.left),max(x+1,r.right),min(y,r.top),max(y+1,r.bottom)
                    r = pygame.Rect(minx,miny,maxx-minx,maxy-miny)
        except:
            r = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        
        self.shape = r
        x,y = self.rect.centerx,self.rect.bottom
        self.rect = pygame.Rect(r)
        self.rect.centerx,self.rect.bottom = x,y
        
        self.loop()
        
        #HACK: to make the player face correctly if moved
        self.facing = None
        self._rect = None
        
    def walkto(self,pos,_path_stop = None):
        if self.can_walk:
            if not self.level.showinventory:
                self.level._walkto(self,pos,_path_stop)
        
        
    def blank(self):
        pass
    
    def face(self,pos):
        if self.can_walk:
            if not pos in self.level.objs: return
            o = self.level.objs[pos]
            self._rect = None
            if self.rect.centerx < o.rect.centerx:
                self.facing = 'e'
            else:
                self.facing = 'w'
    
    def walkpos(self,pos,fnc=None):
        if self.can_walk:
            if fnc == None: fnc = self.blank
            def myfnc():
                self.face(pos)
                fnc()
            self.level._walkto(self,'%s_pos'%pos,myfnc)
        
        
    def _say(self,msg):
        self.text = msg
        self.text_timer = max(FPS/2,len(msg)*FPS/15) #20 CPS reading...
        
    def rename(self,name):
        del self.level.objs[self.name]
        self.name = name
        self.level.objs[name] = self
        

class Layer:
    def __init__(self,c):
        self.image = None
        self.rect = None
        self.key = c
        self.rle = []

class Level:
    def __init__(self,game,src):
        self.game,self.src = game,src
        self.frame = 0
        self.showinventory = False
        
    def layers_build(self):
        img = self.i_layers
        layers = self.layers = {}
        #print layers
        l = layers['#000'] = Layer('#000')
        l.rect = pygame.Rect(0,0,1,1)
        
        for y in xrange(0,img.get_height()):
            layer = None
            slay,sx = None,0
            for x in xrange(0,img.get_width()):
                c = img.get_at((x,y))
                ct = "#%x%x%x"%(c[0]/16,c[1]/16,c[2]/16)
                
                if ct != '#fff' and ct not in layers:
                    l = layers[ct] = Layer(ct)
                    l.rect = pygame.Rect(img.get_width(),img.get_height(),-img.get_width(),-img.get_height())
                    
                if ct != '#fff':
                    layer = layers[ct]
                    
                if slay != None and layer != slay:
                    slay.rle.append((y,sx,x-sx))
                    
                if layer != slay:
                    slay,sx = layer,x
                
                if ct == '#fff' and layer:
                    r = layer.rect
                    minx,maxx,miny,maxy = min(x,r.left),max(x+1,r.right),min(y,r.top),max(y+1,r.bottom)
                    layer.rect = pygame.Rect(minx,miny,maxx-minx,maxy-miny)
            
            #NOTE: add EOL
            x = img.get_width()
            slay.rle.append((y,sx,x-sx))
                    
#         for l in layers.values():
#             print l.key,l.rle
                    
    def layers_save(self):
        layers = self.layers
        
        f = open(os.path.join('data',self.src,"layers.txt"),"w")
        for l in layers.values():
            rle = ";".join([','.join([str(v) for v in vs]) for vs in l.rle])
            f.write("%s\t%d\t%d\t%d\t%d\t%s\n"%(l.key,l.rect.x,l.rect.y,l.rect.w,l.rect.h,rle))
        f.close()
        
    def hotspots_save(self):
        hotspots = self.hotspots
        
        f = open(os.path.join('data',self.src,'hotspots.txt'),'w')
        for k,v in hotspots.items():
            f.write('%s\t%s\n'%(k,v))
        f.close()
        
    def hotspots_load(self):
        hotspots = self.hotspots
        try:
            f = open(os.path.join('data',self.src,'hotspots.txt'),'r')
            for line in f.readlines():
                k,v = line.strip().split('\t')
                hotspots[k] = v
        except:
            import traceback; traceback.print_exc()
            
    def objs_save(self):
        objs = self.objs
        f = open(os.path.join('data',self.src,'objs.txt'),'w')
        for e in objs.values():
            f.write('%s\t%s\t%d\t%d\t%d\n'%(e.name,e.src,e.rect.centerx,e.rect.bottom,e.scale))
            
    def objs_load(self):
        objs = self.objs
        try:
            f = open(os.path.join('data',self.src,'objs.txt'),'r')
            for line in f.readlines():
                vals = line.strip().split('\t')
                if len(vals) == 4:
                    name,src,x,y = vals
                    scale = 100
                else:
                    name,src,x,y,scale = vals
                name,src,x,y,scale = name,src,int(x),int(y),int(scale)
                e = objs[name] = Obj(self,name,src,(x,y),scale)
        except:
            import traceback; traceback.print_exc()
        
    def load(self):
        #KALLE: Support for PNG backgrounds, which we want to use instead.
        try:
            bkgr = self.bkgr = pygame.image.load(os.path.join('data',self.src,'bkgr.jpg')).convert()
        except pygame.error:
                bkgr = self.bkgr = pygame.image.load(os.path.join('data',self.src,'bkgr.png')).convert()
        self.i_layers = pygame.image.load(os.path.join('data',self.src,'layers.png')).convert_alpha()
        self.i_walkable = pygame.image.load(os.path.join('data',self.src,'walkable.png')).convert_alpha()
        self.i_hotspots = pygame.image.load(os.path.join('data',self.src,'hotspots.png')).convert_alpha()
        
        self.layers = {}
        iw = self.i_walkable
        self.walkable = [[iw.get_at((x,y))!=(0,0,0,255) for x in xrange(TW/2,iw.get_width(),TW)] for y in xrange(TH/2,iw.get_height(),TH)]
        self.hotspots = {}
        self.objs = {}
        
        self.bounds = pygame.Rect(0,0,bkgr.get_width(),bkgr.get_height())
        self.view = pygame.Rect(0,0,SW,bkgr.get_height())
        
        self.layers_load()
        self.hotspots_load()
        self.objs_load()
            
    def layers_load(self):
        bkgr = self.bkgr
        layers = self.layers
        
        #Load the layers data from text file
        #pal = [(0,0,0)]
        try:
            f = open(os.path.join('data',self.src,'layers.txt'),'r')
            for line in f.readlines():
                key,x,y,w,h,rle = line.strip().split('\t')
                key,x,y,w,h,rle = key,int(x),int(y),int(w),int(h),rle
                l = layers[key] = Layer(key)
                r = l.rect = pygame.Rect(x,y,w,h)
                l.color = self.hex2c(key)
                l.rle = [[int(v) for v in vs.split(',')] for vs in rle.split(';')]
                #pal.append(l.color)
            f.close()
        except:
            import traceback; traceback.print_exc()
            
        for l in self.layers.values():
            magic = (0,255,255)
            img = bkgr.convert()
            img.fill(magic)
            for y,x,w in l.rle:
                #print l.key,x,y,w
                img.blit(bkgr,(x,y),(x,y,w,1))
            img.set_colorkey(magic)
            l.image = img
                
            
        #the old way was cool, but it doesn't work :(
#         #render all the layers data
#         img = pygame.Surface((self.i_layers.get_width(),self.i_layers.get_height()),0,8)
#         img.set_palette(pal)
#         img.blit(self.i_layers,(0,0))
#         magic1 = (128,0,128)
#         magic2 = (128,128,0)
#         for l in self.layers.values():
#             img2 = bkgr.convert()
#             for n in xrange(0,len(pal)):
#                 img.set_palette_at(n,magic1)
#             img.set_palette_at(pal.index(l.color),magic2)
#             img.set_colorkey(magic2)
#             img2.blit(img,(0,0))
#             img2.set_colorkey(magic1) #,pygame.RLEACCEL) #this gives a minor speed up, but can cause crashes
#             l.image = img2

        
    def c2hex(self,c):
        return "#%x%x%x"%(c[0]/16,c[1]/16,c[2]/16)
    
    def hex2c(self,c):
        return (int(c[1],16)*16,int(c[2],16)*16,int(c[3],16)*16)
        
    def hotspots_match(self,c):
        ct = self.c2hex(c)
        if ct in self.hotspots:
            return self.hotspots[ct]
        return None
    
    def hotspots_find(self,pos):
        try:
            return self.hotspots_match(self.i_hotspots.get_at(pos))
        except:
            pass
    
    def objs_find(self,pos):
        for e in self.objs.values():
            if e.rect.collidepoint(pos):
                return e
        return None
        
    def find(self,pos):
        r = []
        for e in self.objs.values():
            if e.rect.collidepoint(pos):
                r.append(e.name)
        v = self.hotspots_find(pos)
        if v != None:
            r.append(v)
        return r
    
    def save(self):
        self.layers_save()
        self.hotspots_save()
        self.objs_save()
        pass
        
    def init(self):
        self.load()
        self.item = None
        self.mode = 'normal'
        self.items = {}
        self._goto = None
        
    def paint(self,screen):
        getattr(self,'paint_%s'%self.mode)(screen)
        
    def paint_main(self,screen):
        if hasattr(self,'player'):
            self.follow(self.player)
        
        todo = []
        for l in self.layers.values():
            if l.image and l.rect.h > 0:
                todo.append((l.rect.bottom,l.image,(0,0)))
                
        for s in self.objs.values():
            s.loop()
            todo.append((s.rect.bottom,s.image,(s.rect.x-s.shape.x,s.rect.y-s.shape.y)))
            
        self.view.clamp_ip(self.bounds)
            
        todo.sort()
        for z,img,pos in todo:
            pos = pos[0]-self.view.x,pos[1]-self.view.y
            screen.blit(img,pos)
            #screen.fill((255,255,255),(pos[0],z,4,4))

        for o in self.objs.values():
            if o.text != None:
                #lines = o.text.split('\n')
                text = o.text
                text = text.replace('\n',' ')
                l = len(text)
                words = text.split(' ')
                wps = 8
                #if len(words) > 20: wps = len(words)/(4 - int(len(words)%4>0))
                lc = (len(words)/wps) + int(len(words)%wps > 0)
                lines = [ [] for n in xrange(0,lc)]
                n = 0
                for word in words:
                    lines[n/wps].append(word)
                    n += 1
                lines = [' '.join(ws) for ws in lines] 
                
                
                fnt = self.game.font
                h = fnt.get_height()
                cx,y = o.rect.centerx-self.view.x,o.rect.top-(h*len(lines)+8)-self.view.y
                if y < 8: y = 8
                for line in lines:
                    img = fnt.render(line,1,(0,0,0))
                    x = cx-img.get_width()/2
                    sw = SW-8
                    if x + img.get_width() >= sw:
                        x = sw-img.get_width()
                    if x < 8:
                        x = 8
                    for dx,dy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                        screen.blit(img,(x+dx,y+dy))
                    img = fnt.render(line,1,Color(o.text_color))
                    screen.blit(img,(x,y))
                    y += h

        self.game.draw_cursor()

    def paint_edit(self,screen):
        self.paint_main(screen)
        
    def paint_inv_box(self,screen):
        #KALLE: Lade toggler för visning av inventoryt
        if self.showinventory:
            screen.fill((0,0,0),(75,50,433,292))
            
            #KALLE: Rita fler rader
            y = -13 #Ugliest hack evar?:D
            for row in xrange(0,4):
                y += 71
                for n in xrange(0,6):
                    x = 82+INV_W*n
                    row = row +1
                    screen.fill((0x55,0x55,0x55),(x-2,y-2,67,67))
                    #screen.fill((0xaa,0xaa,0xaa),(x-4,y-4,72,72))
                    #screen.fill((0x55,0x55,0x55),(x,y,64,64))
            
            n = 0
            row = 0
            invs = self.game.data['inv'][:]
            if self.item in invs:
                invs.remove(self.item)
            for item in invs:
                if item != None:
                    if item not in self.items:
                        #KALLE: Ladda separat bild för item inuti inventory
                        self.items[item] = pygame.image.load(os.path.join('data','inv','icons','%s.png'%item))
                    img = self.items[item]
                    x = x = 82+INV_W*n
                    y = 71
                    screen.blit(img,(x,y))
                
                n += 1

        self.game.draw_cursor()
            
        
    def paint_normal(self,screen):
        self.paint_main(screen)
        self.game.draw_inventory_icon()
        self.paint_inv_box(screen)
        pygame.display.flip()
        
    def paint_inv(self,screen):
        self.paint_main(screen)
        self.paint_inv_box(screen)

        item = self.item
        if item != None:
            if item not in self.items:
                #KALLE: Ladda separat bild för item inuti inventory
                self.items[item] = pygame.image.load(os.path.join('data','inv','icons','%s.png'%item))
            img = self.items[item]
            x,y = pygame.mouse.get_pos()
            x,y = x-img.get_width()/2,y-img.get_height()/2
            screen.blit(img,(x,y))

        pygame.display.flip()        
        
    def update(self,screen):
        return self.paint(screen)
            
    def follow(self,s):
        view = self.view
        rect = s.rect
        
        w = 250
        view.left = min(view.left,s.rect.centerx-w)
        view.right = max(view.right,s.rect.centerx+w)
    
    def refresh(self):
        for o in self.objs.values():
            if o.text:
                o.text = ''
                o.text_timer = 0
        self.paint(self.game.screen)
    
        
    def loop(self):
        if self._goto:
            r = self._goto
            self._goto = None
            
#             if self.item: #so that players don't lose an item they hold when walking to a new room.
#                 self.inv.append(self.item)
#                 self.item = None
# 
            return r
        
        
        if self.mode == 'normal' and self.item != None:
            self.mode = 'inv'
            self.showinventory = True
        if self.mode == 'inv' and self.item == None:
            self.mode = 'normal'
            self.showinventory = False

        for o in self.objs.values():
            if o.text_timer:
                #print o.name,o.state,o.facing
                o.text_timer -= 1
                if o.text_timer <= 0:
                    o.text = None
                    o.talking = False

            if len(o.path):
                tx,ty = o.path.pop(0)
                if len(o.path):
                    tx,ty = o.path[0]
                    x,y = tx*TW+TW/2,ty*TH+TH/2
                    o.rect.centerx = (o.rect.centerx+x)/2
                    o.rect.bottom = (o.rect.bottom+y)/2
                else:
                    x,y = tx*TW+TW/2,ty*TH+TH/2
                    o.rect.centerx = x
                    o.rect.bottom = y
                #print len(o.path),o._path_stop
                if not len(o.path):
                    fnc = o._path_stop
                    if fnc:
                        o._path_stop = None
                        #print 'run me'
                        r = fnc()
                        if r != False: return r
                    
        
        p = self.player
                    
        focus = self.hotspots_find((p.rect.centerx,p.rect.bottom))
        if focus != p.focus:
            if p.focus:
                r = self._action('exit_%s'%p.focus)
                if r not in (False,None): return r
            p.focus = focus
            if focus:
                r = self._action('enter_%s'%focus)
                if r not in (False,None): return r
                
        self.frame += 1
                
    def _action(self,fnc):
        if hasattr(self,fnc):
            r = getattr(self,fnc)()
            return r
        return None
        
    def _walkto(self,obj,dest,_path_stop):
        obj._path_stop = _path_stop
        
        if type(dest) == str:
            dest = self.objs[dest].pos
            
        from pgu import algo
        
        def dist(a,b):
            return abs(a[0]-b[0])+abs(a[1]-b[1])
            #dx,dy = abs(a[0]-b[0]),abs(a[1]-b[1])
            #return (dx*dx+dy*dy)**0.5
        
        start = obj.rect.centerx/TW,obj.rect.bottom/TH
        end = dest[0]/TW,dest[1]/TH
        
        if not hasattr(self,'_walkable'):
            w = self._walkable = [v[:] for v in self.walkable]
            for v in w:
                v.insert(0,0)
                v.append(0)
            empty = [0 for n in xrange(0,len(w[0]))]
            w.insert(0,empty)
            w.append(empty)
            
        start = start[0]+1,start[1]+1
        end = end[0]+1,end[1]+1
        
        if start == end and obj._path_stop:
            fnc = obj._path_stop
            obj._path_stop = None
            r = fnc()
            if r != False: return r
            
        wa = self._walkable
        okay = wa[end[1]][end[0]]
        d = 0
        x,y = end
        while not okay and d < 200: #just in case, we don't want an infinite loop after 200...
            d += 1
            for dx,dy in [(-0.7,-0.7),(-1,0),(-0.7,0.7),(0,-1),(0,1),(0.7,-0.7),(1,0),(0.7,0.7)]:
                xx,yy = x+int(dx*d),y+int(dy*d)
                if xx >= 0 and xx < len(wa[0]) and yy >=0 and yy < len(wa):
                    v = wa[yy][xx]
                    if v:
                        okay = 1
                        end = xx,yy
        
        try:
            path = algo.astar(start,end,self._walkable,dist)
            obj.path = [(p[0]-1,p[1]-1) for p in path]
        except:
            print start,end
            print 'heh, sometimes our walkto screws up, oh well.'
            import traceback; traceback.print_exc()
        
    def event(self,e):
        self._e = e
        if e.type is KEYDOWN:
            #Tommy: Use e.key == 9 instead of e.scancode == 23. The latter
            # doesn't work in Windows.
            if e.key == 9:
                if(self.showinventory):
                    self.showinventory = False
                else:
                    self.showinventory = True

        if e.type is MOUSEMOTION:
            self.set_mouse_cursor(e.pos)

        if e.type is MOUSEBUTTONDOWN:
            e = pygame.event.Event(e.type,{
                'pos':(e.pos[0]+self.view.x,e.pos[1]+self.view.y),
                'button':e.button,
                })

        getattr(self,'event_%s'%self.mode)(e)

    def set_mouse_cursor(self,pos):
        hover = self.find(pos)
        x,y = pos

        self.game.currentmousepos = (x,y)
        if len(hover) != 0:
            #KALLE: TODO: Sort out what to do if there are multiple objects (shouldn't happen really)
            #KALLE: Currently gets the closest one, which is kinda what we want anyway. (if X is blocking Y, it gets X)
            if "exit_" in hover[0]:
                if "north" in hover[0]:
                    self.game.currentcursor = "exit_north"
                elif "south" in hover[0]:
                    self.game.currentcursor = "exit_south"
                elif "east" in hover[0]:
                    self.game.currentcursor = "exit_east"
                elif "west" in hover[0]:
                    self.game.currentcursor = "exit_west"
            elif "item_" in hover[0]:
                self.game.currentcursor = "pickup"
            elif "npc_" in hover[0]:
                self.game.currentcursor = "talk"
            elif len(hover) == 1 and (hover[0] == "player" or "_pos" in hover[0]):
                self.game.currentcursor = "default"
            else:
                self.game.currentcursor = "use"
        else:
            self.game.currentcursor = "default"
                
    def event_normal(self,e):
        if e.type is MOUSEBUTTONDOWN and self.showinventory == False:
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1:
            	if e.pos[0] <= 630 and e.pos[0] >= 580 and e.pos[1] <= 470 and e.pos[1] >= 410 and self.showinventory == False:
            		self.showinventory = True
                for hover in self.find(e.pos):
                    if hover: #use_ action
                        primaryfnc = 'use_%s'%hover
                        secondaryfnc = 'look_%s'%hover
                        fnc = None
                        if hasattr(self,primaryfnc):
                            fnc = primaryfnc
                        elif hasattr(self,secondaryfnc):
                            fnc = secondaryfnc
                        if fnc != None:
                            r = getattr(self,fnc)()
                            if r != False: return r
                    
                #self.walkto(self.player,e.pos)
                self.player.walkto(e.pos)

            #KALLE: Högerklick kallar objekt_look istället för att alla musknappar var objekt_use som innan.
            elif b3:
                for hover in self.find(e.pos):
                    if hover:
                        fnc = 'look_%s'%hover
                        if hasattr(self,fnc):
                            r = getattr(self,fnc)()
                            if r != False: return r
            return

        #KALLE: Notering: Klicka i inventoryt och får en item i "handen". Stäng inventoryt
        if e.type is MOUSEBUTTONDOWN and self.showinventory == True:
            self.item = self.find_inventory_item(e)
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1:
                self.sfx('get')
                self.mode = 'inv'
                #self.showinventory = False
            elif b3:
                #TODO: Show text nicer somehow. Also, make examine_foo not room-dependent!
                fnc = 'examine_%s'%self.item
                #KALLE: Vi vill inte dra runt objektet!
                self.item = None
                if hasattr(self,fnc):
                    r = getattr(self,fnc)()
                    if r != False: return r

    def inside_inventory(self):
        #KALLE: Some kind of weird bug. Possibly a 64bits pygame bug from what google told me
        try:
            return self._e.pos[0] > 77 and self._e.pos[0] < 501 and self._e.pos[1] > 48 and self._e.pos[1] < 342
        except AttributeError:
            print "FIXME: Can't open inventory for you. Sorry."
            return False

    def find_inventory_item(self,e):

        if self.inside_inventory():

            #KALLE: Lägg på marginalen 50 från skärmens övre kant
            row = (self._e.pos[1]-50)/INV_H

            #KALLE: Lägg på marginalen 75 från skärmens vänstra kant
            n = (self._e.pos[0]-75)/INV_W 
            #KALLE: Och så rätt rad...
            n += 6*row

            #KALLE: Fulhack för att vi inte vill ha mer än 4 (0-3) rader.
            if n < len(self.game.data['inv']) and row < 4:
                return self.game.data['inv'][n]
    

    def event_inv(self,e):

        #KALLE: Notering: Dölj inventoryt när man för musen utanför och håller en item i handen
        if self.showinventory and self.item and self.inside_inventory() == False:
            self.showinventory = False
            return

        #KALLE: Notering: Släpp/lägg tillbaka utanför inventoryt
        if e.type is MOUSEBUTTONDOWN and self.item != None:
            b1,b2,b3 = pygame.mouse.get_pressed()
            #TODO: Check if mouse is hover over another item and if so, use
            #self.item with that item.
            if self.showinventory:
                if b1:
                    combine_item_a = self.item
                    combine_item_b = self.find_inventory_item(e)
                    if combine_item_b != self.item and combine_item_b != None:
                        fnc = 'combine_%s_%s'%(combine_item_a,combine_item_b)
                        if hasattr(self,fnc):
                            r = getattr(self,fnc)()
                            if r != False: return r
                elif b3:
                    print "Put back ",self.item,"in inventory"
                    self.item = None
                    return
            else:
                if b1:
                    for hover in self.find(e.pos):
                        fnc = '%s_%s'%(self.item,hover)
                        if hasattr(self,fnc):
                            r = getattr(self,fnc)()
                            if r != False: return r
                        else:
                            return getattr(self,"use_default")()
                    return
                elif b3:
                    print "Put back ",self.item,"in inventory"
                    self.item = None
                    self.showinventory = False
                    return                

        #KALLE: Notering: flytta items i inventoryt
        if e.type is MOUSEBUTTONDOWN and self.inside_inventory():
            #self.game.data['inv'].append(self.item)
            item = self.item
            self.item = None
            if item in self.inv:
                self.inv.remove(item)
            self.inv.append(item)
            self.sfx('get')
            self.showinventory = True
            return
        
    def event_play(self,e):
        pass
        
            
    def goto(self,name,value=None):
        if type(name) != str:
            self._goto = name
            return
        if value == None:
            value = self.name
        r = __import__('rooms.%s'%name,globals(),locals(),['Room'])
        self._goto = r.Room(self.game,value)
    
    def x_play(self):
        self.mode = 'play'
        item = self.item
        self.item = None
        _done = False
        while not _done:
            _done = True
            for o in self.objs.values()[:]:
                if len(o.path) or o.text != None: _done = False
            self.loop()
            self.paint(self.game.screen)
            self.game.tick()
            #there has got to be a better way... but it's probably hard to understand ;)
            for e in pygame.event.get():
                pass
        self.item = item
        self.mode = 'normal'
        return
                
    def wait(self):
        _done = True
        for o in self.objs.values()[:]:
            if len(o.path) or o.text != None or o.animating == True: _done = False
        return _done

    def talkto(self,fnc,topic):
        return self.talk(fnc,topic)
        
    def say(self,text):
        parts = text.split(":")
        if len(parts) > 1:
            name = parts.pop(0)
        else:
            name = 'player'
        text = ":".join(parts)
        for o in self.objs.values():
            o.text = None
            o.text_timer = 0
        self.objs[name].talking = True
        self.objs[name]._say(text)
        
    def script(self,script):
        self.goto(Script(self.game,self,script,self))
        
    def talk(self,fnc,topic):
        self.goto(Talk(self.game,self,fnc,topic,self))
        
    def got(self,item):
        if item not in self.inv:
            self.inv.append(item)
        #KALLE: Makes items go straight to the inventory, instead of having to
        # place them there manually.
        #self.item = item
        
    def lost(self,item):
        if item in self.inv: self.inv.remove(item)
        if self.item == item:
            self.item = None
            
    def sfx(self,name,loops=0):
        self.game.sfx(name,loops)
    def sfx_stop(self,name):
        self.game.sfx_stop(name)
        
    def music(self,name):
        self.game.music(name)
        

class Room(Level):
    def __init__(self,game,name,value):
        self.name = name
        Level.__init__(self,game,self.name)
        if self.name not in self.game.data:
            self.game.data[self.name] = {}
        self.data = self.game.data[self.name]
        self.inv = self.game.data['inv']
        self.info = self.game.data['info']
        self.value = value
        

class Script(engine.State):
    def __init__(self,game,room,script,next):
        self.game,self.room,self.next = game,room,next
        self.script = []
        self.nextline = False
        for line in script:
            if type(line) == str:
                self.script.append((self.room.say,line,))
                self.script.append((self.room.wait,))
            else:
                self.script.append(line)
                self.script.append((self.room.wait,))
        self.skip = False
        
    def loop(self):
        if not self.skip: return self._loop()
        r = None
        while r == None:
            r = self._loop()
        return r
        
    def _loop(self):
        if len(self.script) == 0:
            return self.next
        todo = self.script[0]
        fnc = todo[0]
        params = todo[1:]
        r = fnc(*params)
        #Tommy: Ugly hack to skip a single line if the mouse is clicked. Check
        # the method "event" to see where self.nextline comes from.

        if r != False:
            self.script.pop(0)

        if self.nextline == True and len(self.script) != 0:
            #KALLE: Make everyone stop talking
            for obj in self.room.objs.values():
                if obj.talking:
                    obj.talking = False
                    obj.text = None
                    obj.text_timer = 0
            self.nextline = False
            self.script.pop(0)

        r = self.room.loop()
        return r
        
    def paint(self,screen):
        self.room.paint_main(screen)
        screen.fill((0,0,0),(0,480,640,0))
        pygame.display.flip()
        
    def update(self,screen):
        self.paint(screen)
        
    def event(self,e):
        if e.type is KEYDOWN and e.key is K_SPACE:
            self.skip = True
        elif e.type is MOUSEBUTTONDOWN:
            self.nextline = True


class Talk(engine.State):
    def __init__(self,game,room,fnc,topic,next):
        self.game,self.room,self.fnc,self.topic,self.next = game,room,fnc,topic,next
        
    def init(self):
        opts = self.fnc(self.topic)
        self.opts = opts

    def loop(self):
        self.init()
        if not len(self.opts):
            return self.next

    def paint(self,screen):
        self.game.currentcursor = "default"
        self.room.paint_main(screen)
        #screen.fill((0,0,0),(0,400,640,80))
        fnt = self.game.font
        pos = pygame.mouse.get_pos()
        n = 0
        #TOMMY: Here be dragons. Also calculates the area needed in order to
        # be able to draw all options. The y value should somehow be sent
        # to the event method. 
        y = 480 - (len(self.opts)*20)
        hover = (pos[1]-y) / 20

        x = 10
        for text in self.opts: 
            c = Color("#eeeeecff")
            c_shadow = Color("#323331ff")
            if n == hover:
                c = Color("#fc4303ff")
                c_shadow = Color("#3d1b0eff")
            #KALLE: Add a nice shadow
            screen.blit(fnt.render(text[0],1,c_shadow),(x+1,y+1))
            img = fnt.render(text[0],1,c)
            screen.blit(img,(x,y))
            y += 20
            n += 1
        pygame.display.flip()
    
    def update(self,screen):
        self.paint(screen)
        
    def event(self,e):
        #KALLE: Dialog alternatives
        if e.type is MOUSEBUTTONDOWN:
            #TOMMY: Hack to get the hover to sync up with the dynamic dialogue area.
            # Should really get the y value from the paint method.
            y = 480 - (len(self.opts)*20)
            n = (e.pos[1]-y) / 20
            if n < 0 or n >= len(self.opts): return

            text,script,topic = self.opts[n]
            self.topic = topic
            self.init()
            if script[0] == None: script[0] = text
            return Script(self.game,self.room,script,self)
        
        #Tommy: Chooses dialog option using 1-9 buttons. Does not work with
        # the numpad.
        if e.type is KEYDOWN:
            if 48 < e.key < 58:
                n = e.key-49
                text,script,topic = self.opts[n]
                self.topic = topic
                self.init()
                if script[0] == None: script[0] = text
                return Script(self.game,self.room,script,self)
            

if __name__ == '__main__':
    s = pygame.display.set_mode((SW,SH))
    
    import sys
    src = sys.argv[1]
    l = Level(None,src)
    l.init()
    l.layers_build()
    l.layers_save()
    
#     from pgu import timer
#     t = timer.Timer(FPS)
#     
#     #l.init()
#     #l.layers_build()
#     #l.layers_save()
#     l.init()
#     
#     #p = Obj(os.path.join("data","test","player"),(128,128))
#     
#     #l.sprites.append(p)
#     p = l.objs['player']
#     
#     _quit = False
#     while not _quit:
#         for e in pygame.event.get():
#             if e.type is QUIT or (e.type is KEYDOWN and e.key == K_ESCAPE): _quit = True
#             
#         keys = pygame.key.get_pressed()
#         inc = 8
#         if keys[K_UP]: p.rect.y -= inc
#         if keys[K_DOWN]: p.rect.y += inc
#         if keys[K_LEFT]: p.rect.x -= inc
#         if keys[K_RIGHT]: p.rect.x += inc
#         
#         l.follow(p)
#         l.paint(s)
#         
#         pygame.display.flip()
#         
#         t.tick()
    
    
