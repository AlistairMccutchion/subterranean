#coding: -utf-8-
import level
import random

class Room(level.Room):
    def __init__(self,game,value):
        level.Room.__init__(self,game,__name__.split('.')[-1],value)
    
    def init(self):
        level.Level.init(self)

        self.player = self.objs['player']
        self.grumpyman = self.objs['grumpyman']

        self.objs["bulbleft"].state = "r"
        self.objs["bulbmiddle"].state = "r"
        self.objs["bulbright"].state = "r"

        self.got('potion')
        self.got('worm')

    def checkbulbs(self):
        return self.objs["bulbleft"].state == "b" and self.objs["bulbmiddle"].state == "o" and self.objs["bulbright"].state == "b"

    def togglebulb(self,bulb):
        if "puzzle_complete_bulbs" not in self.info:
            #print "toggling",bulb
            #hacky, I know. It was very late :)
            if self.objs[bulb].state == "r": self.objs[bulb].state = "y"
            elif self.objs[bulb].state == "y": self.objs[bulb].state = "o"
            elif self.objs[bulb].state == "o": self.objs[bulb].state = "g"
            elif self.objs[bulb].state == "g": self.objs[bulb].state = "b"
            elif self.objs[bulb].state == "b": self.objs[bulb].state = "r"

            if self.checkbulbs() and "puzzle_got_clue" in self.info:
                self.info.append("puzzle_complete_bulbs")
                self.script([
                    """player: Now I get it! Blue Orange Blue! BOB!""",
                    """grumpyman: Well done, laddie. Even I couldn't figure that one out. Here, take this silver key!"""
                    ])
                self.got('key')

    def use_sign(self):
        self.player.walkpos('sign',self._use_sign)

    def _use_sign(self):
        self.script([
            """sign: BOB was here!"""
            #"""player: Hmm... Why is BOB written in uppercase?""",
            ])
        self.info.append("puzzle_got_clue")

    def use_grumpyman(self):
        self.player.walkpos('grumpyman',self._use_grumpyman)

    def _use_grumpyman(self):
        #self.say("""grumpyman:Whatcha lookin' at?""")
        self.talkto(self.talk_grumpyman,'first')

    def foodtalk(self):
        if 'food' not in self.info:
            self.info.append('food')
    def givechili(self):
        if 'chili' not in self.inv:
            self.got('chili')
    
    def talk_grumpyman(self,topic):
        opts = []
        if topic == "first":
            opts.append((
                    """You look kind of big for a dwarf...""",[None,
                    """grumpyman:I'm big boned, so what!?""",
                    ],'first'))
            if 'puzzle_complete_bulbs' not in self.info:
                opts.append((
                        """What are those bulbs for?""",[None,
                        """grumpyman:It's a puzzle. I'm not able to solve it myself. Solve it for me and get a prize!""",
                        ],'first'))
            if 'puzzle_complete_bulbs' in self.info:
                opts.append((
                        """I figured out the puzzle!""",[None,
                        """grumpyman:Yes, you already told me that. Go play somewhere else!""",
                        ],'first'))
            if 'puzzle_got_clue' in self.info:
                opts.append((
                        """Do you know who this BOB guy is?""",[None,
                        """grumpyman:Nope, I haven't been able to figure that out.""",
                        ],'first'))
            if 'worm' in self.info and 'food' not in self.info:
                opts.append((
                    """Did you really eat that worm?""",[None,
                    """grumpyman:Yup. T'was delicious too!""",
                    (self.foodtalk,)
                    ],'first'))
            if 'food' in self.game.data['info'] and 'worm' not in self.inv and 'chili' not in self.inv:
                opts.append((
                            """Is there anything you won't eat?""",[None,
                            """grumpyman:Argh! There be but one thing...""",
                            """grumpyman:This blasted chili fruit! Here, you can have it!""",
                            (self.givechili,)
                            ],'first'))
            opts.append((
                """I've got lots to do. So... See ya!""",[None,]
                ,'exit'))
        return opts

    def use_default(self):
        responses = ["That didn't work.","Hmm... No.","Not working.","I'm not sure how I can do that.","Nah."]
        random.shuffle(responses)
        self.script([
            "player:"+responses[1]
            ])

    def look_grumpyman(self):
        self.script([
            """player:Wow, that's a big dwarf!"""
            ])

    
    def worm_grumpyman(self):
        self.lost('worm')
        self.info.append('worm')
        self.script([
            """grumpyman:Oh thank ye, 'tis my favourite!"""
            ])
    def rock_grumpyman(self):
        self.lost('rock')
        self.script([
            """grumpyman:Ouch! Why'd you throw that at me, you asshole!?"""
            ])

    def examine_chili(self):
        self.script([
            """player:That chili fruit looks really hot!""",
            """player:...and not in the good sense of the word."""
        ])

    def chili_grumpyman(self):
        self.script([
            """grumpyman:Oh no! That be much too spicy for ol' me!"""
        ])

    def chili_dropzone(self):
        self.lost('chili')
        self.script([
            """I'm surprised it didn't catch on fire."""
            ])

    def chili_player(self):
        self.script([
            """player:That's way too hot for me!"""
            ])

    def use_rock(self):
        self.player.walkpos('rock',self._use_rock)

    def _use_rock(self):
        del self.objs['rock']
        self.data['del_rock'] = 1
        self.got('rock')

    def look_rock(self):
        self.player.face("rock")
        self.script([
            """player:It's a rock."""
            ])

    def examine_rock(self): 
        self.script([
            """player:This rock rocks!"""
            ])

    def examine_worm(self):
        self.script([
            """player:Eww. Wriggly."""
            ])

    def examine_potion(self):
        self.script([
            """player:Potion of health (500+)."""
            ])

    def examine_key(self):
        self.script([
            """player:One key to rule them all!."""
            ])

    def key_dropzone(self):
        self.lost('key')
        self.script([
            """player:I dropped the key in the zone. Bye bye."""
            ])

    def worm_dropzone(self):
        self.lost('worm')
        self.script([
            """player:There goes the worm. Bye little fellow!"""
            ])

    def rock_dropzone(self):
        self.lost('rock')
        self.script([
            """player:I'm glad to be rid of this goddamn rock."""
            ])

    def potion_dropzone(self):
        self.lost('potion')
        self.script([
            """player:Now the dropzone gains 500 hp. Neat."""
            ])

    def potion_player(self):
        self.lost('potion')
        self.script([
            """player:Ah! 500hp plus. I AM INVINCIBLE"""
            ])

    def worm_player(self):
        self.script([
            """player:Eat... a ... worm? Are you stupid?"""
            ])
    
    def combine_chili_potion(self):
        self.lost('chili')
        self.lost('potion')
        self.got('firepotion')
        self.script([
            """Whoa! It caught on fire!""",
            """Sweet, it's a fire potion!"""
            ])

    def use_bulbleft(self):
        self.togglebulb("bulbleft")

    def use_bulbmiddle(self):
        self.togglebulb("bulbmiddle")

    def use_bulbright(self):
        self.togglebulb("bulbright")

    def look_bulbleft(self):
        self.script([
            """player:It's a light bulb."""
            ])

    def look_bulbmiddle(self):
        self.script([
            """player:It's a light bulb."""
            ])

    def look_bulbright(self):
        self.script([
            """player:It's a light bulb."""
            ])

    def use_exit(self):
        self.player.walkto('exit_pos',self._use_exit)
    def _use_exit(self):
        self.goto('sewer')
