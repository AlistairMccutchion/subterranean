#coding: -utf-8-
import level

class Room(level.Room):
    def __init__(self,game,value):
        level.Room.__init__(self,game,__name__.split('.')[-1],value)
    
    def init(self):
        level.Level.init(self)
        
        #self.music('default')
        print self.data
        
        self.player = self.objs['player']
        for o in self.objs.values():
            if 'del_%s'%o.name in self.data: del self.objs[o.name]
        if self.value not in ('title',None):
            pos = self.objs['%s_pos'%self.value].pos

        if 'rockplaced' not in self.data:
            self.rockhole = self.objs['rockhole']
            del self.objs['rockhole']

    def look_hole(self):
        self.script([
            """player:I wonder what that hole is for...""",
            ])

    def rock_hole(self):
        self.player.walkto('hole_pos',self._rock_hole)

    def _rock_hole(self):
        self.script([
            """player:It fits perfectly!""",
            ])
        self.lost('rock')
        self.objs['rockhole'] = self.rockhole
        self.data['rockplaced'] = 1
        self.game.data['rockplaced'] = 1
        #KALLE: self.data applies to this room, self.game.data to the entire
        # game.

    def use_sewer(self):
        self.player.walkto('sewer_pos',self._use_sewer)
    def _use_sewer(self):
        self.goto('sewer')
        
