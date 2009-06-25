#coding: -utf-8-
import level
import random

class Room(level.Room):
    def __init__(self,game,value):
        level.Room.__init__(self,game,__name__.split('.')[-1],value)

    def arn(self):
        print "BAR!"
        self.player.walkpos('npc_grumpyman')
    
    def init(self):
        level.Level.init(self)

        self.player = self.objs['player']
        self.grumpyman = self.objs['npc_grumpyman']
        #KALLE: I know, we should define this somewhere else. See "Issues" on github.
        self.player.text_color = "#ffffffff"
        self.grumpyman.text_color = "#8ae234ff"
        self.objs['thinking'].text_color = "#729fcfff"

        self.objs["bulbleft"].state = "r"
        self.objs["bulbmiddle"].state = "r"
        self.objs["bulbright"].state = "r"

        self.got('potion')
        self.got('worm')

        #self.player.can_walk = False
        #self.player.state = "omg"


        self.script([
            (self.player.animate,'omg'),
            """npc_grumpyman:Foobar! I am so sick and tired of you right now! Where are the files!?""",
            (self.player.walkpos,'npc_grumpyman'),
            """player:Um, Sir... What files?""",
            """npc_grumpyman:Argh! The ELDERSTEIN files! The files that were supposed to be on my desk yesterday!""",
            """player:Ah, sorry. My bad. Of course I have those files ready.""",
            """thinking:(I have NO idea what he's talking about.)""",
            (self.player.animate,'omg'),
            """npc_grumpyman:Hurry up! I will stay here until you show those files to me!""",
            """player:...Of course, boss! Let me just get the files from my computer!""",
            (self.player.walkpos,'computer'),
            (self.player.animate,'omg')
            ])

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
                    """player: Now I remember! Blue Orange Blue! BOB!""",
                    ])
                self.objs["computer"].state = "on"

    def look_computer(self):
        if "puzzle_complete_bulbs" in self.info:
            self.player.face("computer")
            self.script([
                """player: It's online! Now I can access those files!"""
                ])
        else:
            self.player.face("computer")
            self.script([
                """player: I need to enter my personal password to use it."""
                ])

    def use_computer(self):
        if "puzzle_complete_bulbs" in self.info:
            self.player.face("computer")
            self.script([
                """player: Let me see...""",
                """player: Ah, there are the files!""",
                ])
            self.info.append("puzzle_got files")
        else:
            self.player.face("computer")
            self.script([
                """player: I need to enter my personal password to use it."""
                ])
    def use_note1(self):
        self.look_note1()

    def use_note2(self):
        self.look_note2()

    def use_note3(self):
        self.look_note3()

    def look_note1(self):
        self.player.face("note1")
        self.script([
            """note1: BOB was here!"""
            ])
        self.info.append("puzzle_got_clue")

    def look_note2(self):
        self.player.face("note2")
        self.script([
            """note2: Don't forget to collect data for the Elderstein project!.""",
            """player: Uh oh..."""
            ])

    def look_note3(self):
        self.player.face("note3")
        self.script([
            """note3: Remember, rock always beats scissors."""
            ])

    def use_npc_grumpyman(self):
        if "free_to_leave" not in self.info:
            self.player.walkpos('npc_grumpyman',self._use_npc_grumpyman)
        else:
            self.script([
                """think:(I should just leave him alone and get those files.)"""
            ])

    def _use_npc_grumpyman(self):
        #self.say("""npc_grumpyman:Whatcha lookin' at?""")
        self.talkto(self.talk_npc_grumpyman,'first')

    def foodtalk(self):
        if 'food' not in self.info:
            self.info.append('food')
    def givechili(self):
        if 'chili' not in self.inv:
            self.got('chili')
    def free_to_leave(self):
        self.info.append("free_to_leave")
    
    def talk_npc_grumpyman(self,topic):
        opts = []
        if topic == "first":
            opts.append((
                    """You look kind of big for a dwarf...""",[None,
                    """npc_grumpyman:I'm big boned, so what!?""",
                    """player:Nothing!""",
                    ],'first'))
            if 'puzzle_complete_bulbs' not in self.info:
                opts.append((
                        """I can't remember my password.""",[None,
                        """npc_grumpyman:Aren't you good for anything, you bastard? You'd better remember - or I'll make you!""",
                        """player:Oh, er... now I remember!""",
                        """thinking:(I seriously need to figure this out. Soon.)""",
                        ],'first'))
            if 'puzzle_got files' in self.info:
                opts.append((
                        """Here are the files!""",[None,
                        """npc_grumpyman:Let me have a look...""",
                        """npc_grumpyman:Just two pages? Are you kidding me!? """,
                        """player:No, sorry. I- need to talk with... S- Sandra, about that.""",
                        """npc_grumpyman:Summers? You mean she has the rest of the data?""",
                        """player:Yes, exactly!""",
                        """npc_grumpyman:Aargh, then get go and get it you worthless hippie!""",
                        """npc_grumpyman:You have fifteen minutes. If I don't have that report on my desk by then, you're toast!""",
                        """player:Yes, Sir! Going now, Sir!""",
                        """thinking:(What a mess!)""",
                        (self.free_to_leave,)]
                        ,'exit'))
            if 'puzzle_got_clue' in self.info:
                opts.append((
                        """Do you know who Bob is?""",[None,
                        """npc_grumpyman:Who? We don't have any Bob working here!""",
                        ],'first'))
            if 'worm' in self.info and 'food' not in self.info:
                opts.append((
                    """Did you really eat that worm?""",[None,
                    """npc_grumpyman:Yup. Now get me those files!""",
                    (self.foodtalk,)
                    ],'first'))
            if 'food' in self.game.data['info'] and 'worm' not in self.inv and 'chili' not in self.inv and 'firepotion' not in self.inv:
                opts.append((
                    """Is there anything you won't eat?""",[None,
                    """npc_grumpyman:Argh! There be but one thing...""",
                    """npc_grumpyman:This blasted chili fruit! Here, you can have it!""",
                    (self.givechili,)
                    ],'first'))
            opts.append((
                """I'll be right back, Sir!""",[None,]
                ,'exit'))
        return opts

    def use_default(self):
        responses = ["That didn't work.","Hmm... No.","Not working.","I'm not sure how I can do that.","Nah."]
        random.shuffle(responses)
        self.script([
            "player:"+responses[1]
            ])

    def look_npc_grumpyman(self):
        self.script([
            """player:Mr.Grumpley: The horror of the seven floors."""
            ])

    def worm_npc_grumpyman(self):
        self.lost('worm')
        self.info.append('worm')
        self.script([
            """npc_grumpyman:Oh thank ye, 'tis my favourite! You're not trying to bribe me, are ye?"""
            ])

    def examine_chili(self):
        self.script([
            """player:That chili fruit looks really hot!""",
            """player:...and not in the good sense of the word."""
        ])

    def chili_npc_grumpyman(self):
        self.script([
            """npc_grumpyman:Oh no! That be much too spicy for ol' me!"""
        ])

    def chili_player(self):
        self.script([
            """player:That's way too hot for me!"""
            ])

    def examine_worm(self):
        self.script([
            """player:Eww. Wriggly."""
            ])

    def examine_potion(self):
        self.script([
            """player:Potion of health (500+)."""
            ])

    def worm_dropzone(self):
        self.player.walkpos('dropzone',self._worm_dropzone)

    def _worm_dropzone(self):
        self.lost('worm')
        self.script([
            """player:There goes the worm. Bye little fellow!"""
            ])

    def use_item_rock(self):
        del self.objs['item_rock']
        self.got('item_rock')

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

    #FIXME Later: This is buggy.
    def use_bulbleft(self):
        #self.player.walkpos('bulbleft',self._use_bulbleft)
        self.togglebulb("bulbleft")

    def _use_bulbleft(self):
        self.togglebulb("bulbleft")

    def use_bulbmiddle(self):
        #self.player.walkpos('bulbmiddle',self._use_bulbmiddle)
        self.togglebulb("bulbmiddle")

    def _use_bulbmiddle(self):
        self.togglebulb("bulbmiddle")

    def use_bulbright(self):
        #self.player.walkpos('bulbright',self._use_bulbright)
        self.togglebulb("bulbright")

    def _use_bulbright(self):
        self.togglebulb("bulbright")

    def look_bulbleft(self):
        self.script([
            """player:It's a button for the computer password."""
            ])

    def look_bulbmiddle(self):
        self.script([
            """player:It's a button for the computer password."""
            ])

    def look_bulbright(self):
        self.script([
            """player:It's a button for the computer password."""
            ])
    def use_exit_north(self):
        if "free_to_leave" in self.info:
            print "END!"
            #self.player.walkpos('exit_north',self._use_exit_north)
            #self._use_exit_north
        else:
            self.script([
            """npc_grumpyman:No way!"""
            ])
    def _use_exit_north(self):
        self.goto('office')
