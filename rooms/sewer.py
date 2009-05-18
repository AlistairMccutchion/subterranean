import level

class Room(level.Room):
    def __init__(self,game,value):
        level.Room.__init__(self,game,__name__.split('.')[-1],value)
    
    def init(self):
        level.Level.init(self)
        
        self.music('swamp')
        
        self.player = self.objs['player']
        for o in self.objs.values():
            if 'del_%s'%o.name in self.data: del self.objs[o.name]
        if self.value not in ('title',None):
            pos = self.objs['%s_pos'%self.value].pos
            self.player.rect.centerx,self.player.rect.bottom = pos

    def use_rock(self):
        self.player.walkpos('rock',self._use_rock)



    def look_rock(self):
        self.player.face("rock")
        self.script([
            """player:It's a rock."""
            ])

    def _use_rock(self):
        del self.objs['rock']
        self.data['del_rock'] = 1
        self.got('rock')
    def use_goo(self):
        self.script([
            """player:I am not touching that.""",
            ])
    def look_goo(self):
        self.player.face("goo")
        self.script([
            """player:This is where the green stuff must be coming from.""",
            """sewerend_pos:Totally!.""",
            """player:Huh? Who goes there?.""",
            ])

    def rock_goo(self):
        self.say("""That won't do any good!""")
            
    def use_mainst(self):
        self.player.walkto('mainst_pos',self._use_mainst)
    def _use_mainst(self):
        self.goto('mainst')

    def use_sewerend(self):
        self.player.walkto('sewerend_pos',self._use_sewerend)
    def _use_sewerend(self):
        self.goto('sewerend')
        
