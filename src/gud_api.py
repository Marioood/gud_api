import time
import random
import subprocess
import math
import sys

import pydn

GUD_API_USER = "DEPRECATED" #your steam name. used to prevent randos from restarting the python script
GUD_API_TICK_DELAY = 400 #sync this with the blah blah alias thingie
GUD_API_CFG_PATH = "gud_api.cfg" #where the cfg is
GUD_API_DATA_PATH = "database.pydn" #where the data is
GUD_API_LOG_PATH = "C:/Program Files (x86)/Steam/steamapps/common/JBMod/jbmod/console.log" #where the log file is. MAKE SURE to put '-condebug' in your launch parameters to make console.log work.
GUD_API_RECENT_LINES_MAX = 16 #how many recent console.log entries are saved when scanning for commands
GUD_API_CONSOLE_USER = "[CONSOLE]"
# dont change these unless you want to get HAXXED
GUD_API_STUPID_RCE = False
GUD_API_STUPID_IGNORE_ADMIN = False

GUD_API_STARTING_PLAYER_DATA = 1000

#TODO: $tipz
#TODO: program crashes if a colon is in the message
#TODO: command queue
#TODO: prevent babble jams when the script is halted unexpectedly
#TODO: reformatting for yap()
#TODO: mac os $monkey command (random commands w/ random inputs)
#TODO: $rep NotBart

cfg = []
cfg_write_count = 0
  
def format_count(count, singular, plural = None):
  if plural == None: plural = singular + "s"
  
  if count == 1:
    return "{} {}".format(count, singular)
  else:
    return "{} {}".format(count, plural)
    
def rand_bool(chance = 2):
  return random.randint(0, chance) == 0

def cmd(text):
  if GUD_API_STUPID_RCE:
    cfg.append(text)
  else:
    #text = text.replace(";", ":")
    #cfg.append(text)
  
    if ';' in text:
      cfg.append("say potential RCE attempt. semicolon found in command")
      print("say potential RCE attempt. semicolon found in command")
    #elif "\\" in text:
    #  cfg.append("say potential RCE attempt. back slash found in command")
    #  print("say potential RCE attempt. back slash found in command")
    else:
      cfg.append(text)
      
      
def cmd_unsafe(text):
  cfg.append(text)
  
chang_mode = False
use_command_line = False
  
def yap(text):
  """text_bak = text
  text = ""
  for char in text_bak:
    text += chr(ord(char) + 1)"""
    
  if chang_mode:
    cmd("say chang " + text)
  else:
    cmd('say "{}"'.format(text))
  
def print_cfg():
  for cmd in cfg:
    print(cmd)
 
def export_cfg(type):
  global cfg
  global cfg_write_count
  global use_command_line
  
  cfg_write_count += 1
    
  if use_command_line:
    for txt in cfg:
      if txt[:3] == "say":
        print((GUD_API_CONSOLE_USER + " :  " + txt[4:].replace('"', ""))[:256])
        
      else:
        print(txt)
      
  else:
    f = open(GUD_API_CFG_PATH, "w", encoding="utf-8")
    print("cfg contents:")
    
    try:
      if type == "inline":
        # write cfg
        for txt in cfg:
          f.write(txt)
          f.write(';')
      elif type == "cfg":
        # write cfg
        for txt in cfg:
          f.write(txt)
          f.write('\n')
          
    except Exception as e:
      open(GUD_API_CFG_PATH, "w", encoding="utf-8").close()
      cfg = []
      f.write("say failure in export_cfg(): {}".format(e)) # crash messages
      print("export_cfg() failed!")
      
    # print info
    for txt in cfg:
      print("  " + txt)
      
    print()
    print("successfully wrote to " + GUD_API_CFG_PATH)
    f.close()
    
#status -- what?
"""def parse_api_data(state):
  f = open(GUD_API_DATA_PATH, "r", encoding="utf-8")
  lines = f.readlines()
  parsed = []
  player_data = {}
  print(lines)
  
  is_reading_string = False
  cur_string = ""
  is_escaped = False
  
  for line in lines:
    parsed_line = []
    
    for char in line:
      if is_reading_string:
        if char == '"' and not is_escaped:
          is_reading_string = False
          parsed_line.append(cur_string)
          cur_string = ""
        elif char == '\\' and not is_escaped:
          is_escaped = True
        else:
          cur_string += char
          is_escaped = False
      else:
        if char == '"':
          is_reading_string = True
        elif char == '#':
          print("skipping " + line)
          break
          
    if len(parsed_line) == 2:
      parsed.append(parsed_line)
      token_count = -1
      
      if parsed_line[1] == "max":
        token_count = sys.maxsize
      elif parsed_line[1] == "inf":
        token_count = math.inf
      elif parsed_line[1] == "-max":
        token_count = -sys.maxsize
      elif parsed_line[1] == "-inf":
        token_count = -math.inf
      else:
        token_count = int(parsed_line[1])
        
      player_data[parsed_line[0]] = Player("n/a", parsed_line[0], token_count)
      
    elif len(parsed_line) == 1:
      print("missing player data...")
    elif len(parsed_line) > 2:
      print("too much player data...")
      
  f.close()
    
  print(parsed)
  print(player_data)
  
  state.player_newdat = player_data"""
  
"""def update_api_data_file(player_data):
  f = open(GUD_API_DATA_PATH, "w", encoding="utf-8")
  print("player data contents:")
  
  try:
    f.write("#this file regenerates automatically\n")
    f.write("#comments left in this file will not be saved\n\n")
    
    for pair in player_data.items():
      player = pair[0]
      data = pair[1]
      player = player.replace('\\', '\\\\')
      player = player.replace('"', '\\"')
      
      f.write('"{}" "{}"'.format(player, data))
      f.write('\n')
      
    f.close()
  except Exception as e:
    open(GUD_API_DATA_PATH, "w", encoding="utf-8").close()
    cfg = []
    f.write("say failure in update_api_data_file(): {}".format(e)) # crash messages
    print("update_api_data_file() failed!")
    
  # print info
  for pair in player_data.items():
    print('  "{}" "{}"'.format(pair[0], pair[1]))
    
  print()
  print("successfully wrote to " + GUD_API_DATA_PATH)"""
  
  
def update_database(global_state):
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  #CLOSE FILES
  
  f = open(GUD_API_DATA_PATH, "w", encoding="utf-8")
  
  try:
    #turn objects into lists
    database = {}
    player_data_reformatted = {}
    
    for player_name in global_state.player_newdat:
      player_obj = global_state.player_newdat[player_name]
      player_list = [player_obj.name, player_obj.tokens, player_obj.kills, player_obj.deaths]
      player_data_reformatted[player_name] = player_list
    
    database["player_data"] = player_data_reformatted
    
    player_data_encoded = pydn.encode(database, pydn.FLAG_COMPACT_LISTS, "This file regenerates automatically; comments left in it will not be saved.", "Player data is stored as: SteamID: [name, tokens, kills, deaths].")
    f.write(player_data_encoded)
    f.close()
    
  except Exception as e:
    #TODO: rather unusual, and also incompatable with command line mode
    open(GUD_API_DATA_PATH, "w", encoding="utf-8").close()
    cfg = []
    f.write("say failure in update_database(): {}".format(e)) # crash messages
    print("update_database() failed!")
    
  print()
  print("[INFO] Successfully wrote to " + GUD_API_DATA_PATH)

class HangmanManager:
  def __init__(self):
    self.playing = False
    self.answer = ""
    self.guesses_right = []
    self.guesses_wrong = []
    self.max_wrong = 6
    self.current_players = []
    
class GodManager:
  def __init__(self):
    #jumping is not a crime
    self.words = ["beautiful","dirty","dirt","stone","rough","water","smooth","harsh","jade","gold","golden","plating","plate","plated","notched","carved","carving","chiseled","tile","button","jagged","porus","spongy","sponge","carpet","wall","floor","dull","shiny","special","clay","mud","sand","magma","lava","leaves","wood","bark","cloth","concrete","curtain","striped","flag","sign","pillar","column","linoleum","quartz","planks","screen","metal","iron","fur","plastic","tinny","tin","steel","marble","marbled","meat","meaty","slippery","red","orange","yellow","lime","green","blue","indigo","purple","magenta","black","pink","white","light","dark","grey","brown","rouge","lemon","sour","foul","awful","amazing","book","paper","leather","glass","glassy","wet","hot","cold","warm","lukewarm","rock","boulder","moss","mossy","abstract","geometric","artistic","algebraic","archaic","simple","crude","basic","cell","battery","tissue","outlet","screw","nail","iridescent","refractive","pearlescent","pearl","cracked","shattered","torn","worn","broken","java","script","cascading","style","sheet","hypertext","markup","language","powder","powdered","calculus","wave","tangent","square","root","gradient","papyrus","cactus","thorny","terrain","rocky","mountain","enormous","miniscule","firey","string","array","set","map","hash","hashed","text","textual","texture","generic","bland","obtuse","obsidian","geode","ruby","platform","sludge","random","procedural","predictable","c","ansi","plus","flower","bone","boned","ball","grass","weed","roof","shingles","cancer","glowing","glowy","glow","bitwise","fractal","recursive","insane","crazy","self","similar","structure","logical","assembly","low","level","with","flat","sprite","buffer","file","stream","memory","pixel","bottle","ur","heaven","bubble","bubbles","sequence","glitter","glittery","sparkles","sparkly","fancy","holy","temple","frutiger","aero","bar","bars","barred","wavy","null","void","pointer","flooring","machine","machinary","graph","mushroom","stalk","trunk","oak","pine","ghost","gum","table","brain","positive","negative","electron","electric","spark","glaze","wine","bread","skin","blood","lambda","foo","baz","jet","theta","pi","ceiling","tube","lamp","lantern","pattern","design","serpent","apple","software","abraham","angel","theology","cloud","edges","edge","blobs","border","noise","bort","phonks","bart","jb","jbmod","man","guy","relt","wawa","chang","charoid","reltoid","take","my","meds","fat","boy","big","money","william","banks","is","a","good","person","maluch","xenia","modification","api","cayama","slop","sloppy","sloppiest","girl","cock","slim","how","to","start","god","bless","usa","floppa","floppoid","pornist","penile","B==============D~~~~~~~~~~-----","little","steam","steamy","freak","freaky","bling","ping","pong","computer","processor","computation","global","local","logarithmic","exponential","in","or","out","commodore","64","amiga","atari","dictionary","complete","scrap","scrapped","scraps","scrapper","incomplete","abandoned","unfinished","finished","some","command","description","pounds","butter","honolulu","estrogen","glory","administrator","help","one","for","me","shit","nooo","no","yes","spave","malloc","hoy","edict","spungler","spoomler","sdoon","grout","ghoul","vivement","joyous","joyfil","joyful","joy","rtv","mind","mindwave","epstein","trump","glory to the administrator","one for me and one for me","sometimes i dream about cheese","dream","cheese","sometimes","about","clone","maw","maws","feet","foot","scratch","cat","hell","babble","babbler","pumpkin","works","dox","doxxed","angler","fish","fishie","ovh","ass","party","lmao","blacked","mr","those who know","those","who","know","inspect","radio","meet","meet me at the radio","port","dangdong","stressed","box","agartha","ufo","doubleplusungood","unwholesome","nineteen","eighty","four","strike","dolbab","doldad","dolbabian","spitish","suckfishes","purgatorian","relentlessnesses","vibe","code","dribble","crash","crasher","content","house","dead","mechanic","less","space","construct","construction","round","bunker","test","prop","props","hand","hands","soda","can","canned","pop","cola","coke","degenerate","faces","face","rebel","chat","generate","generative","boring","bored","bore","hole","hold","holes","chamber","chambered","chambers","charred","char","diddy","blud","ts","pmo","charisma","charismatic","chloroplast","eukaryote","prokaryote","cells","celled","trollimog","wafers","sneed","feed","seed","formerly","chuck","chick","sick","suck","haus","hl2world","world","hl2","animation","cycler","bb","think","unperson"]
    self.map_prefixes = ["jb","jb","jb","jb","jb","gm","gm","gm","de","jbdm","jbdm","jbdm","ttt","jbsm","phy","test","sdk"]
    
class GlobalState:
  def __init__(self):
    self.commands = {
      #public commands
      "$help": CommandHelp(),
      "$???": CommandQuestioneyQuestioneyQuestioney(),
      "$god": CommandGod(),
      "$relt": CommandRelt(),
      "$floppa": CommandFloppa(),
      "$stats": CommandStats(),
      "$hangman": CommandHangman(),
      "$guess": CommandBabble("$guess", "Stupid Dumb Fucking Idiot.", "babble"),
      "$casino": CommandCasino(),
      "$roll": CommandRoll(),
      "$iota": CommandIota(),
      "$cip": CommandBabble("$cip", "The Mouse Program Has Been Installed.", "install cip software onto the server."),
      "$chang": CommandChang(),
      "$kill": CommandKill(),
      "$input": CommandInput(),
      "$test": CommandTest(),
      #private commands
      "$macro": CommandMacro(),
      "$exec": CommandExec(),
      "$autobabble": CommandQuery(),
      "$vaporize": CommandVaporize(),
      "$clear": CommandClear(),
      "$crash": CommandCrash()
    }
    self.hangman = HangmanManager()
    self.god = GodManager()
    self.player_data = {}  #"steam id"    : tokens
    self.player_newdat = {} #"steam id" : player object
    self.player_ids = {}   #"player name" : "steam id"
    self.macros = {}       #"macro name   : macro object
    self.autobabbles = {}  #"query        : "response"
    self.reltbabble = []
    #60
    raw = open("reltbabble_p50.txt", "r", encoding="utf-8")
    lines = raw.readlines()
    reltino_name = "whatsavalue"
    for line in lines:
      if not line[:len(reltino_name)] == reltino_name:
        self.reltbabble.append(line)
        
    raw.close()
    
    self.config = {}
    
    #stripped = open("reltbabble_p40_stripped.txt", "w", encoding="utf-8")
    #
    #for line in self.reltbabble:
    #  stripped.write(line)
    #  
    #stripped.close()
    #print(self.reltbabble)
    
    #sys.exit(1)
    
    
################

class Command:
  #THIS CLASS IS AND SHOULD NEVER BE USED AS A COMMAND!!!
  def __init__(self):
    self.name = "$the_name_of_the_command"
    self.description = "some basic description of the command"
    self.is_restricted = False #whether the command is only usable by the user defined in GUD_API_USER. is ignored when GUD_API_STUPID_IGNORE_ADMIN is True
  
  def execute(self, author, args, state):
    yap("what the command does in-game") #use the yap(text) function to make the api talk
    cmd("kill") #use the cmd(text) function to execute commands
    
    #args is a list of arguments for the command
    #author is whoever used the command
    #imagine a message like "char :  $help $iota"
    #the message gets split up as author = "char", command_name = "$help", args = ["$iota"]
    
    #state is an object that contains several variables for keeping track of stuff between command usage. the $hangman and $input commands use it heavily.
    #state is structured like so:
    
    #state
    #|
    #|---hangman
    #|   |
    #|   |---hangman variables~~
    #|
    #|---god
    #|   |
    #|   |---god variables~~
    #|
    #|---player_data
    #|   |
    #|   |---dict of player name keys and token values
    #|
    #|---macros
    #    |
    #    |---dict of macro definition objects
    
    #TODO: explain custom state
    
class Macro:
  def __init__(self, name, permission, macro_args, command_combined):
    self.name = name #the_name_of_the_macro"
    self.command_unformatted = command_combined#"unformatted (without the arguments) version of the macro"
    self.args_def = macro_args #definition of the macro arguments
    self.creator = "whoever created this macro"
    self.is_restricted = not GUD_API_STUPID_RCE
    #help command for macros
  #def execute(self, args):
    
    #TODO: author, maybe?
    
class Player:
  def __init__(self, id, name, tokens = GUD_API_STARTING_PLAYER_DATA, kills = 0, deaths = 0):
    self.id = id
    self.name = name
    self.tokens = tokens
    self.kills = kills
    self.deaths = deaths
    
################

class CommandHelp(Command):
  def __init__(self):
    self.name = "$help"
    self.description = "'$help' prints a list of commands. '$help <command>' prints a description of the command. '$help private' prints restricted commands."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    #TODO: have commands dict be stored in the global state
    if len(args) == 0:
      commands_text = ""
      i = 0
      
      for command_name in state.commands:
        command = state.commands[command_name]
        if not command.is_restricted:
          #proper grammer
          if i > 0:
            commands_text += ", "
            
          commands_text += command_name
        
          i += 1
      
      yap("Commands: " + commands_text + ".")
      
    elif args[0] == "private":
      commands_text = ""
      i = 0
      
      for command_name in state.commands:
        command = state.commands[command_name]
        if command.is_restricted:
          #proper grammer
          if i > 0:
            commands_text += ", "
            
          commands_text += command_name
        
          i += 1
      
      yap("private commands: " + commands_text)
    
    else:
      command_name = args[0].lower()
      
      if command_name in state.commands:
        command_help = state.commands[command_name]
        command_restricted = "yes" if command_help.is_restricted else "no"
        yap("{} restricted? {}.".format(command_help.description, command_restricted))
        
      elif '$' + command_name in state.commands:
        command_help = state.commands['$' + command_name]
        command_restricted = "yes" if command_help.is_restricted else "no"
        yap("{} restricted? {}.".format(command_help.description, command_restricted))
        
      else:
        yap("unknown command '{}'".format(command_name))

################

class CommandIota(Command):
  def __init__(self):
    self.name = "$iota"
    self.description = "'$iota <amount (default: 1)>' increments a counter."
    self.is_restricted = False
    
    self.iota_counter = 0
  
  def execute(self, author, args, state):
    increment = 1
    
    if len(args) > 0:
      increment = int(args[0])
      
    self.iota_counter += increment
    
    if self.iota_counter == 1:
      yap("This command has been run {} time.".format(self.iota_counter))
    else:
      yap("This command has been run {} times.".format(self.iota_counter))
    
################

class CommandTest(Command):
  def __init__(self):
    self.name = "$test"
    self.description = "HELP!"
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if len(args) == 0:
      yap("HELP!")
    else:
      yap("args: {}".format(args))
        
################

class CommandQuestioneyQuestioneyQuestioney(Command):
  def __init__(self):
    self.name = "$???"
    self.description = "Prints statistics and info about the current gud_api session."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if len(args) == 0:
      yap("console.log entries: {}. console.log reads: {}. gud_api.cfg writes: {}. current user: {}".format(len(lines), log_read_count, cfg_write_count, GUD_API_USER))
    else:
      stat = args[0]
      if stat == "player_data":
        yap("nah")#str(state.player_data))
        
      if stat == "player_newdat":
        yap(str(state.player_newdat))
        
      elif stat == "autobabbles":
      
        yap(str(state.autobabbles))
        
      elif stat == "start_message":
        yap(state.config["system"]["start_message"])
    
################

class CommandChang(Command):
  def __init__(self):
    self.name = "$chang"
    self.description = "toggles whether or not each message printed by gud_api should be prefixed with 'chang'."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    global chang_mode
    
    if chang_mode:
      chang_mode = not chang_mode
      yap("all messages will no longer be prefixed with 'chang'")
    else:
      chang_mode = not chang_mode
      yap("all messages will now be prefixed with 'chang'")

################

class CommandGod(Command):
  def __init__(self):
    self.name = "$god"
    self.description = "'$god <count (default: random)>' prints a list of random words. '$god <message>' answers a question."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    god_text = ""
    prefix = ""
    word_count = random.randrange(17)
    jbmode = False
    
    if len(args) > 0:
      try:
        word_count = int(args[0])
        
        if word_count > 100:
          yap("That is way too many words.")
          return
        
      except ValueError:
        if args[0] == "map":
          jbmode = True
          word_count = random.randrange(9)
        else:
          for arg in args[:-1]:
            prefix += arg
            prefix += " "
        
          prefix += args[-1] + "? "
    
    for i in range(word_count):
      #TODO: make this less voodoolicious
      god_word = random.choice(state.god.words)
      if jbmode: god_word = god_word.replace(' ', '_')
      #nineteen eight-four
      if rand_bool(50):
        god_word = "un" + god_word
      elif rand_bool(50):
        god_word = "mal" + god_word
      elif rand_bool(50):
        god_word = "good" + god_word
        
      if rand_bool(50):
        god_word = "plus" + god_word
      elif rand_bool(50):
        god_word = "doubleplus" + god_word
        
      if rand_bool(50):
        god_word = "old" + god_word
      elif rand_bool(50):
        god_word = "new" + god_word
        
      if rand_bool(50):
        god_word = "up" + god_word
        
      if rand_bool(50):
        god_word = "ante" + god_word
      elif rand_bool(50):
        god_word = "post" + god_word
      
      if rand_bool(10): god_word += "oid"
      
      god_text += god_word
      
      if i != word_count - 1:
        if jbmode:
          god_text += '_'
        else:
          if rand_bool(15):
            god_text += '-'
          elif rand_bool(15):
            god_text += '_'
          elif rand_bool(25):
            god_text += ' ' + random.choice(state.god.map_prefixes) + '_'
          else:
            god_text += ' '
        
    if jbmode:
      god_text = random.choice(state.god.map_prefixes) + '_' + god_text
      if rand_bool():
        god_text += '_v' + str(random.randint(0, 20))
      
    yap(prefix + "God says: " + god_text)

################

class CommandKill(Command):
  def __init__(self):
    self.name = "$kill"
    self.description = "'$kill' kills the user of the command. '$kill <target>' kills the target. will not work without sv_cheats."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    target = author
    if len(args) > 0:
      target = args[0]
    #TODO: check if they've actually been killed
    yap('" {} has been killed telepathically."'.format(target))
    cmd("kill {}".format(target))
      
################

class CommandBabble(Command):
  def __init__(self, name, message, description = "babble"):
    self.name = name
    self.description = description
    self.is_restricted = False
    
    self.message = message
    
  def execute(self, author, args, state):
    yap(self.message)
      
################

class CommandHangman(Command):
  def __init__(self):
    self.name = "$hangman"
    self.description = "'$hangman <max incorrect guesses (default: 5)>' start a game of hangman."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    state.hangman.guesses_right = [' ', '-', '_', "'", '"']
    state.hangman.guesses_wrong = []
    state.hangman.answer = random.choice(state.god.words)
    
    if len(args) > 0:
      state.hangman.max_wrong = int(args[0])
    
    
    hint_text = ""
    
    for char in state.hangman.answer:
      if char == ' ':
        hint_text += '  '
      else:
        hint_text += ' _'
        
    yap("word:{}. what is your guess? say '$input <guess>' to guess. game will be lost after {} incorrect guesses".format(hint_text, state.hangman.max_wrong))
    state.hangman.playing = True

################

class CommandCasino(Command):
  def __init__(self):
    self.name = "$casino"
    self.description = "test."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    bet = 10
    if random.randint(0, 100) == 0:
      yap("How To Enter Relt's Casino.")
      return
      
    if author in state.player_newdat:
      player = state.player_newdat[author]
      
      if len(args) > 0:
        arg_bet = args[0]
        if arg_bet == "all":
          bet = player.tokens
        else:
          try:
            bet = int(args[0])
          except ValueError:
            yap("Bet can only be a whole number or 'all.'")
            return
            
      if player.tokens - bet < 0:
        yap("{} only has {} tokens...".format(author, player.tokens))
        return
      elif bet < 0:
        yap("{}, you cannot bet negative tokens!".format(author))
        return
    
      SLOT_BAR = 1
      SLOT_CHERRY = 2
      SLOT_7 = 3
      SLOT_HEART = 4
      SLOT_BIG_MONEY = 5
      SLOT_GOD = 6
      SLOT_RELT = 7
      SLOT_HORSESHOE = 8
      SLOT_CROWN = 9
      SLOT_DIAMOND = 10
      SLOT_SPADE = 11
      SLOT_LEMON = 12
      
      slots = [
        ("BAR", SLOT_BAR),
        ("()'", SLOT_CHERRY),
        (" 7 ", SLOT_7),
        #("(v)", SLOT_HEART),
        ("$$$", SLOT_BIG_MONEY),
        #("GOD", SLOT_GOD),
        #("CNG", SLOT_CHANG),
        #("MLH", SLOT_MALUCH),
        ("RLT", SLOT_RELT),
        #("ZEN", SLOT_ZENNY),
        (" U ", SLOT_HORSESHOE),
        #("nMn", SLOT_CROWN),
        #("<> ", SLOT_DIAMOND)
        #("(|)", SLOT_SPADE),
        #("<>'", SLOT_LEMON)
      ]
      choices = [-1,-1,-1]
      
      choices[0] = random.choice(slots)
      choices[1] = random.choice(slots)
      choices[2] = random.choice(slots)
      
      display_text = "|{}|{}|{}|".format(choices[0][0],choices[1][0],choices[2][0])
      earned_tokens = 0
      info = ""
      
      if choices[0][1] == SLOT_BAR and choices[1][1] == SLOT_BAR and choices[2][1] == SLOT_BAR:
        earned_tokens = 10
      #elif choice_sum == SLOT_7 + SLOT_7 * slot_mult + SLOT_7 * slot_mult * 2:
      elif choices[0][1] == SLOT_7 and choices[1][1] == SLOT_7 and choices[2][1] == SLOT_7:
        earned_tokens = 777
      elif choices[0][1] == SLOT_BIG_MONEY and choices[1][1] == SLOT_BIG_MONEY and choices[2][1] == SLOT_BIG_MONEY:
        earned_tokens = 25
      elif choices[0][1] == SLOT_RELT and choices[1][1] == SLOT_RELT and choices[2][1] == SLOT_RELT:
        #square the bet
        earned_tokens = bet
      elif choices[0][1] == choices[1][1] == choices[2][1]:
        #any 3 slots that are the same
        earned_tokens = 2
      else:
        for slot in choices:
          if slot[1] == SLOT_BAR:
            earned_tokens += 2
        
        
      if earned_tokens == 0:
        info = "You lost..."
      elif earned_tokens == 1000:
        info = "You have won BIG MONEY!!!"
      else:
        info = "You won!!!"
        
      earning = bet * earned_tokens - bet
      
      yap("{} bet {} tokens. Results: {}. {} earned {} tokens".format(author, bet, display_text, info, earning))
      player.tokens += earning
    else:
      state.player_newdat[author] = Player("n\a", author)
      yap("{} was previously unregistered. They have been given {} tokens.".format(author, GUD_API_STARTING_PLAYER_DATA))
      
    #update_api_data_file(state.player_data)

################

class CommandInput(Command):
  def __init__(self):
    self.name = "$input"
    self.description = "provides a way to interact with game commands ($hangman). this command may or may not be changed."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if state.hangman.playing:
      if len(args) == 0:
        yap("Guess cannot be empty.")
        
      else:
        state.hangman.current_players.append(author)
      
        guess = args[0].lower()
        is_correct = False
        text = ""
        
        if guess in state.hangman.guesses_right or guess in state.hangman.guesses_wrong:
          text = "That's already been guessed..."
          
        elif len(guess) == len(state.hangman.answer):
          if guess == state.hangman.answer:
            yap("You won!!! The answer was '{}'. Incorrect guesses: {}".format(state.hangman.answer, len(state.hangman.guesses_wrong)))
            state.hangman.playing = False
          else:
            text = "Guess is incorrect..."
            state.hangman.guesses_wrong.append(guess)
          
        elif len(guess) > 1:
          yap("Guess can only be a single letter or the whole word!")
        
        else:
          for char in state.hangman.answer:
            if guess == char:
              state.hangman.guesses_right.append(guess)
              is_correct = True
          
          if is_correct:
            if len(state.hangman.guesses_right) == len(state.hangman.answer):
              for player in state.hangman.current_players:
                if player in state.player_data:
                  state.player_data[player] += 50
                
                else:
                  state.player_data = GUD_API_STARTING_PLAYER_DATA + 50
              
              state.hangman.current_players = []
              update_api_data_file(state.player_data)
              
              yap("You won!!! The answer was '{}'. guesses: {}. 50 tokens have been given to each hangman player.".format(state.hangman.answer, len(state.hangman.guesses_right) + len(state.hangman.guesses_wrong)))
              state.hangman.playing = False
            else:
              text = "guess is correct!"
            
          else:
            if len(state.hangman.guesses_wrong) == state.hangman.max_wrong - 1:
              for player in state.hangman.current_players:
                if player in state.player_data:
                  state.player_data[player] -= 50
                
                else:
                  state.player_data = GUD_API_STARTING_PLAYER_DATA - 50
              
              state.hangman.current_players = []
              update_api_data_file(state.player_data)
              
              yap("You lost... the answer was '{}'. 50 tokens have been deducted from each hangman player.".format(state.hangman.answer))
              state.hangman.playing = False
            else:
              text = "guess is incorrect..."
              state.hangman.guesses_wrong.append(guess)
              
        if state.hangman.playing:
          hint_text = " word: "
          
          for char in state.hangman.answer:
            if char in state.hangman.guesses_right:
              hint_text += char
            else:
              hint_text += '_'
              
            hint_text += ' '
            
          hint_text += "wrong: "
          
          for char in state.hangman.guesses_wrong:
            hint_text += char
            hint_text += ' '
            
          yap(text + hint_text)
        
    else:
      yap("This command can only be used when $hangman is active.")
  
################

class CommandRoll(Command):
  def __init__(self):
    self.name = "$roll"
    self.description = "'$roll <sides (default: 2))>' rolls a die."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    sides = 2
    if len(args) == 1:
      sides = int(args[0])
    
    roll = random.randrange(sides) + 1
    
    yap("rolled a {}".format(roll))

################

class CommandClear(Command):
  def __init__(self):
    self.name = "$clear"
    self.description = "Clears console.log."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    f = open(GUD_API_LOG_PATH, "w", encoding="utf-8")
    for i in range(GUD_API_RECENT_LINES_MAX):
      f.write("padding {}\n".format(i))
    
    f.close()
    yap("console.log has been successfully cleared")
    
################

class CommandCrash(Command):
  def __init__(self):
    self.name = "$crash"
    self.description = "Causes an intentional crash."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    print("a" + 1)

################

class CommandStats(Command):
  def __init__(self):
    self.name = "$stats"
    self.description = "'$stats <person (default: author)>' prints the person's gud_api stats."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    person = author
    external_check = False
    
    if len(args) > 0:
      person = " ".join(args)
      external_check = True
      
    if person in state.player_newdat:
      #TODO: save previously recorded stats
      player = state.player_newdat[person]
      tokens_txt = format_count(player.tokens, "token")
      kills_txt = format_count(player.kills, "kill")
      deaths_txt = format_count(player.deaths, "death")
      
      yap("{}: {}, {} and {}. ID: {}".format(person, tokens_txt, kills_txt, deaths_txt, player.id))
    else:
      if external_check:
        yap("{} is not registered.".format(person))
        
      else:
        state.player_newdat[person] = Player("n/a", person)
        yap("{} is now registered. They have been given {} tokens.".format(person, GUD_API_STARTING_PLAYER_DATA))
        update_database(state)
    
################

class CommandMacro(Command):
  def __init__(self):
    self.name = "$macro"
    self.description = "'$macro <permission> <name> <args> -> <command>' defines a custom command. Commands are run with $exec."#. Usage is found in code comments in the CommandMacro object."#"'$macro <permission (private or public)> <name> <args (separated by spaces, ended by '->')> <command (args are used like {arg} in the command)>' Defines a custom command. "
    #$macro public color_zombie color -> ent_create npc_zombie rendercolor {color}
    #$macro permission name arg1 arg2 argn -> command
    self.is_restricted = True
  
  def execute(self, author, args, state):
    if len(args) > 4:
      permission = args[0]
      name = args[1]
      macro_args = []
      i = 2
      while len(args) > i:
        arg = args[i]
        if arg == "->":
          break
        else:
          macro_args.append(arg)
        i += 1
      command_segmented = args[i + 1:]
      command_combined = command_segmented[0]
      
      for command in command_segmented[1:]:
        command_combined += ' '
        command_combined += command
      
      cmd_unsafe("say p {} n {} a {} c {}".format(permission, name, macro_args, command_combined))
      state.macros[name] = Macro(name, permission == "private", macro_args, command_combined)
      
################

class CommandExec(Command):
  def __init__(self):
    self.name = "$exec"
    self.description = "'$exec <macro name> <macro arguments>' executes a macro."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if len(args) == 0:
      yap("No macro provided.")
    
    else:
      macro_name = args[0]
      
      if not macro_name in state.macros:
        yap("Unknown macro '{}'".format(macro_name))
        return
        
      macro = state.macros[macro_name]
      
      macro_args = args[1:]
      
      if len(macro_args) < len(macro.args_def):
        yap("Not enough arguments. Expected: {}".format(state.macros[macro_name].args_def))
        return
        
      if macro_name in state.macros:
        command_formatted = macro.command_unformatted
        
        for i in range(len(macro_args)):
          macro_arg = macro_args[i]
          macro_arg_name = macro.args_def[i]
          
          command_formatted = command_formatted.replace('{' + macro_arg_name + '}', macro_arg)
        
        cmd_unsafe(command_formatted)
        cmd_unsafe("say ran: {}".format(command_formatted))
        
################

class CommandQuery(Command):
  def __init__(self):
    self.name = "$autobabble"
    # <case sensitive (default: yes)>
    self.description = "'$autobabble <phrase> <response ({src} will insert the line the phrase was found in)>' searches the console for the phrase. If found, the response is said."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    if len(args) == 0:
      yap("Autobabble needs a phrase and response.")
    elif len(args) == 1:
      if args[0] in state.autobabbles:
        del state.autobabbles[args[0]]
        yap("'{}' will no longer result in babbling.".format(args[0]))
        
      else:
        yap("Autobabble needs a response.")
    else:
      state.autobabbles[args[0]] = args[1]
      yap("If '{}' is in the console, then '{}' will be said.".format(args[0], args[1]))
################

class CommandVaporize(Command):
  def __init__(self):
    self.name = "$vaporize"
    self.description = "'$vaporize <player ({self}, {random}, {all})>' unfile person data." #Delete player data.
    self.is_restricted = True
  
  def execute(self, author, args, state):
    if len(args) > 0:
      victim = " ".join(args)
      
      if state.player_newdat == {}: 
        yap("persons data unexist allwise") #Any/all player data does not exist.
        return
        
      if victim == "{random}":
        victim = random.choice(list(state.player_newdat.keys()))
      elif victim == "{self}":
        victim = author
          
      if victim in state.player_newdat:
        del state.player_newdat[victim]
        messages = [
          "{} doublepluscold", #{} is extremely cold.
          "doubleplusungood person {} unpersoned",#"Doubleplusungood player {} has been vaporized.",
          #"{} has been unperson'd.",
          "{} data unfiled",#"{}'s player data has been cleared.",
          #"{} vaporized",#"{} got vaporized.",
          "{} unpersoned",#"{} is now an unperson.",
          "sended {} miniluv basement",#"{} has been sent to the miniluv basement.",
          "{} mouse program installed",#"{}, The Mouse Program Has Been Installed."
          "sended {} joycamp" #Sent {} to a labor camp.
        ]
        yap(random.choice(messages).format(victim))
        update_database(state)
        
      else:
        if victim == "{all}":
          state.player_newdat.clear()
          yap("unfile persons data allwise") #All player data has been deleted.
          update_database(state)
          
        else:
          yap("command refs unperson {}".format(victim)) #Player {} in command does not exist.
      
    else:
      yap("command unplenty arguments") #Command does not have enough arguments.
    
################

class CommandRelt(Command):
  def __init__(self):
    self.name = "$relt"
    self.description = "Prints a random Relt quote. '$relt <message>' answers a question."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    god_text = ""
    prefix = ""
    word_count = random.randrange(17)
    jbmode = False
    
    if len(args) > 0:
      if args[0] == "map":
        jbmode = True
        word_count = random.randrange(9)
      else:
        for arg in args[:-1]:
          prefix += arg
          prefix += " "
      
        prefix += args[-1] + "? "
      
    babble = random.choice(state.reltbabble)
      
    yap(prefix + "Relt says: " + babble)
    
################

class CommandFloppa(Command):
  def __init__(self):
    self.name = "$floppa"
    self.description = "'$floppa <count (default: random)>' prints a random list of barely-coherent words."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    god_text = ""
    prefix = ""
    word_count = random.randrange(8) + 1
    
    if len(args) > 0:
      try:
        word_count = int(args[0])
        
        if word_count > 100:
          yap("That is way too many words.")
          return
        
      except ValueError:
        if args[0] == "map":
          raise NotImplementedError("testicular cancer")
          
        else:
          for arg in args[:-1]:
            prefix += arg
            prefix += " "
        
          prefix += args[-1] + "? "

    nouns = ["a","a","a","gm_construct","gm_counstruct","tree","tree","map","secret","platform","building","construct","room","pool","sign","juraywood","vehicle","player","stair","cylinder","gm_flatgrass","flattywood","hack","plane","all","door","gn_pissstruct","water","man","l4d2","dooble","thumb","playermodel","credit"]
    pronouns = ["i","i","you","you","me","my","it","it's","this"]
    verbs = ["delete","add","remove","use","like","favorite","sub","enjoy","made","edit","is","it's","fly","favor","do","work","think","thumb up","forgot"]
    adverbs = ["bad","good","just","also","very"]
    adjectives = ["best","new","fun","sphere","cylinder","worst","pee","good","bad","red","green","blue","purple","black","white","dark","light","first","old","second"]
    conjunctions = ["the","and","if","then","but"]
    prepositions = ["in","with","without"]
    #filler = ["uhh...","yeah","like"]
    THING = 1
    VERB = 2
    ADVERB = 3
    ADJECTIVE = 4
    CONJUNCTION = 5
    
    
    if rand_bool(8):
      god_text += random.choice(nouns) + ' '
    else:
      god_text += random.choice(pronouns) + ' '
      
    prev_type = THING
          
        
          
    for i in range(word_count):
      if prev_type == THING or prev_type == VERB or prev_type == ADVERB:
        if rand_bool(2):        
          if rand_bool(2):
            god_word = random.choice(verbs)
            prev_type = VERB
          
            if rand_bool(4):
              if god_word[-1] == 'e':
                god_word += 'd'
              else:
                god_word += "ed"
            
          else:
            god_word = random.choice(adverbs)
            prev_type = ADVERB
            
        else:
          if rand_bool(2):
            god_word = random.choice(adjectives)
            prev_type = ADJECTIVE
            
          else:
            god_word = random.choice(conjunctions)
            prev_type = CONJUNCTION
              
      elif prev_type == CONJUNCTION or prev_type == ADJECTIVE:
        if rand_bool(2):
          god_word = random.choice(pronouns)
        else:
          god_word = random.choice(nouns)
          
          if rand_bool(4):
            god_word += 's'
          
        prev_type = THING
      
      god_text += god_word
      
      if i != word_count - 1:
        god_text += ' '
      
    yap(prefix + "Floppa says: " + god_text)
    
def run_in_source(global_state):
  global cfg
  recent_lines = [] #(index, content)
  used_line_indices = []
  ran_command = False
  log_read_count = 0
  admin = global_state.config["system"]["admin"]
  
  try:
    while True:
      print(ran_command)

      f = open(GUD_API_LOG_PATH, 'r', encoding="utf-8")
      log = f.read()
      log_read_count += 1
      lines = log.split('\n')
      
      #skip parsing if there are too few log entries
      if len(lines) <= GUD_API_RECENT_LINES_MAX:
        time.sleep(3)
        continue
        
      recent_lines = []
      
      for i in range(-GUD_API_RECENT_LINES_MAX - 1, -1):
        recent_lines.append((i + len(lines), lines[i]))
      
      if len(used_line_indices) > GUD_API_RECENT_LINES_MAX * 8:
        used_line_indices = []
      
      print(recent_lines)
      print(used_line_indices)
      
      for line_tuple in recent_lines:
        if line_tuple[0] in used_line_indices:
          pass
          
        else:
          used_line_indices.append(line_tuple[0])
          last_line = line_tuple[1]#lines[-2]
          #autobabble search
          for phrase in global_state.autobabbles.keys():
            if phrase.lower() in last_line.lower():
              response = global_state.autobabbles[phrase]
              last_line_formatted = last_line.replace(phrase, "{phrase}")
              response = response.replace("{src}", last_line_formatted)
                
              yap(response)
                
              ran_command = True
              export_cfg("cfg")
          
          #chat commands
          split_message = last_line.split(':')
          
          if len(split_message) >= 2:
            message = split_message[1][2:] #chop off leading space
            
            args = []
            is_reading_string = False
            cur_string = ""
            prev_char = 'jb55'
            is_escaped = False
            #pedophile code
            for i in range(len(message)):
              char = message[i]
              
              if is_reading_string:
              # or "'"
                if char == '"':
                  if prev_char == '\\':
                    cur_string += char
                  else:
                    is_reading_string = False
                    args.append(cur_string)
                    cur_string = ""
                elif char == '\\':
                  pass
                else:
                  cur_string += char
              else:
                if char == ' ':
                  args.append(cur_string)
                  cur_string = ""
                elif char == '"':
                  is_reading_string = True
                  cur_string = ""
                else:
                  cur_string += char
              
                if i == len(message) - 1:
                  args.append(cur_string)
              
              prev_char = char
              
            print(args)
            
            if len(args) > 0: command_name = args[0].lower()
            author = split_message[0][:-1] #chop off trailing space
            
            if command_name in global_state.commands:
              command = global_state.commands[command_name]
              args = args[1:] #cut off the command part of the arguments
              
              if command.is_restricted:
                if author == admin or GUD_API_STUPID_IGNORE_ADMIN:
                  command.execute(author, args, global_state)
                  print("executed " + command_name)
                  ran_command = True
                  export_cfg("inline")
                  
                else:
                  yap("This command is restricted.")
                  ran_command = True
                  export_cfg("inline")
                
              else:
                command.execute(author, args, global_state)
                ran_command = True
                export_cfg("inline")
                print("executed " + command_name)
                
            elif len(command_name) > 1:
              if command_name[0] == '$':
                
                yap("Unknown command '{}.' Type $help for command list.".format(message))
                
                ran_command = True
                export_cfg("inline") 
          
          else:
            #kill tracker
            kill_detected = " killed " in last_line and " with " in last_line
            #kill_detected = kill_detected or " suicided " in last_line
            if kill_detected:
              #TODO: weapon death scores
              #killed panda killed pasta with killed sauce with crowbar
              #("NotBart killed pumpkinworks with crowbar")
              
              #echo "Backshot Betty #killtf2 killed JBMan with crowbar"
              #echo "NotBart killed pumpkinworks with crowbar"
              split_killed = last_line.split(" killed ")
              split_with = split_killed[1].split(" with ")
              
              assert len(split_killed) == 2 and len(split_with) == 2
              killer = split_killed[0]
              victim = split_with[-2]
              yap("{} | {}".format(killer, victim))
              ran_command = True
              export_cfg("inline") 
              
              if not killer in global_state.player_newdat:
                global_state.player_newdat[killer] = Player("n/a", killer)
                
              if not victim in global_state.player_newdat:
                global_state.player_newdat[victim] = Player("n/a", victim)
                
              global_state.player_newdat[killer].kills += 1
              global_state.player_newdat[killer].tokens += 5
              
              global_state.player_newdat[victim].deaths += 1
              global_state.player_newdat[victim].tokens -= 2
              
              update_database(global_state)
              
      time.sleep(1)

      #clear cfg file
      if ran_command:
        cfg = []
        export_cfg("inline")
        ran_command = False
        print("previously executed command has been cleared")
      
      time.sleep(2)
      
  #OSError
  except Exception as e:
    cfg = []
    yap("failure in main command loop: {}".format(e)) # crash message
    export_cfg("inline")
    print(e)
    time.sleep(2)
    cfg = []
    export_cfg("inline")

def run_in_command_line(global_state):
  global cfg
  admin = global_state.config["system"]["admin"]
  
  while True:
    last_line = (GUD_API_CONSOLE_USER + " :  " + input("Say :"))[:256]
    print(last_line)
    time.sleep(1)
    #autobabble search
    for phrase in global_state.autobabbles.keys():
      if phrase.lower() in last_line.lower():
        response = global_state.autobabbles[phrase]
        last_line_formatted = last_line.replace(phrase, "{phrase}")
        response = response.replace("{src}", last_line_formatted)
          
        yap(response)
          
        export_cfg("cfg")
    
    #chat commands
    split_message = last_line.split(':')
    
    if len(split_message) >= 2:
      message = split_message[1][2:] #chop off leading space
      
      args = []
      is_reading_string = False
      cur_string = ""
      prev_char = 'jb55'
      is_escaped = False
      #pedophile code
      for i in range(len(message)):
        char = message[i]
        
        if is_reading_string:
        # or "'"
          if char == '"':
            if prev_char == '\\':
              cur_string += char
            else:
              is_reading_string = False
              args.append(cur_string)
              cur_string = ""
          elif char == '\\':
            pass
          else:
            cur_string += char
        else:
          if char == ' ':
            args.append(cur_string)
            cur_string = ""
          elif char == '"':
            is_reading_string = True
            cur_string = ""
          else:
            cur_string += char
        
          if i == len(message) - 1:
            args.append(cur_string)
        
        prev_char = char
      
      if len(args) > 0: command_name = args[0].lower()
      author = split_message[0][:-1] #chop off trailing space
      
      if command_name in global_state.commands:
        command = global_state.commands[command_name]
        args = args[1:] #cut off the command part of the arguments
        
        if command.is_restricted:
          if author == admin or GUD_API_STUPID_IGNORE_ADMIN:
            command.execute(author, args, global_state)
            export_cfg("inline")
            
          else:
            yap("This command is restricted.")
            export_cfg("inline")
          
        else:
          command.execute(author, args, global_state)
          export_cfg("inline")
          
      elif len(command_name) > 1:
        if command_name[0] == '$':
          
          yap("Unknown command '{}.' Type $help for command list.".format(message))
          
          export_cfg("inline") 
    
    else:
      #kill tracker goes here
      pass

    #clear cfg file
    cfg = []

def main():
  global use_command_line
  global cfg
  
  global_state = GlobalState()

  #parse_api_data(global_state)
  try:
    config_file = open("config.pydn", "r", encoding="utf-8")
    global_state.config = pydn.decode(config_file.read())
    config_file.close()
    
    use_command_line = global_state.config["system"]["use_command_line"]
    
  except FileNotFoundError:
    yap("[ERROR] Could not find 'config.pydn'. Are you sure it's in the same folder as 'gud_api.py'?")
    export_cfg("inline")
    time.sleep(1)
    cfg = []
    export_cfg("inline")
    sys.exit(1)

  try:
    data_file = open(GUD_API_DATA_PATH, "r", encoding="utf-8")
    player_data_raw = pydn.decode(data_file.read())["player_data"]
    data_file.close()
    #TODO: use player ID instead of name for this
    for player_name in player_data_raw:
      player_raw = player_data_raw[player_name]
      global_state.player_newdat[player_name] = Player("n/a", player_raw[0], player_raw[1], player_raw[2], player_raw[3])
    
  except FileNotFoundError:
    #TODO: this should get created automatically
    yap("[ERROR] Could not find 'database.pydn'. Are you sure it's in the same folder as 'gud_api.py'?")
    export_cfg("inline")
    time.sleep(1)
    cfg = []
    export_cfg("inline")
    sys.exit(1)
    
  admin = global_state.config["system"]["admin"]
  print("current admin is: {}".format(admin))

  collected_words = []
  duplicate_words = ""

  for word in global_state.god.words:
    if word in collected_words:
      duplicate_words += word
      duplicate_words += ' '
    else:
      collected_words.append(word)

  if duplicate_words != "":
    yap("[INFO] Fail in script--duplicate god words: " + duplicate_words)
  else:
    #yap("[INFO] gud_api is online. Type '$help' for a list of commands.")
    #yap("[INFO] Playerdata is being rewritten, it will not save. Type '$help' for a list of commands.")
    yap(global_state.config["system"]["start_message"])
    
    """for message in global_state.config["autoexec"]:
      #parse message
      args = []
      is_reading_string = False
      cur_string = ""
      prev_char = 'jb55'
      is_escaped = False
        
      for i in range(len(message)):
        char = message[i]
        
        if is_reading_string:
        # or "'"
          if char == '"':
            if prev_char == '\\':
              cur_string += char
            else:
              is_reading_string = False
              args.append(cur_string)
              cur_string = ""
          elif char == '\\':
            pass
          else:
            cur_string += char
        else:
          if char == ' ':
            args.append(cur_string)
            cur_string = ""
          elif char == '"':
            is_reading_string = True
            cur_string = ""
          else:
            cur_string += char
        
          if i == len(message) - 1:
            args.append(cur_string)
        
        prev_char = char
        
      command_name = args[0]
      #chop off command name
      args = args[1:]
        
      if command_name in global_state.commands:
        command = global_state.commands[command_name]
          
        command.execute(admin, args, global_state)
      else:
        yap("[ERROR] Unknown command '" + command_name + "' in autoexec.")
        export_cfg("inline")
        time.sleep(1)
        cfg = []
        export_cfg("inline")
        sys.exit(1)
        
  for i in range(GUD_API_RECENT_LINES_MAX):
    cmd("echo padding {}".format(i))"""

  export_cfg("cfg")
  print("autoexec has been executed")
  time.sleep(1)
  cfg = []
  export_cfg("inline")
  print("starting text has been cleared")

  if use_command_line:
    run_in_command_line(global_state)
    
  else:
    run_in_source(global_state)
    
if __name__ == "__main__":
  main()