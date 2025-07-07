import time
import random
import subprocess
import math

GUD_API_USER = "Backshot Betty #killtf2" #your steam name. used to prevent randos from restarting the python script
GUD_API_TICK_DELAY = 400 #sync this with the blah blah alias thingie
GUD_API_CFG_PATH = "gud_api.cfg" #where the cfg is
GUD_API_DATA_PATH = "gud_api_player_data.txt" #where the data is
GUD_API_LOG_PATH = "C:/Program Files (x86)/Steam/steamapps/common/JBMod/jbmod/console.log" #where the log file is. MAKE SURE to put '-condebug' in your launch parameters to make console.log work.
GUD_API_RECENT_LINES_MAX = 16 #how many recent console.log entries are saved when scanning for commands

# dont change these unless you want to get HAXXED
GUD_API_STUPID_RCE = False
GUD_API_STUPID_IGNORE_ADMIN = False

GUD_API_STARTING_PLAYER_DATA = 1000

#TODO: $tipz
#TODO: case independence
#TODO: $rob command
#TODO: github repo licensed under mit
#TODO: program crashes if a colon is in the message
#TODO: command queue

cfg = []
cfg_write_count = 0

def cmd(text):
  if GUD_API_STUPID_RCE:
    cfg.append(text)
  else:
    if ';' in text:
      cfg.append("say potential RCE attempt. semicolon found in command")
      print("say potential RCE attempt. semicolon found in command")
    #elif "\\" in text:
    #  cfg.append("say potential RCE attempt. back slash found in command")
    #  print("say potential RCE attempt. back slash found in command")
    else:
      cfg.append(text)
  
chang_mode = False
  
def yap(text):
  if chang_mode:
    cmd("say chang " + text)
  else:
    cmd("say " + text)
  
def print_cfg():
  for cmd in cfg:
    print(cmd)
 
def export_cfg(type):
  global cfg
  global cfg_write_count
  
  f = open(GUD_API_CFG_PATH, "w")
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
    open(GUD_API_CFG_PATH, "w").close()
    cfg = []
    f.write("say failure in export_cfg(): {}".format(e)) # crash messages
    print("export_cfg() failed!")
    
  # print info
  for txt in cfg:
    print("  " + txt)
    
  print()
  print("successfully wrote to " + GUD_API_CFG_PATH)
  cfg_write_count += 1
  f.close()
#status
def parse_api_data(state):
  f = open(GUD_API_DATA_PATH, "r")
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
      player_data[parsed_line[0]] = int(parsed_line[1])
    elif len(parsed_line) == 1:
      print("missing player data...")
    elif len(parsed_line) > 2:
      print("too much player data...")
      
  f.close()
    
  print(parsed)
  print(player_data)
  
  state.player_data = player_data
  
def update_api_data_file(player_data):
  f = open(GUD_API_DATA_PATH, "w")
  print("player data contents:")
  
  try:
    f.write("#this file regenerates automatically\n")
    f.write("#comments left in this file will not be saved\n")
    
    for pair in player_data.items():
      player = pair[0]
      data = pair[1]
      player = player.replace('\\', '\\\\')
      player = player.replace('"', '\\"')
      
      f.write('"{}" "{}"'.format(player, data))
      f.write('\n')
      
    f.close()
  except Exception as e:
    open(GUD_API_DATA_PATH, "w").close()
    cfg = []
    f.write("say failure in export_cfg(): {}".format(e)) # crash messages
    print("export_cfg() failed!")
    
  # print info
  for pair in player_data.items():
    print('  "{}" "{}"'.format(pair[0], pair[1]))
    
  print()
  print("successfully wrote to " + GUD_API_DATA_PATH)

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
    self.words = ["beautiful","dirty","dirt","stone","rough","water","smooth","harsh","jade","gold","golden","plating","plate","plated","notched","carved","carving","chiseled","tile","button","jagged","porus","spongy","sponge","carpet","wall","floor","dull","shiny","special","clay","mud","sand","magma","lava","leaves","wood","bark","cloth","concrete","curtain","striped","flag","sign","pillar","column","linoleum","quartz","planks","screen","metal","iron","fur","plastic","tinny","tin","steel","marble","marbled","meat","meaty","slippery","red","orange","yellow","lime","green","blue","indigo","purple","magenta","black","pink","white","light","dark","grey","black","brown","rouge","lemon","sour","foul","awful","amazing","book","paper","leather","glass","glassy","wet","hot","cold","warm","lukewarm","rock","boulder","moss","mossy","abstract","geometric","artistic","algebraic","archaic","simple","crude","basic","cell","battery","tissue","outlet","screw","nail","iridescent","refractive","pearlescent","pearl","cracked","shattered","torn","worn","broken","java","script","cascading","style","sheet","hypertext","markup","language","powder","powdered","calculus","wave","tangent","square","root","gradient","papyrus","cactus","thorny","terrain","rocky","mountain","enormous","miniscule","firey","string","array","set","map","hash","hashed","text","textual","texture","generic","bland","obtuse","simple","obsidian","geode","ruby","platform","sludge","random","procedural","predictable","c","ansi","plus","flower","bone","boned","ball","grass","weed","roof","shingles","cancer","glowing","glowy","glow","bitwise","fractal","recursive","insane","crazy","self","similar","structure","logical","assembly","low","level","with","flat","sprite","buffer","file","stream","memory","pixel","bottle","ur","heaven","bubble","bubbles","sequence","glitter","glittery","sparkles","sparkly","fancy","holy","temple","frutiger","aero","bar","bars","barred","wavy","null","void","pointer","flooring","machine","machinary","graph","mushroom","stalk","trunk","oak","pine","ghost","gum","table","brain","positive","negative","electron","electric","spark","glaze","wine","bread","skin","blood","lambda","foo","baz","jet","theta","pi","ceiling","tube","lamp","lantern","pattern","design","serpent","apple","software","abraham","angel","theology","cloud","edges","edge","blobs","border","noise","bort","gradient","phonks","bart","jb","jbmod","man","guy","relt","wawa","chang","charoid","reltoid","take","my","meds","fat","boy","big","money","william","banks","is","a","good","person","maluch","xenia","modification","api","cayama","slop","sloppy","sloppiest","girl","cock","slim","how","to","start","god","bless","usa","floppa","floppoid","pornist","penile","B==============D~~~~~~~~~~-----","little","steam","steamy","freak","freaky","fur","bling","ping","pong","computer","processor","computation","global","local","logarithmic","exponential","table","in","or","out","commodore","64","amiga","atari","dictionary","complete","scrap","scrapped","scraps","scrapper","incomplete","abandoned","unfinished","finished","some","command","description","pounds","butter","butter","honolulu"]
    
class GlobalState:
  def __init__(self):
    self.hangman = HangmanManager()
    self.god = GodManager()
    self.player_data = {} # "steam id" : tokens
    self.player_names = {} # "steam id" : "player name"
    self.player_ids = {} # "player name" : "steam id"
    
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
    #    |
    #    |---god variables~~
    
    #TODO: explain custom state
################

class CommandHelp(Command):
  def __init__(self):
    self.name = "$help"
    self.description = "'$help' prints a list of commands. '$help <command>' prints a description of the command."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if len(args) == 0:
      commands_text = ""
      i = 0
      
      for command in commands:
        #proper grammer
        if i > 0:
          commands_text += ", "
          
        commands_text += command
        
        i += 1
      
      yap("command list: " + commands_text)
    
    else:
      command_name = args[0].lower()
      command_help = commands[command_name]
      command_restricted = "yes" if command_help.is_restricted else "no"
      yap("restricted? {}. {}".format(command_restricted, command_help.description))

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
      yap("this command has been run {} time".format(self.iota_counter))
    else:
      yap("this command has been run {} times".format(self.iota_counter))
    
################

class CommandTest(Command):
  def __init__(self):
    self.name = "$test"
    self.description = "HELP!"
    self.is_restricted = False
  
  def execute(self, author, args, state):
    yap("HELP!")
    
################

class CommandQuestioneyQuestioneyQuestioney(Command):
  def __init__(self):
    self.name = "$???"
    self.description = "prints statistics and info about the current gud_api session."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    yap("console.log entries: {}. console.log reads: {}. gud_api.cfg writes: {}. current user: {}".format(len(lines), log_read_count, cfg_write_count, GUD_API_USER))
    
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
    self.description = "'$god <count (default: random)>' prints a list of random words."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    god_text = ""
    word_count = 0
    
    if len(args) == 0:
      word_count = random.randrange(16) + 1
    else:
      word_count = int(args[0])
      
      if word_count > 100:
        yap("that is way too many words")
        return
    
    for i in range(word_count):
      god_text += state.god.words[random.randrange(len(state.god.words))]
      god_text += ' '
      
    yap("God says: " + god_text)

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

class CommandCIP(Command):
  def __init__(self):
    self.name = "$cip"
    self.description = "install cip software onto the server."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    yap("The Mouse Program Has Been Installed.")
      
################

class CommandWalk(Command):
  def __init__(self):
    self.name = "$walk"
    self.description = "forces the person running gud_api to walk forward."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    yap("forcing {} to walk".format(GUD_API_USER))
    cmd("+forward")
    cmd("wait 5000")
    cmd("-forward")
      
################

class CommandHangman(Command):
  def __init__(self):
    self.name = "$hangman"
    self.description = "'$hangman <max incorrect guesses (default: 5)>' start a game of hangman."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    state.hangman.guesses_right = []
    state.hangman.guesses_wrong = []
    state.hangman.answer = state.god.words[random.randrange(len(state.god.words))]
    
    if len(args) > 0:
      state.hangman.max_wrong = int(args[0])
    
    
    hint_text = ""
    
    for char in state.hangman.answer:
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
    if random.randint(0, 100) == 50:
      yap("How To Enter Relt's Casino.")
      
    if author in state.player_data:
      if len(args) > 0:
        bet = int(args[0])
      
      if state.player_data[author] - bet < 0:
        yap("you only have {} tokens...".format(state.player_data[author]))
        return
      elif bet < 0:
        yap("you cannot bet negative tokens!")
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
        #("()'", SLOT_CHERRY),
        (" 7 ", SLOT_7),
        #("(v)", SLOT_HEART),
        ("$$$", SLOT_BIG_MONEY),
        #("GOD", SLOT_GOD),
        #("CNG", SLOT_CHANG),
        #("MLH", SLOT_MALUCH),
        ("RLT", SLOT_RELT)
        #("ZEN", SLOT_ZENNY),
        #(" U ", SLOT_HORSESHOE),
        #("nMn", SLOT_CROWN),
        #("<> ", SLOT_DIAMOND),
        #("(|)", SLOT_SPADE),
        #("<>'", SLOT_LEMON)
      ]
      choices = [-1,-1,-1]
      
      choices[0] = random.choice(slots)
      choices[1] = random.choice(slots)
      choices[2] = random.choice(slots)
      
      slot_mult = len(slots)
      
      display_text = "|{}|{}|{}|".format(choices[0][0],choices[1][0],choices[2][0])
      choice_sum = choices[0][1] + choices[1][1] * slot_mult + choices[2][1] * slot_mult * 2
      earned_tokens = 0
      info = ""
      
      if choice_sum == SLOT_BAR + SLOT_BAR * slot_mult + SLOT_BAR * slot_mult * 2:
        earned_tokens = 10
      elif choice_sum == SLOT_7 + SLOT_7 * slot_mult + SLOT_7 * slot_mult * 2:
        earned_tokens = 777
      elif choice_sum == SLOT_BIG_MONEY + SLOT_BIG_MONEY * slot_mult + SLOT_BIG_MONEY * slot_mult * 2:
        earned_tokens = 25
      elif choice_sum == SLOT_RELT + SLOT_RELT * slot_mult + SLOT_RELT * slot_mult * 2:
        earned_tokens = 1000
      else:
        for slot in choices:
          if slot[1] == SLOT_BAR:
            earned_tokens += 2
        
        
      if earned_tokens == 0:
        info = "you lost..."
      elif earned_tokens == 1000:
        info = "BIG MONEY!!!"
      else:
        info = "you won!!!"
        
      earning = bet * earned_tokens - bet
      
      yap("bet {} tokens. results: {}. {} {} tokens earned".format(bet, display_text, info, earning))
      state.player_data[author] += earning
    else:
      state.player_data[author] = GUD_API_STARTING_PLAYER_DATA
      yap("token count for {}: {}".format(author, state.player_data[author]))
      
    update_api_data_file(state.player_data)

################

class CommandInput(Command):
  def __init__(self):
    self.name = "$input"
    self.description = "provides a way to interact with game commands ($hangman). this command may or may not be changed."
    self.is_restricted = False
  
  def execute(self, author, args, state):
    if state.hangman.playing:
      if len(args) == 0:
        yap("guess cannot be empty")
        
      else:
        state.hangman.current_players.append(author)
      
        guess = args[0].lower()
        is_correct = False
        text = ""
        
        if guess in state.hangman.guesses_right or guess in state.hangman.guesses_wrong:
          text = "that's already been guessed..."
          
        elif len(guess) == len(state.hangman.answer):
          if guess == state.hangman.answer:
            yap("you won!!! the answer was '{}'. incorrect guesses: {}".format(state.hangman.answer, len(state.hangman.guesses_wrong)))
            state.hangman.playing = False
          else:
            text = "guess is incorrect..."
            state.hangman.guesses_wrong.append(guess)
          
        elif len(guess) > 1:
          yap("guess can only be a single letter or the whole word!")
        
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
              
              yap("you won!!! the answer was '{}'. guesses: {}. 50 tokens have been given to each participating player".format(state.hangman.answer, len(state.hangman.guesses_right) + len(state.hangman.guesses_wrong)))
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
              
              yap("you lost... the answer was '{}'. 50 tokens have been deducted from each participating player".format(state.hangman.answer))
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
      yap("this command can only be used when $hangman is active")
  
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
    self.description = "clears console.log."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    f = open(GUD_API_LOG_PATH, "w")
    for i in range(GUD_API_RECENT_LINES_MAX):
      f.write("padding {}\n".format(i))
    
    f.close()
    yap("console.log has been successfully cleared")
    
################

class CommandHalt(Command):
  def __init__(self):
    self.name = "$halt"
    self.description = "halts and exits the gud_api script."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    yap("gud_api has been halted. commands will not work")
    export_cfg("cfg")
    time.sleep(3)
    cfg = []
    export_cfg("cfg")
    exit(1)

################

class CommandCrash(Command):
  def __init__(self):
    self.name = "$crash"
    self.description = "causes an intentional crash."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    print("a" + 1)

################

class CommandRestart(Command):
  def __init__(self):
    self.name = "$restart"
    self.description = "exits and relaunches the gud_api script."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    yap("gud_api is being restarted... commands will not work")
    export_cfg("cfg")
    time.sleep(3)
    cfg = []
    export_cfg("cfg")
    subprocess.call(["py", __file__])
    exit(1)

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
      person = args[0]
      external_check = True
      
    if person in state.player_data:
      yap("{}'s stats: {} tokens".format(person, state.player_data[person]))
    else:
      if external_check:
        yap("{} has not been registered".format(person))
        
      else:
        state.player_data[person] = GUD_API_STARTING_PLAYER_DATA
        yap("you have no stats! {} has been successfully registered. you have been given 1000 tokens".format(person))

################

class CommandSave(Command):
  def __init__(self):
    self.name = "$save"
    self.description = "save stats."
    self.is_restricted = True
  
  def execute(self, author, args, state):
    #TODO: save previously recorded stats
    f = open(GUD_API_LOG_PATH, "w")
    for i in range(GUD_API_RECENT_LINES_MAX):
      f.write("padding {}\n".format(i))
    
    f.close()
    yap("console.log has been successfully cleared")
    
################

commands = {
  "$help": CommandHelp(),
  "$god": CommandGod(),
  "$kill": CommandKill(),
  "$cip": CommandCIP(),
  "$iota": CommandIota(),
  "$chang": CommandChang(),
  "$walk": CommandWalk(),
  "$hangman": CommandHangman(),
  "$input": CommandInput(),
  "$roll": CommandRoll(),
  "$casino": CommandCasino(),
  "$stats": CommandStats(),
  "$save": CommandStats(),
  "$test": CommandTest(),
  "$???": CommandQuestioneyQuestioneyQuestioney(),
  "$clear": CommandClear(),
  "$halt": CommandHalt(),
  "$restart": CommandRestart(),
  "$crash": CommandCrash()
}

recent_lines = [] #(index, content)
used_line_indices = []

global_state = GlobalState()

parse_api_data(global_state)

#time.sleep(10)

print("current user is: {}".format(GUD_API_USER))

yap("gud_api is online. type '$help' for a list of commands")
export_cfg("inline")
print("starting text has been executed")

time.sleep(1)

cfg = []
export_cfg("inline")
print("starting text has been cleared")

ran_command = False
log_read_count = 0
#TODO: clean up code involving this
previous_command_idx = -1
previous_command = ""

try:
  while True:
    print(ran_command)

    f = open(GUD_API_LOG_PATH, 'r')
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
    
    if len(used_line_indices) > GUD_API_RECENT_LINES_MAX * 2:
      used_line_indices = []
    
    print(recent_lines)
    print(used_line_indices)
    
    for line_tuple in recent_lines:
      if line_tuple[0] in used_line_indices:
        pass
        
      else:
        used_line_indices.append(line_tuple[0])
        last_line = line_tuple[1]#lines[-2]
          
        split_message = last_line.split(':')
          
        if len(split_message) >= 2:
          message = split_message[1][2:] #chop off leading space
          args = message.split(' ')
          command_name = args[0].lower()
          author = split_message[0][:-1] #chop off trailing space
          
          if previous_command == command_name:
            yap("this command has already been used 1")
          
          if command_name in commands:
            command = commands[command_name]
            args = args[1:] #cut off the command part of the arguments
            
            if command.is_restricted:
              if author == GUD_API_USER or GUD_API_STUPID_IGNORE_ADMIN:
                command.execute(author, args, global_state)
                print("executed " + command_name)
                ran_command = True
                export_cfg("inline")
                
              else:
                yap("this command is restricted")
                ran_command = True
                export_cfg("inline")
              
            else:
              command.execute(author, args, global_state)
              ran_command = True
              export_cfg("inline")
              print("executed " + command_name)
              
          elif len(command_name) > 1:
            if command_name[0] == '$':
              
              yap("unknown command '{}', type $help for command list".format(message))
              
              ran_command = True
              export_cfg("inline")
              print("executed " + command_name)
        
          #time.sleep(1)
          
    time.sleep(1)

    
    #time.sleep(1)
    #clear cfg file
    if ran_command:
      cfg = []
      export_cfg("inline")
      ran_command = False
      print("previously executed command has been cleared")
    
    time.sleep(2)
        
#OSError
except OSError as e:
  cfg = []
  yap("failure in main command loop: {}".format(e)) # crash message
  export_cfg("inline")
  print(e)
  time.sleep(2)
  cfg = []
  export_cfg("inline")