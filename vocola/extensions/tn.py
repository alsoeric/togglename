# """process
    # get region
    # Once we have region, fragment into components, one component at a time.
    # components are:
        # stringname
        # codename
        # bangbangname
        # notname #garbange can, whitespace, codelitmeter + blah 
        
        
        
        
    # predicats are :
        # (is stringname) and (not cursor needed )and (string_to_code)
        # (is stringname )and (cursor needed) and (string_to_code)
        
        # (is codename )and (not cursor needed) and (not string_to_code)
        # (is codename )and (cursor needed) and (not string_to_string)


# ----------------------------

# Toggle Box: Programing by speach
# A collection of editor tools for easy to dictate and read code formaters.


# The fundimental problem that arises when dictating code is syntaxs.
# It is slow and annoying to dictate every open_square_bracket close_square_bracket
# every under_score and every exclamation point equals.

# This coupled with the problems that dictation software has with English syntaxs,
# such as capatlasation and using spaces in between words rather then underscores;
# makes coding by speach a complex time consuming task.

# Toggle Box is the solution.

# String-names solve the problem of having dictated variables.

# A string-name is, simply, an illgal variable name that is in plain english such as:
    # a long river
    # input stack
    # parrent node
    # temp value
    # error flag
# These would normaly throw an error when being assigned to. 
# When coding we tend to use the same variable names more then one time, and in more
# then one scope or project. So we pair each string-name to a code-name. A python legal 
# variable name, such as:
    # aLongRiver
    # input_stack
    # parrentNode
    # tmpvar
    # ERROR_FLAG

# After dictating the code, simply call Toggle Box's apropriate command and all string-name
# will automaticly converted into code-name.

# Here is an example of pre toggle and post toggle code:

# class Train():
    # def __init__(self):
        # self.is moveing = True

    # def running():
        # while self.is moving:
            # self.blow horn()
            # if distance to next city < self.stopping distance:
                # self.slow down()

# class Train():
    # def __init__(self):
        # self.is_moveing = True

    # def running():
        # while self.is_moving:
            # self.blow_horn()
            # if cityDist < self.stopDist:
                # self.reduseSpeed()

# If however a string-name does not have a pair mached to it, it will be suffixed by "!!unknown"
# when this happens, one of ToggleBox's fix commands should be called, that will repalce the "unknown"
# with the curser, for quick typing of the desired code-name. Then Fix Next should be called,
# all following accurances of the string-name will be replaced by the newly matched code-name.

# There are also methods avalble to revert code-names back into string-name, and match code-names to string-names.

# -----------------------------------------------

# Sceloton commands and bone-names.
# Quck generation of symbol heavy syntaxs.

# Another problem that accurs when dictating code are symbol syntaxs.

# Skeloton commands generate the empty shell of a regular coding pattern such as deffining new methods. 
# Using that example the 'new method' skellton command would generate:

          
# new method:count backwards arg list:up to:
    # for count in range arg list:0, up to, -1:
        # print count

# new method:count backwards arg list:up to:
    # while up to > 0:
        # print up to
        # up to += 1




# """
import logging
import sqlite3dbm
import re


logging.basicConfig(filename='./toggle_name.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)
logging.debug('------------ start of tn.py run ------------------')


toggle_name_DB = "./togglename.sqlite"


language_keywords = ['and',
                    'del',
                    'from',
                    'not',
                    'while',
                    'as',
                    'elif',
                    'global',
                    'or',
                    'with',
                    'assert',
                    'else',
                    'if',
                    'pass',
                    'yield',
                    'break',
                    'except',
                    'import',
                    'print',
                    'class',
                    'exec',
                    'in',
                    'raise',
                    'continue',
                    'finally',
                    'is',
                    'return',
                    'def',
                    'for',
                    'lambda',
                    'try',
                    'self',
]

CURSOR_MARKER = "\x01"

class sqlHandle():
    def open(self):
        """Opens sql DB @ self.handle"""
        try:
            self.handle = sqlite3dbm.dbm.open(toggle_name_DB, 'c')    
        except sqlite3dbm.dbm, error:
            logging.debug( "N2C %s" %(repr(error)))
            raise
            
    def close(self):
        """Closes sql DB"""
        del self.handle
    
    def ci_val_lookup(self, key):
        return self.val_lookup (key)
    
    def val_lookup(self, key):
        """Returns the value at self.handle[key] or None"""
        self.open()
        val = self.handle.get(key, None)
        logging.debug("SQL val look up with key |%s|: |%s|" % (key, val))
        self.close()
        return val
    
    def key_lookup(self, search_val):
        """Returns the key that returns val in self.handle 
        asumes that there is only one key that is set to val
        If no key, returns None"""
        # Rather then searing though all string-code pairs, when setting new string-code pairs, also set a code-string pair.
        # there shouldn't be any conflicts... :\
        self.open()
        key = next((key  for key, val in self.handle.items() if val == search_val), None)
        logging.debug("SQL key look up with val |%s|: |%s|" % (search_val, key))
        self.close()
        return key

    def ci_set_match(self,key, value):
        return self.set_match (key, value)

    def set_match(self, key, val):
        """Sets self.handle[key] to val.
        deletes any other key that points to val and returns that key
        overwrites self.handle[key]
        """
        conflict_key = self.key_lookup(val)
        self.open()
        if conflict_key:
            self.handle.pop(conflict_key)
        self.handle[key] = val
        return conflict_key

    def clear_data(self):
        self.open()
        self.handle.clear()
        self.close()
    
    
def first_word(string):
    """Returns the string of the first word in the string,
    end of string is denoted by whitespace, or punk"""
    word = ""
    for char in string:
        if char.isspace() or not char.isalpha() and not char == CURSOR_MARKER:
            break
        else:
            word += char
    return word
    
def key_word(string):
    """returns lenght of the keyword at the begining of a str"""
    fw = first_word(string)
    first_word_sans_curser = fw.replace(CURSOR_MARKER, "")
    for keyword in language_keywords:
        if first_word_sans_curser == keyword:
            return len(fw)
    return 0

class ToggleName():

    def __init__(self,data):
        
        self.data = data
        self.remainingdata = data
        
        
        self.component_list = []
        self.nesting_stack = [self.component_list]
        self.component_count = {} 
    
    def reasemble(self):
        rs = ""
        for component in self.component_list:
            data = component.present()
            rs += data
        return rs + self.remainingdata

    def goto_start(self):
        ToggleName.__init__(self, self.reasemble())
        
    def toggle(self, s2c= True, cn= True ):
        """Togglename command
        s2c = string to code. The direction of toggle. Toggle/flip
        """
                #Maybe do a if not bool(self.get_parsed_data()): self.goto_start() ?
        #I don't think there's a time that we would call toggle twice in the same isntance, but for the furture maybe?
        
        cursor_found = False
        for token in self.component():
            if cn and token.has_cursor():
                cursor_found = True
            
            if (isinstance(token, string_name) and 
                s2c == True and
                cn == cursor_found):
                token.convert()
                
            elif (isinstance(token, code_name) and 
                s2c == False and
                cn == cursor_found):
                token.convert()
            
            elif (isinstance(token, bang_name)and
                cn == cursor_found):
                token.matchname(s2c)
                
            if cursor_found:
                break
        return 
            
        
    def fix_unknown(self):
        """works though data, looking for unfilled bangname, apon finding the first one, replacing unknown with cursor
        
        cursor should not be in data,
        does a look to be sure it is not there
        """
        
        if bool(self.get_parsed_data()): #Restart the parsing to the beginning.
            self.goto_start()
        
        self.remainingdata = self.data.replace(CURSOR_MARKER,"")
        
        for part in self.component():
            if isinstance(part, bang_name):
                if part.fix_unknown():
                    break
        else:
            self.remainingdata += CURSOR_MARKER
                    
        return 

    def get_parsed_data(self):
        return self.component_list
    
    def component(self):
        """convert data into indiviual data types"""
                
        test_list = [self.q_bone_name, # looks for Bone-names, must be done before q_not_Name
                     self.q_not_Name, #looks for punkucations + whitespace + comments + quotes
                     self.q_bang_name, #handles floating !!'s
                     self.q_stringname,
                     self.q_codename,          
                    ]

        previous_token = None
        while self.remainingdata:
            for i in test_list:
                token = i()
                if token:
                    
                    if self.token_is_nesting_closeur_trigger(token):
                        self.reduse_nesting()
                    if isinstance(token, Bone_Name):
                        self.nest_token(token)
                    else:
                        self.add_token(token)
                    self.count(token)
                    if previous_token is None:
                        previous_token, token = token, None
                        break
                    yield previous_token
                    previous_token, token = token, None
                    break
        yield previous_token
                    
        return

    def token_is_nesting_closeur_trigger(self, token):
        if len(self.nesting_stack) > 1:
            return self.nesting_stack[-1].is_closing_trigger(token)
        else:
            return False
        

    def add_token(self, token):
        if len(self.nesting_stack) > 1:
            self.nesting_stack[-1].append(token)
        else:
            self.component_list.append(token)

    def nest_token(self, token):
        self.add_token(token)
        self.nesting_stack.append(token)

    def reduse_nesting(self):
        if len(self.nesting_stack) == 1:
            return
        else:
            self.nesting_stack.pop()

                
    def count(self, component):
        """increments the compnent types count by 1 in self.component_count"""
        self.component_count[component.__class__] = self.component_count.get(component.__class__, 0) + 1

    @staticmethod
    def white_space(string):
        """Returns length of whitespace type in the start of the string"""
        length = 0
        for character in string:
           if character.isspace():
                length += 1
           else: break
        return length
        

    @staticmethod            
    def punk(string):
        """returns the lenght of puncuation at the beggining of str"""
        length = 0
        for index, char in enumerate(string):
            if char.isalnum() or char in ("_", CURSOR_MARKER, "#", "'", '"', '"""') or char.isspace():
                break
            
            if string[index:].startswith("!!"):
                break
                
            length += 1
        return length
    @staticmethod        
    def quote_string(string):
        """Returns the lenght of quoteString at the begginging of str"""
        
        qs = ('"""', "'", '"')
        q = None
        for quote in qs:
            if string.startswith(quote):
                q = quote
                break
        if q == None: return 0
        #~ logging.debug("NN qs dectected|%s|"%string)
        index = len(q)
        end_index = len(string)
        while end_index > index:
            if string[index:].startswith(q):
                return index+len(q) 
            index += 1
        return end_index
    @staticmethod        
    def hash_comment(string):
        """Returns the lenght of the comment at the beggining of string"""
        if not string.startswith("#"):
            return 0
        nl_index = string.find("\n")
        if nl_index == -1:
            return len(string)
        else:
            return nl_index
        
    def get_count(self):
        """Returns a tuple of 4 ints. Each int corisponding to the count of component types in the order of nn bn sn cn"""
        result = []
        for type in [not_name,
                     bang_name,
                     string_name,
                     code_name]:
            result.append(self.component_count.get(type, 0))
        #~ logging.debug(str(self.component_count))
        return tuple(result)
        
    def q_not_Name(self):
        """Returns not_name Object and updates self.remaningData
        otherwise returns None"""
        #Insepts self.data for n things
        #Languare keywords
        #untouchables, (quote strings & comments)
        #whiteSpace
        #puncuation (not inculding '_' or '\x01' or #)
        #Ignores 
             
            
        not_name_test_list = [(self.hash_comment, comment_not_name),
                              (key_word, None),
                              (self.white_space, w_space_not_name),
                              (self.quote_string, quote_not_name),
                              (self.punk, not_name),
                              ]
        
        length = 0
        flag = True
        while flag:
            flag = False
            for test, sub_class in not_name_test_list:
                l = test(self.remainingdata[length:])
                if l:
                    length += l
                    flag = True
                    if test is key_word: #To prevent keywords from eating bonenames
                        flag = False
                    break
        
        if length == 0:
            return None        
        
        not_Name_obj = not_name(self.remainingdata[:length])
        self.remainingdata = self.remainingdata[length:]
        return not_Name_obj
    
    
    def q_key_name(self):
        #(key_word, key_name),
        l = key_word(self.remainingdata)
        if l:
            key = key_name(self.remainingdata[l:])
            self.remainingdata = self.remainingdata[l:]
            return key
        else:
            return None
    
    def q_codename(self):
        """Returns codename componendt from the front of self.remaining data
        assumes that self.reaningdata does NOT start with a keyword"""     
        length = 0
        for char in self.remainingdata:
            if not char.isalnum() and char not in (CURSOR_MARKER, "_"):
                break
            length += 1
        
        if length == 0: return None
                            
        bn = self.q_bang_name(length)
        if bn: return bn
        
        
        data = self.remainingdata[:length]
        self.remainingdata = self.remainingdata[length:]
        
        return code_name(data)
        
    def q_bang_name(self, start_index=0):
        """Returns bangobject
        is used in q_stringname and q_codename
        also in compontent tests

        looks for !!codename at self.remainingdata[index:]
        start_index = int # place in self.remaining data that is looked at
        """
        if self.remainingdata[start_index:].startswith("!!"):
            bang_offset = 2 
            
        elif self.remainingdata[start_index:].startswith("!"+CURSOR_MARKER+"!"):
            bang_offset = 3
        else:
            return 0
            
        pre_bang_str = self.remainingdata[:start_index + bang_offset]
        self.remainingdata = self.remainingdata[start_index + bang_offset:]
        
        post_bang_data = self.q_codename()#Calls q_codename to capture whateever is after the !!
        if post_bang_data is None: #will only happen if for some reason a !! is followed by nothing.
            post_bang_string = "" #Should this be a "unknown"?
        else:
            post_bang_string = post_bang_data.present()
        return bang_name(pre_bang_str + post_bang_string)
    
    
    def q_stringname(self):
        
        name_string = ""
        #~ cursor = False
        if self.remainingdata[0].isdigit():
            return None
        for char in self.remainingdata:
            if char == CURSOR_MARKER:
                #~ name_string = "\x01" + name_string
                pass
                #~ continue
            
            elif char == " ":
                #if the next char is not alunum or is a keyword
                #it marks the end of string_word
                #except in the case where the curser is after a space
                name_len = len(name_string)
                next_is_keyword = key_word(self.remainingdata[name_len+1:])
                try:
                    next_is_alnum = self.remainingdata[name_len+1].isalnum()
                    next_is_cursor = self.remainingdata[name_len+1] == CURSOR_MARKER
                except IndexError:
                    return None
                
                if next_is_keyword or not next_is_alnum and not next_is_cursor:
                        break
            elif not char.isalnum():
                if char == "_":
                    #Bumped into a code_word, remove chars untill " " is hit
                    name_string = name_string.rsplit(" ", 1)[0]
                    #Then remove " "
                    #~ name_string = name_string.rstrip("\x01")
                    #~ name_string = name_string.rstrip(" ")
                    
                    #~ print("|%s|"%name_string)

                    
                break
            
            name_string += char
        
        name_string = name_string.rstrip(" ")
        if name_string == "" or " " not in name_string:
            return None
        
        name_len = len(name_string)
        #bang bang lookup
        bb = self.q_bang_name(name_len)
        if bb: return bb
        
        #intisigate string_name 
        sn = string_name(self.remainingdata[:name_len])
        #update remainingdata
        self.remainingdata = self.remainingdata[name_len:]
        
        return sn
                
    def q_bone_name(self):
        """
        returns a bone-name token, if self.remaining_data starts with a vaild bone_name, else returns None
        also updates self.remainingdata

        will not nest the colon name, only detect.
        
        All bonenames must be two words seperated by whitespace
        """
        token = None
        previous_token = None
        before_last_token = None
        space_token = None
        bn_string = ""
        re_pattern = r"[a-zA-Z0-9]* [a-zA-Z0-9]*$"
        
        if not self.remainingdata.startswith("::"):
            return token
        #Possible chance for bone name.
        #work backwards untill two 'words' are captured.
        #if a stringname is first, then it is insured that
        #we will have >= 2 words
        previous_token = self.nesting_stack[-1][-1]
        if isinstance(previous_token, string_name):
            bn_string = re.search(re_pattern, previous_token.data)
            if bn_string is not None:
                bn_string = bn_string.group()

        elif isinstance(previous_token, (code_name, pass_name)):
            #work backwards untill two words are grabbed,
            before_last_token = self.nesting_stack[-1][-2]
            if before_last_token.data == " ":
                space_token = before_last_token #returns None
                before_last_token = self.nesting_stack[-1][-3]
                string = " ".join([before_last_token.data,
                               previous_token.data],)
            else:
                string = "".join([before_last_token.data,
                               previous_token.data],)
            logging.debug("QBN looking at |%s|"%string)
            bn_string = re.search(re_pattern, string)
            
            if bn_string is None:
                print("ffuuu")
                return None
            bn_string = bn_string.group()
            
            
                
        token = Bone_Name.new(bn_string)
        if token is None:
            return token
        
        elif before_last_token is None: 
            croped_data = previous_token.data.rpartition(bn_string)[0]
            logging.debug("QBN BLTisNone remaining data: |%s|"%croped_data)
            if not croped_data == "":
                previous_token.data = croped_data
            else:
                previous_token.convert_to_nullname()
            
        else:
            #datas = [before_last_token.data + " ", previous_token.data]
            #datas = self._crop_strings(datas, bn_string)
            #logging.debug("QBN croped_string: |%s|"%datas)
            previous_token.convert_to_nullname()
            if space_token is not None:
                space_token.convert_to_nullname()
            cropedd_string = before_last_token.data[:len(previous_token.data) - len(bn_string)]
            if cropedd_string == "":
                before_last_token.convert_to_nullname()
            else:
                before_last_token.data = cropedd_string
#datas[0]
    
        #remove the "::"
        self.remainingdata = self.remainingdata[2:]
        return token
        
    @staticmethod
    def _crop_strings(list_of_strings, search_string):
        """returns a edited version of arg1
        crop off as much of search_string that
        exists at the end of each string. also cropping search_string""" 
        result_strings = []
        for s in list_of_strings:
            print(s)
            for i in range(len(search_string),0,-1):
                print(i, search_string[:i], s.endswith(search_string[:i]))
                if s.endswith(search_string[:i]):
                    search_string = search_string[i:]
                    result_strings.append(s[:-i])
                    print("FAFSAF")
                    break
            else:
                result_strings.append(s[-i:])
        return result_strings
                

                    
        

class component_Parent(object):
    
    def __str__(self,):
        return "<%s |%s|>"%(self.__class__.__name__, self.data)

    def __repr__(self,):
        return self.__str__()

    def __init__(self, data, had_cursor = False):
        if had_cursor == True:
            self.had_cursor = True
        elif CURSOR_MARKER in data:
            self.had_cursor = True
            data = data.replace(CURSOR_MARKER,"")
        else:
            self.had_cursor = False
        self.data = data
    def present(self):
        """Returns string form of data
        it cursor was in data, adds cursor to the of string"""
        if self.had_cursor:
            return self.data + CURSOR_MARKER
        return self.data
        
    def has_cursor(self):
        return self.had_cursor

    def convert_to_notname(self):
        self.__class__ = not_name
    
    def convert_to_nullname(self):
        self.__class__ = null_name

    def convert_to_passname(self):
        self.__class__ = pass_name
        
class string_name(component_Parent):
    def convert(self):
        """returns new code_name or bang_name
        looks up sql database for partering codename, if none,
        returns bang_name"""
        sql = sqlHandle()
        val = sql.val_lookup(self.data.lower())
        
        if val == None:
            self.__class__ =  bang_name
            self.__init__(self.data+"!!unknown", had_cursor = self.had_cursor)
        else:
            self.__class__ = code_name
            self.__init__(val, had_cursor = self.had_cursor)
        
    
class code_name(component_Parent):
    def convert(self):
        """returns new code_name or bang_name
        looks up sql database for partering codename, if none,
        returns bang_name"""
        # store data in dictionary hidden inside an SQLlite database
        if self.data == CURSOR_MARKER: #This is here because a lone cursor is consiered a codename, however it should no be converted,
            return self
        
        sql = sqlHandle()
        string_n  = sql.key_lookup(self.data.replace(CURSOR_MARKER, ""))
        if string_n == None:
            self.__class__ = bang_name
            self.__inti__("unknown!!" + self.data, had_cursor = self.had_cursor)
        else:
            self.__class__ = string_name
            self.__init__(string_n, had_cursor = self.had_cursor)
    

class bang_name(component_Parent):
    def matchname(self, s2c):
        """Returns a string_name or code_name if bang_name has been
        filled out.
        Otherwise returns a copy of itself."""
        # store data in dictionary hidden inside an SQLlite database
        #What happends in the case of "  !!cod_name" ? should do testing
        str_name , cod_name = self.data.split("!!")
        str_name = str_name.lower()
        if "" in (str_name, cod_name):
            return self
        
        sql = sqlHandle()
        
        if s2c:
            end_type = code_name
            goal_name = cod_name
            other_name = str_name
            lookup = sql.val_lookup
        else:
            end_type = string_name
            goal_name = str_name
            other_name = cod_name
            lookup = sql.key_lookup
            
            
        if "unknown" == other_name:
            pass 
        elif "unknown" == goal_name:
            #look up if it has been updated
            goal_name = lookup(other_name)
            if goal_name is None:
                return self
                
        else:
            conflict = sql.set_match(str_name, cod_name)
        
        self.__class__ = end_type
        self.__init__(goal_name, had_cursor = self.had_cursor)
        #conflict = sql.ci_set_match(str_name, cod_name)
        #return end_type(goal_name, had_cursor = self.had_cursor)

        
    
        #This might be more readable. :D
        #~ if s2c: 
            #~ if "unknown" == str_name:
                #~ return code_name(cod_name) # replace with pass?
            #~ elif "unknown" == cod_name:
                #~ #look up if it has been updated
                #~ cod_name = sql.val_lookup(str_name)
                #~ if cod_name is None:
                    #~ return self
                    #~ 
            #~ else:
                #~ conflict = sql.set_match(str_name, cod_name)
            #~ return code_name(cod_name)

    def fix_unknown(self):
        """used with fixname, to input the cursor where the unknown was
        foo bar!!unknown    -> foo bar!!cursor
        unknown!!foo        -> cursor!!foo
        !!unknown           -> cursor
        foobar!!            -> foobar!!cursor # This is needed incase someone calls fix_next without entering in a codename
        
        returns True if bangname has unknown, and will edit data
        otherwise returns false
        """
        
        left, right = self.data.split("!!")
        if "unknown" not in (left, right):
            return False
        
        if right == "unknown":
            right = CURSOR_MARKER
        elif left == "unknown" or CURSOR_MARKER:
            left = CURSOR_MARKER
        
        if left == "":
            self.data = right    
        else:
            self.data = left + "!!" + right
        return True

class not_name(component_Parent):
    pass

class key_name(component_Parent):
    pass

class quote_not_name(component_Parent):
    pass

class comment_not_name(component_Parent):
    pass

class w_space_not_name(component_Parent):
    pass

class null_name(component_Parent):
    """A null name,
    if a token is converted to this class, will essentally be deleted
    """
    def present(self):
        return ""

class pass_name(component_Parent):
    def convert(self):
        return

class Bone_Name(component_Parent):
    """
    """

    def __init__(self,):
        component_Parent.__init__(self, self.__class__.__name__.lower().replace("_", " ",) + "::")
        self.nesting_list = []
        self.prefix = ""
        self.suffix = ""
        self.had_cursor = False
        self.trigger = "\n"
        
#        self.set_bones("(",")") # default bones, 
                                # to be used to testing only, 
                                # subclasses should use this 
                                # method to asign what it formats
                                # (prefix, sufix)
    @staticmethod    
    def get_valid_names():
        
        valid_names = {sub_class.__name__.lower().replace("_", " "):sub_class for sub_class in Bone_Name.__subclasses__()}
        #valid_names = {"arg list": ""}
        return valid_names
    
    @staticmethod
    def new(boneString):
        """Returns the correct subclass instance of boneString, or None if there is no subclass of with that name"""
        subclass = Bone_Name.get_valid_names().get(boneString, None)
        if subclass is not None:
            return subclass()
        else:
            return None

    def __str__(self):
        return "<%s |%s|>"%(self.__class__.__name__, self.nesting_list)
    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.nesting_list[key]
    
    def append(self, token):
        self.nesting_list.append(token)
    
    def set_bones(self, prefix, suffix):
        self.prefix = prefix
        self.suffix = suffix


    def present(self,):
        val =  [self.prefix]
        #dealing with the seperators for dictionars looks to be tricky,
        #sepcount = 0
        for t in self.nesting_list:
            val.append(t.present())
            #val.append(self.sep[sepcount])
            #selcount = (sepcount + 1)%len(sepcount)
        val.append(self.suffix)
        return "".join(val)

    def is_closing_trigger(self, token):
        if isinstance(token, not_name):
            if self.trigger in token.data:
                return True
        return False

    def work_with(self, token):
        """Abastract method,
        If a bonename must directly edit a token that is inside itself. But does not nessassarrly have anything to do with it's trigger
        """
        return
            

class Arg_list(Bone_Name):
    def __init__(self):
        Bone_Name.__init__(self)
        self.set_bones("(",")")
    
class New_tuple(Arg_list, Bone_Name):
    pass

class Quoted_tripple(Bone_Name):
    def __init__(self):
        Bone_Name.__init__(self)
        self.set_bones('"""', '"""')
        self.trigger = Quoted_tripple
    def is_closing_trigger(self, token):
        # will not close being q_bonename will not go
        # because the previous token will be turned into 
        # notnames
        if isinstance(token, Quoted_tripple):
            token.convert_to_nullname()
            return True
        token.convert_to_passname()
        return False

class Open_With(Bone_Name):
    """ open with:: "foo.txt" as foo
    ->  with open("foo.txt") as foo:
    oop:
        get the presented form of inards: | "foo.txt" as foo|
        rsplit(" as ",1)
      """
    def __init__(self):
        Bone_Name.__init__(self)
        self.set_bones("with open(",
                       ":")
    
    def present(self):
        
        contence = "".join([t.present() for t in self.nesting_list])
        contence = contence.rsplit(" as ", 1)
        #contence = [s.strip() for s in contence]
        logging.debug("WOP present |%s|"%contence)
        result = self.prefix + ") as ".join(contence)
        if not result.endswith(":\n") or result.endswith(":") :
            result += ":"
        return result

class With_Open(Open_With, Bone_Name):
    pass
