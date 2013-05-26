"""process
    get region
    Once we have region, fragment into components, one component at a time.
    components are:
        stringname
        codename
        bangbangname
        notname #garbange can, whitespace, codelitmeter + blah 
        
        
        
        
    predicats are :
        (is stringname) and (not cursor needed )and (string_to_code)
        (is stringname )and (cursor needed) and (string_to_code)
        
        (is codename )and (not cursor needed) and (not string_to_code)
        (is codename )and (cursor needed) and (not string_to_string)
        
"""
import logging
import sqlite3dbm


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
#~ foo = getregion(data, s2c, cn)
#~ for part in foo.component():
    #~ part.convert()
    #~ retrline += part.present()
#~ return retrline

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
        self.open()
        key = next((key  for key, val in self.handle.items() if val == search_val), None)
        logging.debug("SQL key look up with val |%s|: |%s|" % (search_val, key))
        self.close()
        return key
    
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
        if char.isspace() or not char.isalpha() and not char =="\x01":
            break
        else:
            word += char
    return word
    
def key_word(string):
    """returns lenght of the keyword at the begining of a str"""
    fw = first_word(string)
    first_word_sans_curser = fw.replace("\x01", "")
    for keyword in language_keywords:
        if first_word_sans_curser == keyword:
            return len(fw)
    return 0

class ToggleName():

    def __init__(self,data):
        
        self.data = data
        self.remainingdata = data
        
        
        self.component_list = []
        self.component_count = {} 
    
    def reasemble(self):
        rs = ""
        for component in self.component_list:
            data = component.present()
            rs += data
        return rs + self.remainingdata

    def goto_start(self):
        self.data = self.reasemble()
        self.remainingdata = self.data
        
    def toggle(self, s2c= True, cn= True ):
        """Togglename command
        s2c = string to code. The direction of toggle. Toggle/flip
        """
        
        cursor_found = False
        for token in self.component():
            if cn and token.has_cursor():
                cursor_found = True
            
            if (isinstance(token, string_name) and 
                s2c == True and
                cn == cursor_found):
                token = token.convert()
                
            elif (isinstance(token, code_name) and 
                s2c == False and
                cn == cursor_found):
                token = token.convert()
            
            elif (isinstance(token, bang_name)and
                cn == cursor_found):
                token = token.matchname(s2c)
            
            self.component_list.append(token)
            if cursor_found:
                break
        return 
            
        
    def fix_unknown(self):
        """works though data, looking for unfilled bangname, apon finding the first one, replacing unknown with cursor
        
        cursor should not be in data,
        does a look to be sure it is not there
        """
        self.remainingdata = self.data.replace("\x01","")
        
        for part in self.component():
            self.component_list.append(part)
            if isinstance(part, bang_name):
                if part.fix_unknown():
                    break
        else:
            self.remainingdata += "\x01"
                    
        return 

    def get_parsed_data(self):
        return self.component_list
    
    def component(self):
        """convert data into indiviual data types"""
                
        test_list = [self.q_not_Name, #looks for punkucations + whitespace + comments + quotes
                    self.q_bang_name, #handles floating !!'s
                    self.q_stringname,
                    self.q_codename,
                    ]


        while self.remainingdata:
            for i in test_list:
                objname = i()
                if objname:
                    self.count(objname)
                    yield objname
                    break
                    
        return
                
    def count(self, component):
        """increments the compnent types count by 1 in self.component_count"""
        self.component_count[component.__class__] = self.component_count.get(component.__class__, 0) + 1
        
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
        
        def white_space(string):
            """Returns length of whitespace type in the start of the string"""
            length = 0
            for character in string:
                if character.isspace():
                    length += 1
                else: break
            return length
            

            
        def punk(string):
            """returns the lenght of puncuation at the beggining of str"""
            length = 0
            for index, char in enumerate(string):
                if char.isalnum() or char in ("_", "\x01", "#", "'", '"', '"""') or char.isspace():
                    break
                
                if string[index:].startswith("!!"):
                    break
                
                length += 1
            return length
        
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
        
        def hash_comment(string):
            """Returns the lenght of the comment at the beggining of string"""
            if not string.startswith("#"):
                return 0
            nl_index = string.find("\n")
            if nl_index == -1:
                return len(string)
            else:
                return nl_index
             
            
        not_name_test_list = [hash_comment,
                              white_space,
                              key_word,
                              quote_string,
                              punk,
                              ]
        
        length = 0
        flag = True
        while flag:
            flag = False
            for test in not_name_test_list:
                l = test(self.remainingdata[length:])
                if l:
                    length += l
                    flag = True
                    break
        
        if length == 0:
            return None        
        
        not_Name_obj = not_name(self.remainingdata[:length])
        self.remainingdata = self.remainingdata[length:]
        return not_Name_obj
    
    
    
    
    def q_codename(self):
        """Returns codename componendt from the front of self.remaining data
        assumes that self.reaningdata does NOT start with a keyword"""     
        length = 0
        for char in self.remainingdata:
            if not char.isalnum() and char not in ("\x01", "_"):
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
            
        elif self.remainingdata[start_index:].startswith("!\x01!"):
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
    
    def q_unknown(self):
        """returns unknown object"""
        pass
    
    def q_stringname(self):
        
        name_string = ""
        #~ cursor = False
        if self.remainingdata[0].isdigit():
            return None
        for char in self.remainingdata:
            if char == "\x01":
                #~ name_string = "\x01" + name_string
                pass
                #~ continue
            
            elif char == " ":
                #if the next char is not alunum or is a keyword
                #it marks the end of string_word
                #except in the case where the curser is after a space
                name_len = len(name_string)
                next_is_keyword = key_word(self.remainingdata[name_len+1:])
                next_is_alnum = self.remainingdata[name_len+1].isalnum()
                next_is_cursor = self.remainingdata[name_len+1] == "\x01"
                
                if next_is_keyword or not next_is_alnum and not next_is_cursor:                
                        break
                #~ else:
                    #~ true_string_name = True
            
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
                

        
class component_Parent():
    def __init__(self, data, had_cursor = False):
        if had_cursor == True:
            self.had_cursor = True
        elif "\x01" in data:
            self.had_cursor = True
            data = data.replace("\x01","")
        else:
            self.had_cursor = False
        self.data = data
    def present(self):
        """Returns string form of data
        it cursor was in data, adds cursor to the of string"""
        if self.had_cursor:
            return self.data + "\x01"
        return self.data
        
    def has_cursor(self):
        return self.had_cursor
        
class string_name(component_Parent):
    def convert(self):
        """returns new code_name or bang_name
        looks up sql database for partering codename, if none,
        returns bang_name"""
        sql = sqlHandle()
        val = sql.val_lookup(self.data)
        
        if val == None:
            return bang_name(self.data+"!!unknown", had_cursor = self.had_cursor)
        else:
            return code_name(val, had_cursor = self.had_cursor)
        
    
class code_name(component_Parent):
    def convert(self):
        """returns new code_name or bang_name
        looks up sql database for partering codename, if none,
        returns bang_name"""
        # store data in dictionary hidden inside an SQLlite database
        if self.data == "\x01":
            return self
        
        sql = sqlHandle()
        string_n  = sql.key_lookup(self.data.replace("\x01", ""))
        if string_n == None:
            return bang_name("unknown!!" + self.data, had_cursor = self.had_cursor)
        else:
            return string_name(string_n, had_cursor = self.had_cursor)
    

class bang_name(component_Parent):
    def matchname(self, s2c):
        """Returns a string_name or code_name if bang_name has been
        filled out.
        Otherwise returns a copy of itself."""
        # store data in dictionary hidden inside an SQLlite database
        #What happends in the case of "  !!cod_name" ? should do testing
        str_name , cod_name = self.data.split("!!")
        
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
        return end_type(goal_name, had_cursor = self.had_cursor)

        
    
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
        
        returns True if bangname has unknown, and will edit data
        otherwise returns false
        """
        left, right = self.data.split("!!")
        if "unknown" not in (left, right):
            return False
        
        if right == "unknown":
            right = "\x01"
        elif left == "unknown":
            left = "\x01"
        
        if left == "":
            self.data = right    
        else:
            self.data = left + "!!" + right
        
        return True
class not_name(component_Parent):
    pass
    
    
