import random as r
import math as m
import time as t
import base64

# go easy on me i had two days to make this 🥺
# also idk if i had to do this much but im bored and i love scripting!!!!
# oh yeah theres so many comments because i need a break from logic theres too much logic help meee

if (not globals().get('isJS')): # browser port features
    globals()["isJS"] = False

"╔═╗ ║ ╚╦╩╝ ╠╬╣╌╎"

locations = list("abcdefghijklmnpq")

inventory = []
location = "n"

key = """\
  ╬  wall        n
  ╎  door      w + e
  o  you         s
  !  important
"""

# please please PLEASE tell me yall have an ansi supported console
# these are self explanitory and i lowkey had to go reference an ansi chart
def hideCursor(): # cursor look bad
    print("\033[?25l", end="", flush=True)
def showCursor(): # nvm we need the cursor so the player knows to type
    print("\033[?25h", end="", flush=True)
def deleteLastLine(): # VERY IMPORTNAT DO NOT DELEtE
    print("\033[A\033[K", end="", flush=True)

# smooth!!!!!! this is only used in text typewriter btw
def easeOutCubic(x):
    return 1 - m.pow(1 - x, 4)

# ...
def ellipsis():
    t.sleep(0.75)
    for _ in range(3):
        print(".", end="", flush=True)
        t.sleep(0.5)
    print()

navigate = False
options = {}

# anonymous function SIMULATOR [2028 working] (NEW!) hacked
def navigateTo(place, dir):
    global location, navigate
    
    def setPlace():
        global location, navigate
        location = place
        navigate = True
        story(f'You walk {dir}.')
    return setPlace

# multiple typewriter at once
def handleOptions():    
    for i in range(21):
        # probably not the BEST way to do the async typewriter effect?
        # oh well im too lazy to download asyncio
        for (k, v) in options.items():
            x = easeOutCubic(i / 20)
            str = f"{k} - {v[0]}"
            print(str[:m.ceil(x * len(str))], flush=True)
        if i != 20:
            t.sleep(0.05)
            for n in range(len(options)):
                deleteLastLine() # this causes occasional stutter in output idk why python is weird like that
    showCursor()
    while True:
        choice = input()
        if options.get(choice):
            deleteLastLine()
            options.get(choice)[1]()
            break
        else:
            deleteLastLine()
            # can the player PLEASE be reasonable and not do weird magic stuff
            story(f"({choice} isn't a valid choice! Try again.)", True)
    hideCursor()

# the ultimate variable eater (five hundred variables = 1 dictionary)
# handles and keeps track of important events in the story
storyEvents = {}

# function to handle the description of where you are
def description():
    global options
    
    # aaaaghghhh python equivalent of js switch when
    if location == 'n':
        story("You woke up here. The air is freezing. Laying on the stone floor is uncomfortable.", True)
        if 'bluekey' in inventory:
            story("There's a ventilation duct behind you. It blasts air at your face.", True)
        else:
            story("There's a ventilation duct behind you. It contains a blue key.", True)
        def o1(): # this language sucks where are my anonymous functionssss
            story('You check the vent.', True)
            if storyEvents.get('bluekey'):
                story('The inside is walled with metal.', True)
                story('Darkness stares back at you.', True)
            else:
                if 'stick' in inventory:
                    story("Luckily, you now have the stick to grab the key.", True)
                    story("Your paws make it hard to move the stick around.")
                    ellipsis()
                    story("After a bit of difficulty,", True)
                    story("You got the blue key!")
                    storyEvents["bluekey"] = True
                    storyEvents['bluekeyobjective'] = False
                    inventory.append('bluekey')
                else:
                    ellipsis()
                    story("You can't quite reach the blue key.", True)
                    story("You need something long to reach it, as your arm can't fit through the ventilation cover.", True)
        options = {
            'north': ('Head north.', navigateTo('j', 'north')),
            'east': ('Head east.', navigateTo('p', 'east')),
            '1': ('Check the vent behind you.', o1)
        }
    elif location == 'j':
        story("There's a door to the east.", True)
        if storyEvents.get('jdoor'):
            story("It's open.", True)
        else:
            story("It's locked with a blue lock.", True)
        def o2():
            story("You hold your candle up to the lock.", True)
            story("The wax drips out onto the floor.")
            if options.get("2"):
                del options["2"]
            storyEvents['meltedlock'] = True
        def updateOptions():
            global options
            
            options = {
                'south': ('Head south.', navigateTo('n', 'south')),
            }
            if storyEvents.get('jdoor'):
                options['east'] = ('Head east.', navigateTo('k', 'east'))
            else:
                if storyEvents.get('attemptedjdoor') and ('candle' in inventory) and not storyEvents.get('meltedlock'):
                    options["2"] = ('Melt the wax.', o2)
                if 'bluekey' in inventory:
                    options["1"] = ('Unlock the door.', o1)
        def o1():
            story("You try to unlock the door.", True)
            ellipsis()
            if storyEvents.get('meltedlock'):
                story("The door clicks open.")
                storyEvents['jdoor'] = True
            else:
                story('The key is blocked by some sort of waxy substance.', True)
                story('Maybe it can be melted?')
                storyEvents['attemptedjdoor'] = True
            updateOptions()
        updateOptions()
    elif location == 'q':
        story("There is a long hallway.", True)
        options = {
            'north': ('Head north.', navigateTo('m', 'north')),
            'west': ('Head west.', navigateTo('p', 'west')),
        }
    elif location == 'm':
        story("The breeze can be felt from here.", True)
        options = {
            'north': ('Head north.', navigateTo('i', 'north')),
            'south': ('Head south.', navigateTo('q', 'south')),
        }
    elif location == 'i':
        story("The hallway is bright here.", True)
        options = {
            'north': ('Head north.', navigateTo('e', 'north')),
            'south': ('Head south.', navigateTo('m', 'south')),
        }
    elif location == 'e':
        options = {
            'south': ('Head south.', navigateTo('i', 'south')),
        }
        def o1():
            story("There's a microphone near the doorknob.", True)
            story("There's a note saying \"The name of the cat who stays here?\"", True)
            story("Your response is:", True)
            showCursor()
            c = input()
            hideCursor()
            deleteLastLine()
            story(f"You: \"I think the answer is... '{c.strip().capitalize()}'.\"")
            correct = c.strip().lower() == "ashley"
            if correct:
                story("The door swings open.")
                del options["1"]
                storyEvents['edoor'] = True
                options["north"] = ('Head north.', navigateTo('win', 'north'))
            else:
                story("The door stays shut, and a buzzer sound emits from the door.")
        if storyEvents.get('edoor'):
            story("The door is open.", True)
            options["north"] = ('Head north.', navigateTo('win', 'north'))
        else:
            story("The door is locked with a puzzle.", True)
            options["1"] = ('Try unlocking the door.', o1)
    elif location == 'p':
        story("You come across a door and another hallway.", True)
        options = {
            'north': ('Head north.', navigateTo('d', 'north')),
            'west': ('Head west.', navigateTo('n', 'west')),
        }
        def o1():
            story("There's a number pad near the doorknob.", True)
            story("Enter the 4 digit code:", True)
            showCursor()
            c = input()
            hideCursor()
            if c.strip().isdigit() and len(c.strip()) == 4:
                ci = int(c.strip())
                deleteLastLine()
                correct = None
                if ci == 2296:
                    correct = True
                else:
                    correct = False
                
                ci = list(str(ci))
                # prob better way to do this too but im too lazy
                print(f"[ - - - ]")
                t.sleep(0.5 + r.random() * 0.25)
                deleteLastLine()
                print(f"[{ci[0]}- - - ]")
                t.sleep(0.5 + r.random() * 0.25)
                deleteLastLine()
                print(f"[{ci[0]}-{ci[1]}- - ]")
                t.sleep(0.5 + r.random() * 0.25)
                deleteLastLine()
                print(f"[{ci[0]}-{ci[1]}-{ci[2]}- ]")
                t.sleep(0.5 + r.random() * 0.25)
                deleteLastLine()
                print(f"[{ci[0]}-{ci[1]}-{ci[2]}-{ci[3]}]")
                t.sleep(0.5 + r.random() * 0.25)
                if correct:
                    story("The door swings open.")
                    options["east"] = ('Head east.', navigateTo('q', 'east'))
                    del options["1"]
                    storyEvents['pdoor'] = True
                    
                    if not storyEvents.get('talked'):
                        story("There's a cat coming out of the door.", True)
                        for i in range(5):
                            print()
                            t.sleep(0.25)
                        
                        draw_portrait()
                        story('Ashley: "You know..."')
                        story('Ashley: "It would be nicer to play through the game."')
                        story('Ashley: "Rather than... looking through the code."')
                        story('Ashley: "I can\'t tell if you\'ve played this before. Sorry to those of you."')
                        story('Ashley: "Please don\'t cheat."')
                        story('Ashley: "I\'ll let you go now."')
                        story('Ashley: "Take this."')
                        story("You got the map.")
                        inventory.append('map')
                else:
                    story("The door stays shut, and a buzzer sound emits from the keypad.")
            else:
                story("The code doesn't fit in the door.")
        if storyEvents.get('pdoor'):
            story("The door is open.", True)
            options["east"] = ('Head east.', navigateTo('q', 'east'))
        else:
            story("The door is locked with a combination code.", True)
            options["1"] = ('Try unlocking the door.', o1)
    elif location == 'd':
        story("You look at the window.", True)
        story("A soft reflection glares back at you.", True)
        options = {
            'south': ('Head south.', navigateTo('p', 'south')),
            'west': ('Head west.', navigateTo('c', 'west')),
        }
    elif location == 'k':
        story("It's wet in here.", True)
        story("Your fur is now soggy.", True)
        options = {
            'east': ('Head east.', navigateTo('l', 'east')),
            'west': ('Head west.', navigateTo('j', 'west')),
        }
    elif location == 'l':
        options = {
            'west': ('Head west.', navigateTo('k', 'west')),
        }
        if not 'sledgehammer' in inventory:
            story("There seems to be a sledgehammer here.", True)
            def o1():
                story("You take the sledgehammer.", True)
                story("There's nothing left in the room.")
                del options['1']
                inventory.append('sledgehammer')
            options['1'] = ('Grab the sledgehammer', o1)
        else:
            story("There's nothing.", True)
    elif location == 'h':
        options = {
            'north': ('Head north.', navigateTo('c', 'north')),
        }
        if not 'candle' in inventory:
            story("There's a candle.", True)
            def o1():
                story("You take the candle.", True)
                story("There isn't a candle in the room anymore.")
                del options['1']
                inventory.append('candle')
            options['1'] = ('Candle', o1)
        else:
            story("There isn't a candle.", True)
    elif location == 'c':
        if storyEvents.get('cdoor'):
            story("The sunlight here is dim, but you can see a door, which is now open.", True)
        else:
            story("The sunlight here is dim, but you can see a door, which has a blue lock on it.", True) # soccer anime ref maybe
        story("Past this point, the sunlight ends and it's really dark.", True)
        options = {
            'east': ('Head east.', navigateTo('d', 'east')),
            'west': ('Head west.', navigateTo('b', 'west')),
        }
        if storyEvents.get('cdoor'):
            options['south'] = ('Head south.', navigateTo('h', 'south'))
        else:
            if 'bluekey' in inventory:
                def o1():
                    story("You unlock the door.")
                    storyEvents['cdoor'] = True
                    del options['1']
                    options['south'] = ('Head south.', navigateTo('h', 'south'))
                options['1'] = ('Unlock the door', o1)
    elif location == "g":
        story("There is a cat across the room typing on what looks to be a mini-laptop.", True)
        story("She has a slice of pizza in her paw. There is a half-empty pizza box nearby.", True)
        def o1():
            if storyEvents.get("talked"):
                story("She looks more mad than before.", True)
                story("You think to yourself that you should probably leave her alone.")
            else:
                story("You go and talk to her.")
                for i in range(5):
                    print()
                    t.sleep(0.25)
                
                draw_portrait()
                story('???: "Hello?"')
                story('You: "Hi! Who are you?"')
                story('???: "My name?"')
                story('Ashley: "You can call me \'Ashley\'."')
                story('Ashley: "What do you want?"')
                story('You: "Whatcha doing?"')
                story('Ashley: "Well, I\'m making this thing..."')
                t.sleep(0.25)
                print()
                t.sleep(0.25)
                story("(You naturally stopped listening to what she was saying.)")
                story("(She started talking about these 'pythons' and how they run.)")
                story('(You think to yourself that this is nonsense.)')
                story('(And snakes are scary.)')
                t.sleep(0.25)
                print()
                t.sleep(0.25)
                story('Ashley: "Hello? Are you even istening?"')
                story('You: "Oh... I\'m sorry."')
                story('Ashley: "What are you here for?"')
                story('You: "I need the code for the door."')
                story('Ashley: "Why didn\'t you just say that? It\'s 2296."')
                story('You: "You knew the code all along?"')
                story('You: "Why don\'t you come outside? This place sucks."')
                story('Ashley: "Well... I don\'t think this place sucks."')
                story('Ashley: "Its calm and dark in here. I love it."')
                story('You: "Ok. Thank you!!"')
                story('Ashley: "Alright. I\'ll see you next time."')
                for i in range(5):
                    print()
                    t.sleep(0.25)
                story("The code is 2296. Remember that.")
                storyEvents['talked'] = True 
        options = {
            'north': ('Head north.', navigateTo('b', 'north')),
            '1': ('Talk to her.', o1),
        }
    elif location == 'b':
        if (not storyEvents.get("wall")) and 'candle' in inventory:
            story("The candle reveals a miscolored wall with cracks in it.", True)
        else:
            story("You can't see anything.", True)
            story("But... you can smell the walls, and you know where you can go.", True)
        options = {
            'east': ('Head east.', navigateTo('c', 'east')),
            'west': ('Head west.', navigateTo('a', 'west')),
        }
        def o1():
            story("You break the wall down. It reveals a passageway.")
            options["south"] = ("Head south.", navigateTo('g', 'south'))
            del options['1']
            storyEvents["wall"] = True
        if not storyEvents.get("wall"):
            if 'map' in inventory:
                story("Oddly enough, there's a door marked here on the map.", True)
                story("You reach out to touch it and it's a wall.", True)
            if 'sledgehammer' in inventory:
                options["1"] = ("Use the sledgehammer on the wall.", o1)
        else:
            options["south"] = ("Head south.", navigateTo('g', 'south'))
    elif location == 'a':
        if not ('candle' in inventory):
            story("You can't see anything.", True)
            story("But... you can smell the walls, and you know where you can go.", True)
        story("There's a hole in the wall, small enough that your kind can fit in, but not the humans.", True)
        story("Not much else going on here.", True)
        story("It's really empty here.", True)
        story("It's as if someone ran out of ideas for this area of the map.", True)
        story("On second thought, there's a spider in the corner, but that's it.", True)
        options = {
            'east': ('Head east.', navigateTo('b', 'east')),
            'south': ('Head south.', navigateTo('f', 'south')),
        }
    elif location == 'f':
        options = {
            'north': ('Head north.', navigateTo('a', 'north')),
        }
        if not storyEvents.get('trash'):
            story("It stinks in here.", True)
            story("There's a huge pile of trash here, though. It might explain the smell.", True)
            def o1():
                story("You dig through the pile of trash.")
                story("Your paws get dirty, but it's fine. Anything honestly to get out of here.")
                ellipsis()
                story("You find a map that looks like the outline of this place.", True)
                story("It might come in handy.")
                ellipsis()
                story("You find a stick!")
                del options['1']
                if options.get("2"):
                    del options["2"]
                storyEvents['trash'] = True
                storyEvents['bluekeyobjective'] = True
                inventory.append('stick')
                inventory.append('map')
            def o2():
                story("No.")
                storyEvents['yummy'] = True
                del options['2']
            options['1'] = ('Dig through the pile of trash.', o1)
            if not storyEvents.get('yummy'):
                options['2'] = ('Eat the trash?', o2)
        else:
            story("Nothing.", True)

# map
def map():
    mapThing = places.get(location) if (not ('map' in inventory)) else world
    mapThing = mapThing.replace(location, "o")
    if storyEvents.get('bluekeyobjective'): mapThing = mapThing.replace("n", "!")
    for v in locations:
        mapThing = mapThing.replace(v, " ")
    mapThing += key
    lines = mapThing.split("\n")
    lastChar = 0
    for i in range(50):
        x = easeOutCubic(i / 50)
        thisChar = m.ceil(x * len(lines))
        for l in range(lastChar, thisChar):
            print(lines[l])
        lastChar = thisChar
        t.sleep(0.02)

# its me!
def draw_portrait():
    lines = portrait.split("\n")
    lastChar = 0
    for i in range(50):
        x = easeOutCubic(i / 50)
        thisChar = m.ceil(x * len(lines))
        for l in range(lastChar, thisChar):
            print(lines[l])
        lastChar = thisChar
        t.sleep(0.02)
    print()

# thanka you so mucha for playing my game!
def draw_logo():
    lines = logo.split("\n")
    lastChar = 0
    for i in range(50):
        x = easeOutCubic(i / 50)
        thisChar = m.ceil(x * len(lines))
        for l in range(lastChar, thisChar):
            print(lines[l])
        lastChar = thisChar
        t.sleep(0.02)
    print()
        
# SPOILER SPOILER YOURE NOT MEANT TO SEE THIS IF YOU SEE THIS YOURE A CHEATER
world = """\
╔═══════════════╦═╌═╗
║ a   b   c   d ║ e ║
╠═ ═╦═╌═╦═╌═╗   ║   ║
║ f ║ g ║ h ║   ║ i ║
╠═══╬═══╩═══╣   ║   ║
║ j ╎ k   l ║   ║ m ║
║   ╚═══════╝   ║   ║
║ n           p ╎ q ║
╚═══════════════╩═══╝
"""

# arhgahrhgsrhso python sucks so im gonna do this the noob way
places = {
    'n': "║   ╚\n║ n  \n╚════\n",
    'j': "╠═══╬\n║ j ╎\n║   ╚\n",
    'p': "╝   ║\n  p ╎\n════╩\n",
    'd': "════╦\n  d ║\n╗   ║\n",
    'c': "═════\n  c  \n╦═╌═╗\n",
    'b': "═════\n  b  \n═════\n",
    'a': "╔════\n║ a  \n╠═ ═╦\n",
    'f': "╠═ ═╦\n║ f ║\n╠═══╬\n",
}

# typewriter/slowprint
def story(str, immediate = False):
    chars = list(str)
    lastChar = 0
    for i in range(m.floor(len(str)) + 1):
        x = easeOutCubic(i / m.floor(len(str)))
        thisChar = m.ceil(x * len(str))
        print(str[lastChar:thisChar], end="", flush=True)
        lastChar = thisChar
        t.sleep(0.01)
    if not immediate:
        print("\n(press Enter to continue)")
        t.sleep(0.01) # browser port need delay so people see enter to continue
        # python how do i track keypresses wihout library
        input()
        deleteLastLine()
        deleteLastLine()
    else:
        print()

if globals().get("isJS"):
    globals().get("loadinghide")()
    t.sleep(1)

hideCursor()

# yall are lame if you skip this on the first playthrough
story("Skip introduction?", True)
showCursor()
res = input()
hideCursor()

if ("no" in res) or (res == "false"):
    # yap time!
    story("It's the evening.")
    story("This time of the day was always your favorite.")
    t.sleep(0.15)
    print()
    t.sleep(0.15)
    story("Too much has been happening lately around your neighborhood.")
    story("Recently, some suspicious things have been going on. \nA couple of your neighbors have disappeared over the last month.")
    story("No one knew who caused it, but you're lucky it hasn't happened to you... yet.")
    story("To ease your mind off of this, you play the piano.")
    t.sleep(0.15)
    print()
    t.sleep(0.15)
    story("Inside your home, you had a grand piano.")
    story("Playing the piano was always a passion you've had.")
    story("You were a few of your kind in the neighborhood that listened to music.")
    t.sleep(0.15)
    print()
    t.sleep(0.15)
    story("After a bit, you hear knocks on your home. Not on the door, but around the walls.")
    story("Then... one of your walls collapse.")
    story("The sound was loud and sudden, and due to your faint nature, \nyou instinctively run into your bedroom and hide under the bed.")
    story("Lots of scurrying could be heard and objects were shuffled around.")
    story("After a bit, the footsteps grow quiet and you no longer hear much\nexcept the breeze coming in.")
    story("You emerge from underneath your bed and what awaited you was complete destruction.")
    story("All of your stuff... all broken down. Even your precious grand piano.") #trauma
    story("A tear catches your eye.")
    t.sleep(0.15)
    print()
    t.sleep(0.15)
    story("You cry yourself to sleep.")
    story("Tomorrow you start anew.")
    story("You hear giggling after you drift asleep")
    story("and then something hard strikes your head!")
    story("It's weak, but it's strong enough that you fall unconscious.")
    story("Before you do, you feel your body being dragged.")
    t.sleep(0.15)
    print()
    t.sleep(0.15)
    story("You wake up in an unfamiliar room.")

    for i in range(5):
        print()
        t.sleep(0.25)

# self portrait of my oc <3 (sorry i suck at drawing)
# actually PLAY MY ADVENTURE GAME to see my self insert
# it was converted this way using javascript cause it my favorite language and im fluent in it
# ignore how messy it is im too lazy to make a better codec
# sorry if it lags a bit i just wanted to make art for my game 😭
portrait_encoded = [
    0,[1,95],2,5,3,[6,26],9,8,[6,67],3,5,3,[6,23],7,8,[6,4],7,9,7,[6,63],3,5,3,
    [6,23],[7,2],[6,2],9,8,[6,17],[8,2],[9,5],8,7,[6,17],[8,2],[6,2],9,8,[6,17],3,5,3,[6,45],
    [10,2],9,[7,3],[8,2],[10,3],8,[6,14],8,9,7,8,9,[6,19],3,5,3,[6,45],[10,2],9,7,[6,6],8,[10,2],
    8,[6,15],[7,2],[6,19],3,5,3,[6,41],8,9,[10,5],9,[6,8],9,[10,2],8,[6,34],3,5,3,[6,28],[7,2],
    [6,4],7,[9,2],[10,5],9,8,7,6,7,8,7,[6,8],8,[10,5],9,7,[6,30],3,5,3,[6,12],7,[9,6],[10,16],9,
    [10,5],9,7,[6,12],[9,3],8,[6,3],8,[10,4],8,[6,8],[9,7],8,[6,11],3,5,3,[6,4],7,8,9,[10,6],9,
    [8,5],[7,2],[6,4],[7,3],[6,10],7,[8,3],[10,2],8,[6,9],7,[10,2],7,8,9,10,9,7,[6,2],[9,2],
    [10,9],[8,7],9,[10,7],9,8,[6,2],3,5,3,6,8,[10,4],9,7,[6,5],8,[9,10],8,7,[6,42],[7,4],
    [6,16],7,9,10,9,[6,3],3,5,3,7,9,[10,2],8,[6,7],7,9,[10,10],8,7,[6,45],7,9,[10,11],9,[6,2],7,
    9,[10,2],9,[6,3],3,5,3,[6,2],7,8,[10,3],9,7,[6,4],9,[10,9],7,[6,48],7,[10,7],9,7,[6,2],7,
    [10,4],8,[6,5],3,5,3,[6,6],7,9,[10,2],9,[8,2],7,[6,2],7,8,9,[10,4],9,[6,37],7,[8,2],[10,2],
    9,8,[6,4],7,9,[10,2],[8,2],7,8,9,[10,5],7,[6,8],3,5,3,[6,10],8,[10,6],[6,4],[7,2],[6,5],8,
    [10,5],7,[6,17],9,[10,13],9,[6,5],[7,2],8,[10,7],7,[6,12],3,5,3,[6,14],[8,2],9,[10,5],9,[6,5],
    7,9,[10,2],9,[10,9],9,[6,10],[10,7],8,[6,4],[10,3],8,[6,2],8,[10,3],8,7,[6,18],3,5,3,[6,20],8,
    [10,2],7,[6,4],8,[10,2],8,[6,2],[10,9],[6,10],[10,8],7,[6,4],[10,2],9,[6,2],7,[10,2],9,[6,20],
    3,5,3,[6,20],7,[10,2],7,[6,3],7,[10,2],9,[6,3],[10,9],[6,11],[10,6],8,[6,5],8,9,[6,3],9,10,9,
    [6,21],3,5,3,[6,20],8,[10,3],[6,4],8,[10,2],8,[6,3],7,[10,6],8,[6,15],[7,8],[6,3],8,[10,3],7,
    [6,21],3,5,3,[6,14],7,9,[10,4],9,7,[6,8],[7,8],[6,7],[10,4],8,[6,7],[7,4],[6,7],8,[10,12],9,7,
    [6,12],3,5,3,[6,12],8,[10,4],[7,2],[6,12],[7,6],[6,35],[7,2],9,[10,6],9,7,[6,12],3,5,3,[6,13],
    7,[10,10],[6,22],7,9,10,9,[6,17],8,[10,6],8,[6,20],3,5,3,[6,18],7,9,[10,2],9,7,8,9,[10,3],8,7,
    [6,9],[7,2],[6,2],7,9,[10,5],9,8,7,6,7,[6,11],7,8,9,[10,2],9,7,[6,2],7,9,10,9,10,9,8,7,[6,11],
    3,5,3,[6,17],9,[10,3],9,[10,4],[9,2],[10,3],8,[7,2],[6,10],8,10,9,8,[7,2],9,10,9,8,[6,4],
    [7,2],[8,4],7,[6,5],7,9,[10,2],7,6,[10,5],9,[10,4],[7,2],[6,7],3,5,3,[6,17],9,[10,3],[9,2],7,
    [6,5],8,9,[10,5],8,[7,6],[6,4],[7,5],[8,2],[10,20],7,[6,3],8,10,9,[6,3],7,9,[10,4],8,[6,4],3,
    5,3,[6,29],7,9,[10,2],[8,2],[9,2],[10,17],9,[8,3],7,[6,5],9,[10,2],9,[8,4],9,8,[6,4],7,9,10,8,
    6,7,8,7,[6,2],8,9,[10,3],8,7,3,5,3,[6,28],7,[10,2],8,[6,15],7,[10,4],9,[10,3],[6,9],9,[10,2],
    7,[6,10],8,[10,2],[8,3],[6,6],7,9,[10,2],3,5,3,[6,27],8,[10,2],9,[6,16],7,[10,3],9,[7,2],10,9,
    [6,10],[10,3],7,[6,10],9,[10,2],7,[6,4],8,[10,4],9,8,3,5,3,[6,26],7,[10,2],9,[6,19],7,8,9,8,
    [6,13],8,[10,2],8,[6,10],8,[10,2],8,[6,4],[8,2],9,8,7,[6,2],3,5,3,[6,26],[10,2],9,7,[6,36],7,
    [10,3],8,[6,9],7,[10,2],8,[6,2],9,[10,2],9,7,[6,4],3,5,3,[6,25],8,[10,2],8,[6,38],7,[10,2],8,
    [6,9],7,[10,2],8,[6,2],9,[10,2],9,7,[6,4],3,5,3,[6,25],[10,2],9,[6,39],7,[10,2],9,[6,9],7,
    [10,2],8,[6,4],7,[6,6],3,5,11,[1,95],4
]
logo_encoded = [
    [6,115],5,[6,7],[9,3],[6,105],5,6,[10,11],[6,24],[10,2],6,[10,2],[6,74],5,6,[10,3],[6,7],
    [10,3],[6,13],[10,2],[6,3],[10,7],[6,59],9,[10,11],[6,5],5,[6,3],[10,3],[6,5],9,[10,2],
    [6,13],[10,2],[6,3],[10,5],8,[10,3],[6,9],[10,2],[6,45],[10,2],[6,9],[10,2],[6,5],5,[6,4],
    [10,3],[6,5],[10,2],[6,13],[10,2],[6,21],[10,2],[6,43],[10,2],[6,9],[10,2],8,[6,6],5,[6,6],
    [10,5],9,6,[10,2],[6,11],9,[10,2],[6,5],[10,2],[6,12],[10,3],[6,44],[10,2],[6,7],[10,2],[6,9],
    5,[6,14],[10,2],[6,4],[10,2],[6,4],[10,2],7,[6,4],[10,3],[6,4],[10,7],[6,2],[10,5],[6,2],
    [10,6],[6,2],[10,2],[6,2],[10,4],[6,7],[10,3],[6,13],[10,5],6,9,[10,2],[6,3],[10,4],8,[6,3],5,
    [6,14],[10,2],[6,3],[10,3],[6,3],[10,3],[6,4],[10,2],[6,5],[10,3],[6,3],[10,2],[6,2],7,10,
    [6,3],[10,7],[6,3],[10,5],[6,2],[10,2],[6,4],[10,2],[6,6],9,[10,3],7,[10,2],6,[10,4],[6,7],
    [10,3],6,9,[10,2],[6,4],5,[6,15],[10,3],9,[10,7],[6,4],[10,3],[6,4],9,[10,3],[6,3],[10,2],8,
    [6,2],[10,7],[6,8],[10,3],[6,9],[10,2],[6,6],[10,2],[6,4],[10,3],[6,2],[10,2],[6,2],10,8,[6,2],
    7,[10,2],[6,9],5,[6,18],7,[6,37],[10,6],[6,2],8,10,[6,11],[10,6],6,[10,7],6,[10,3],[6,2],[10,3],
    [6,3],7,[10,2],[6,9],5,[6,11],[10,10],[6,8],[10,4],[6,10],[10,4],[6,26],[10,6],[6,4],[10,2],
    [6,16],[10,3],8,[6,10],5,[6,21],[10,8],9,[6,2],[10,11],7,[6,3],[10,27],[6,4],7,[10,4],9,6,
    [10,16],8,[6,13],5,[6,115],5,[6,115]
]
silly_map = {
    0: "╔",
    1: "═",
    2: "╗",
    3: "║",
    4: "╝",
    5: "\n",
    6: " ",
    7: "░",
    8: "▒",
    9: "▓",
    10: "█",
    11: "╚", # i forgot so its at the end now
}
portrait = ""
logo = ""
# dont make fun of me im still learning compression algorithms
for v in portrait_encoded:
    if type(v) == int:
        portrait += silly_map[v]
    else:
        portrait += silly_map[v[0]] * v[1]
for v in logo_encoded:
    if type(v) == int:
        logo += silly_map[v]
    else:
        logo += silly_map[v[0]] * v[1]

navigate = True
while True:
    if navigate:
        navigate = False
        print()
        map()
        description()
    handleOptions()
    if location == "win":
        break

for i in range(5):
    print()
    t.sleep(0.25)

draw_logo()

credits = [
    "     Thank you for playing!",
    " " * 50,
    "     Wintercat - a short puzzle game",
    "     Made for Folktale Hack Club 2026",
    " " * 50,
    "     There are lots of bugs and mistakes, especially with the text in some cases, but the game is most likely in a playable state.",
    " " * 50,
    "     And thank you to everyone who helped:",
    "     Me - basically everything",
    "     Tehseen 'Ashbourne' Noyan - emotional support and testing sometimes occasionally", 
    "     Honorable mentions",
    "     Gus, Shabir, Roman, Kenai, Vyron, Said, Joseph, Zamu 'Prod' Four, 'Gloomy'",
    "     And my teachers - Mr. Aguilar, Mr. Dushane, Mr. Martin, Mr. Sequeira, Ms. Sagara, Mr. Warmerdam, Ms. Berry",
    " " * 50,
    "     Yes I put myself into the game",
    "     Yes the main characters are cats",
    "     The gang is a group of cats btw if you couldn't tell",
    "     I like kitties",
    "     Oh yeah and the main character bought another grand piano",
    "     And the gang got arrested",
    "     The end",
    "     Ok thank you",
    "     Goodbye"
]

for v in credits:
    story(v, True)
    t.sleep(0.75)
for i in range(5):
    print()
    t.sleep(0.25)

if globals().get("isJS"):
    globals().get("ending")()
