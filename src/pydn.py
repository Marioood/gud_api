# VERSION 0.9 OF PYDN #
#                     #
#  JSON-like format   #
#  for Python data.   #
#                     #
# CREATED BY marioood #

import math
#maybe??????
#TODO: sets
#TODO: data skeletons, to verify that the data is correct
#TODO: tuples
#TODO: rewrite in a more modular way, where elements are split by colons and commas and the types are converted in a similar fashion to json.dumps()

#definitely do
#TODO: force commas
#TODO: complex numbers
#TODO: ways of writing ints (bin hex oct)
#TODO: single quotes

#TODO: better errors
#TODO: pass file name for errors ? ? ? ?

#REMINDER: comments (for the code)
  
def main() -> None:
  """f = open("test.pydn", "r")
  raw_text = f.read()
  
  decoded_dict = decode(raw_text)
  print(decoded_dict)
  f.close()"""
  
  raw_dict = {
    "foo": "bar",
    "abc": -123,
    "bool": True,
    "has_balls": False,
    "escape": "I am the \"greatest\" player ever! \\ \' \n \b \t \f \r",
    "unescape": "\\n is how you write newlines",
    #holy shit, this works!
    "depth1": {
      "foo": "bar",
      "ahh": None,
      "balls": 3.1415,
      #"bin": 0b10,
      #"hex": 0x10,
      #"oct": 0o10
      "depth2": {
        "bool": True,
        "c": math.nan
      },
      "abc": -123,
      "a": -math.inf
    },
    "txt_list": [
      "a",
      [
        1,
        2,
        3,
        {
          "foo": "bar",
          "ahh": None,
          "balls": 3.1415,
          "abc": -123,
          "a": -math.inf,
          "bool": True,
          "c": math.nan
        },
        False,
        None
      ],
      "b",
      "c",
      True
    ]
  }

  print(encode(raw_dict, "this regnerates automatically", "shit wont be saved"))
  print(decode(encode(raw_dict)))
  
class PyDNEncodeError(ValueError):
  pass
  
def decode(raw_text) -> dict:
  return decode_dict_leaf(raw_text, 0, 0)

def encode(raw_dict, *comments) -> str:
  encoded_text = encode_dict_leaf(raw_dict, 1)
  
  if len(comments) > 0:
    comments_joined = ""
    
    for comment in comments:
      comments_joined += '#' + comment + '\n'
      
    return comments_joined + '\n' + encoded_text
    
  else:
    return encoded_text
  
def decode_dict_leaf(raw_text, starting_idx, starting_depth) -> dict:
  #sort of a combined lexer and parser. should be fine for such a simple format.
  cur_depth = starting_depth
  cur_string = ""
  cur_key = ""
  parsed = {}
  #yknow... the dict parsing could also be rewritten to use a stack
  #parse lists using a stack. top of the stack contains the parent list, later indices are the children of the parent/the parent's children
  list_stack = []
  cur_list_idx = -1
  is_reading_string = False
  is_escaping_char = False
  is_adding_keyvalue = False
  is_reading_another_dict = False
  is_reading_list = False
  is_reading_comment = False
  is_reading_float = False
  #first recursion this will be True, otherwise, False
  skip_first_brace = True
  
  #add 1 to the starting idx so we skip the first '{'
  for i in range(starting_idx, len(raw_text)):
    char = raw_text[i]
    #start of file
    if i == 0:
      #doing this results in no other special cases, nice!
      prev_char = ''
    else:
      prev_char = raw_text[i - 1]
      
    #end of file
    if i == len(raw_text) - 1:
      #doing this results in no other special cases, nice!
      next_char = ''
    else:
      next_char = raw_text[i + 1]
      
    #parsing with individual characters
    if is_reading_comment:
      if char == '\n':
        is_reading_comment = False
      
    elif is_reading_another_dict:
      #when a dict is nested inside of a dict, we do not want the child dict's data being added to the parent dict
      #skip through parsing text, only making sure to count how deep we are into the child dicts
      if char == '{':
        cur_depth += 1
        
      elif char == '}':
        cur_depth -= 1
        
      if cur_depth == starting_depth:
        print("exit skip mode")
        is_reading_another_dict = False
      
    elif is_reading_string:
      #parsing for strings
      if char == '\\' and prev_char != '\\':
        is_escaping_char = True
        
      elif is_escaping_char:
        if char == '"':
          cur_string += char
          
        elif char == '\'':
          cur_string += char
          
        elif char == '\\':
          cur_string += char
          
        elif char == 'n':
          cur_string += '\n'
          
        elif char == 'r':
          cur_string += '\r'
          
        elif char == 't':
          cur_string += '\t'
          
        elif char == 'b':
          cur_string += '\b'
          
        elif char == 'f':
          cur_string += '\f'
          
        elif char == 'x':
          raise NotImplementedError("hexadecimal escape characters are not implemented yet")
          
        elif is_numeral_ascii(char):
          raise NotImplementedError("octal escape characters are not implemented yet")
          
        elif char == 'a':
          #ascii bell. doesn't exist in python... but don't worry about that :)
          cur_string += chr(7)
          
        else:
          raise SyntaxError("invalid escape character '\\{}'".format(char))
          
        is_escaping_char = False
          
      elif char == '"':
        is_reading_string = False
        if is_reading_list:
          list_stack[cur_list_idx].append(cur_string)
          
        else:
          if is_adding_keyvalue:
            parsed[cur_key] = cur_string
            is_adding_keyvalue = False
            
          else:
            cur_key = cur_string
          
        cur_string = ""
        
      else:
        cur_string += char
    
    else:
      #parsing in whitespace
      if char == '#':
        is_reading_comment = True
      
      elif char == '"':
        is_reading_string = True
        
      elif char == ':':
        if is_adding_keyvalue:
          raise SyntaxError("PYDN parsing error: colon found after colon")
          
        is_adding_keyvalue = True
        
      elif is_numeral_ascii(char) or (char == '-' and is_numeral_ascii(next_char)):
        #parsing for ints and floats
        #could this be combined with later code??? bool parsing
        #TODO: check with commas or something
        cur_string += char
          

        if next_char == '.' or next_char == 'e' or next_char == '+':
          is_reading_float = True
          
        elif not is_numeral_ascii(next_char):
          if is_reading_float:
            is_reading_float = False
            
            if is_adding_keyvalue:
              try:
                if is_reading_list:
                  list_stack[cur_list_idx].append(float(cur_string))
                  
                else:
                  parsed[cur_key] = float(cur_string)
                  is_adding_keyvalue = False
                  
                cur_string = ""
              
              except ValueError:
                raise ValueError("float parsing failed")
              
            else:
              raise SyntaxError("unexpected float found while parsing")
          
          else:
            #reading int
            if is_adding_keyvalue:
              try:
                if is_reading_list:
                  list_stack[cur_list_idx].append(int(cur_string))
                  
                else:
                  parsed[cur_key] = int(cur_string)
                  is_adding_keyvalue = False
                  
                cur_string = ""
              
              except ValueError:
                raise ValueError("int parsing failed at {}".format(i))
              
            else:
              raise SyntaxError("unexpected int found while parsing")
        
      elif char == '{':
        #don't call this function again if this is the first dict. allows for whitespace at the start of the raw text
        #also just used for every dict parse lololololol
        if skip_first_brace:
          skip_first_brace = False
          
        else:
          #start parsing a new dict (recursively, scary!!!)
          cur_depth += 1
          is_reading_another_dict = True
          if is_reading_list:
            list_stack[cur_list_idx].append(decode_dict_leaf(raw_text, i, cur_depth))
            
          else:
            parsed[cur_key] = decode_dict_leaf(raw_text, i, cur_depth)
            is_adding_keyvalue = False
        
      elif char == '}':
        #return the dict n shit
        print(parsed)
        print("RAW:" + raw_text[starting_idx + 1:] + "-----")
        return parsed
        
      elif char == '[':
        list_stack.append([])
        cur_list_idx += 1
        is_reading_list = True
        
      elif char == ']':
        cur_list_idx -= 1
        
        if cur_list_idx < 0:
          is_reading_list = False
          is_adding_keyvalue = False
          parsed[cur_key] = list_stack.pop()
          
        else:
          list_stack[cur_list_idx].append(list_stack.pop())
        
      elif char != ' ' and char != '\n' and char != ',':
        #parsing for booleans, None, inf, -inf and nan
        cur_string += char
        
        if cur_string == "True":
          if is_adding_keyvalue:
            parsed[cur_key] = True
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(True)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "False":
          if is_adding_keyvalue:
            parsed[cur_key] = False
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(False)
            cur_string = ""
          
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "None":
          if is_adding_keyvalue:
            parsed[cur_key] = None
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(None)
            cur_string = ""
            
        elif cur_string == "math.inf":
          if is_adding_keyvalue:
            parsed[cur_key] = math.inf
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(math.inf)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected inf found while parsing")
            
        elif cur_string == "-math.inf":
          if is_adding_keyvalue:
            parsed[cur_key] = -math.inf
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(-math.inf)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected -inf found while parsing")
            
        elif cur_string == "math.nan":
          if is_adding_keyvalue:
            parsed[cur_key] = math.nan
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(math.nan)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected nan found while parsing")
      
  raise EOFError("reached end of file in parse_dict_leaf()")

def encode_dict_leaf(raw_dict, starting_depth) -> str:
  #verbose and compact output?
  output_text = "{\n"
  depth = starting_depth
  i = 0
  for key in raw_dict:
    spacing = "  " * depth
    value = raw_dict[key]
    value_type = type(value)
    
    if value_type == str:
      #TODO: reformat keys (noone uses escape characters in keys, but add that anyways)
      #TODO: unicode maybe like................. hex escape characters
      value_reformatted = (value
      .replace("\\", "\\\\")
      .replace("\"", "\\\"")
      .replace("\'", "\\'")
      .replace("\n", "\\n")
      .replace("\b", "\\b")
      .replace("\f", "\\f")
      .replace("\t", "\\t")
      .replace("\r", "\\r"))
      
      output_text += '{}"{}": "{}"'.format(spacing, key, value_reformatted)

    elif value_type == dict:
      output_text += '{}"{}": {}'.format(spacing, key, encode_dict_leaf(value, depth + 1))

    elif value_type == list:
      output_text += '{}"{}": {}'.format(spacing, key, encode_list_leaf(value, depth + 1))
      
    elif value == math.nan:
      output_text += '{}"{}": math.nan'.format(spacing, key)
      
    elif value == math.inf:
      output_text += '{}"{}": math.inf'.format(spacing, key)
      
    elif value == -math.inf:
      output_text += '{}"{}": -math.inf'.format(spacing, key)
      
    elif value_type == int or value_type == float or value_type == bool or value == None:
      output_text += '{}"{}": {}'.format(spacing, key, value)
      
    else:
      raise NotImplementedError("Type {} is not implemented in PyDN.".format(value_type))
    
    
    
    if i == len(raw_dict) - 1:
      output_text += "\n"
    else:
      output_text += ",\n"
    
    i += 1
  
  output_text += "  " * (depth - 1) + '}'
  
  return output_text
  
def encode_list_leaf(raw_list, starting_depth) -> str:
  output_text = "[\n"
  depth = starting_depth
  i = 0
  for item in raw_list:
    spacing = "  " * depth
    item_type = type(item)
    
    if item_type == str:
      #TODO: hex escape characters for unicode?
      item_reformatted = (item
      .replace("\\", "\\\\")
      .replace("\"", "\\\"")
      .replace("\'", "\\'")
      .replace("\n", "\\n")
      .replace("\b", "\\b")
      .replace("\f", "\\f")
      .replace("\t", "\\t")
      .replace("\r", "\\r"))
      
      output_text += spacing + '"' + item_reformatted + '"'

    elif item_type == dict:
      output_text += spacing + encode_dict_leaf(item, depth + 1)

    elif item_type == list:
      output_text += spacing + encode_list_leaf(item, depth + 1)
      
    elif item == math.nan:
      output_text += spacing + "math.nan"
      
    elif item == math.inf:
      output_text += spacing + "math.inf"
      
    elif item == -math.inf:
      output_text += spacing + "-math.inf"
      
    elif item_type == int or item_type == float or item_type == bool or item == None:
      output_text += spacing + str(item)
      
    else:
      raise NotImplementedError("Type {} is not implemented in PyDN.".format(value_type))
    
    
    
    if i == len(raw_list) - 1:
      output_text += "\n"
    else:
      output_text += ",\n"
    
    i += 1
  
  output_text += "  " * (depth - 1) + ']'
  
  return output_text

def is_numeral_ascii(string) -> bool:
  #the vanilla isnumeric() counts weird unicode characters (like exponent signs) as numerals for some reason.
  #this function only counts the ascii 0-9 numerals as numeric.
  for char in string:
    #why do they have to murder chars in every programming language? god, i love chars in C.
    #there's none of this conversion bullshit in C when you want to check/parse numeric text. you just type char - '0'.
    char_codepoint = ord(char)
    
    if not (char_codepoint >= ord('0') and char_codepoint <= ord('9')):
      return False
      
  return True
  
if __name__ == "__main__":
  main()