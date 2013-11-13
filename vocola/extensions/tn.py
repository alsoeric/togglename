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
    """
    mysqlite3dbm handeler.
    Used to store stringname-codename pairs.
    each pair is stored sn:cn & cn:sn to allow for faster reverse search
    """
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
    
    def set_match(self, key, val):
        """Sets self.handle[key] to val. & self.handle[val] to key
        """
        self.open()
        self.handle[key] = val
        self.handle[val] = key
        return 

    def clear_data(self):
        "Clears the DB. Use at own risk"
        self.open()
        self.handle.clear()
        self.close()

class ToggleName():
    """Toggle Box parser and toggler
    """
    def __init__(self, source_string):
        self.source_string = source_string
        self.remaining_source = source_string
        self.cursor_index = source_string.find(CURSOR_MARKER)
        if self.cursor_index == -1:
            self.cursor_index = False
        else:
            self.remaining_source = source_string.replace(CURSOR_MARKER, "")
        self.parsed_tokens = []
        #The list of tokens that are used to tokenize source_string
        self.token_list = [LanguageKeyWord,
                           StringName,
                           CodeName,
                           BangName,
                           CommentNotName,
                           QuoteNotName,
                           NotName,]
        #Stack of nesting
        self.nesting_stack = [self.parsed_tokens]
        
    def reasemble(self):
        sl = []
        for token in self.parsed_tokens:
            sl.append(token.present())
        return "".join( sl )

    def goto_start(self):
        ToggleBox.__init__(self, self.reasemble())
        
    def add_token(self, token):
        """Adds a token to the list of parsed tokens. 
            If the token types alow a merge, such as the case with notnames, and stringname!!bangnames,
            will merge the two tokens rather then adding,
        """
        if self.get_previous_token().is_compatable(token): 
            self.get_previous_token().merge(token)
        else:
            self.parsed_tokens.append(token)
    
    def get_previous_token(self):
        """ returns the previously parsed token, or dummy token if there have been no tokens parsed yet"""
        try:
            return self.parsed_tokens[-1]
        except IndexError:
            return Token("") #dummy token

    def parse_tokens(self, cn = False):
        """ Returns a list of tokens 
        parses out tokens from source_string using self.token_list
        if token is a nesting token, append to nesting stack
        appends parsed tokens to self.parsed_tokens
        yeilds token
        """
        cursor_found = False
        while self.remaining_source:
            for t in self.token_list:
                #Ask the token if the source_string starts with it's token
                parsed_token = t.parse_token(self.remaining_source)
                if parsed_token is not None:
                    if self.cursor_index is not False:
                        self.cursor_index -= len(parsed_token)
                        if self.cursor_index <= 0:
                            parsed_token.has_cursor = True
                            self.cursor_index = False
                    #commented out, uncomment when 
                    #if self.token_is_nesting_closure(parsed_token):
                    #    self.reduse_nesting()
                    #if isinstance(parsed_token, NestingToken):
                    #    self.nest_token
                    #else:
                    self.add_token(parsed_token)
                    self.remaining_source = self.remaining_source[len(parsed_token):]
                    break
            if cn and cursor_found:
                break

        return self.parsed_tokens
        
    def fix_unknown(self,):
        self.goto_start()
        self.cursor_index = False
        for token in self.parse_tokens():
            if isinstance(token, BangName):
                token.place_cursor()
                break
        
    def toggle(self, s2c = True, cn = True):
        """Togglename Command.
        s2c: string2code: bool: spesifies direction of toggleing
        cn: cursor needed: Will only toggle name containing the cursor
        Stringname that do not have a pair will be replaced with a bangname
        """
        parsed_tokens = self.parse_tokens()
        for token in parsed_tokens:
            if cn:
                if token.has_cursor and isinstance(token, (StringName, CodeName)):
                    token.toggle()
                    break
                elif token.has_cursor and isinstance(token, BangName):
                    token.match_name(s2c)
                    token.has_cursor = True
            elif (isinstance(token, StringName) and 
                 s2c == True ):
                token.toggle()
                
            elif (isinstance(token, CodeName) and 
                 s2c == False):
                token.toggle()
            
            elif (isinstance(token, BangName)):
                token.match_name(s2c)
                
        return 


class Token(object):
    """Abstract class of a token."""
    #re
    re = "" 
    mergable_token_types = ()
    def __init__(self, string, has_cursor = False):
        self.string = string
        self.has_cursor = has_cursor
        pass
        
    def __len__(self,):
        return len(self.string)

    @classmethod
    def parse_string(cls, string2parse):
        """Parses a string and returns the portion at the begining that is a valid type of the token. If none, will return empty string."""
        if type(string2parse) != str:
            raise TypeError("|%s| is not string, can not be parsed"%string2parse)
        try:
            s = re.match(cls.re, string2parse).group()
        except AttributeError:
            s = ""
        return s
        
    @classmethod
    def parse_token(cls, string2parse):
        token_data = cls.parse_string(string2parse)
        if token_data:
            return cls(token_data)
        else:
            return None

    def is_compatable(self, token):
        """Returns True if Token is an instance of any tokens in self.mergable_token_types"""
        return isinstance(token, self.mergable_token_types)

    def merge(self, token):
        """Abstract method
        Merge two tokens into one"""
        raise NotImplementedError()
        


    def present(self):
        if self.has_cursor:
            return self.string + CURSOR_MARKER
        return self.string

    
class NullToken(Token):
    """Token that presents itself with an empty string"""
    pass

class PassToken(Token):
    """Token that does not act on any conversion commands"""
    pass
    
class LanguageKeyWord(Token):
    """reperests language keywords such as if and or as while for"""
    re = re.compile("("+ "|".join(language_keywords) + ")(?=(?!\w))", re.I)
    keyword_dict = {keyword.lower() : keyword for keyword in language_keywords}
    def present(self):
        self.string = LanguageKeyWord.keyword_dict[self.string.lower()]
        return Token.present(self,)

class BangName(Token):
    re = "!!\w*"
    
    def match_name(self, s2c):
        """looks up the tokens in the sqldb
        s2c bool: True if converting string to code,"""
        sn , cn = self.string.split("!!")
        if "" in (sn, cn): #What's to match? NOTHING!
            return
        sql = sqlHandle()
        if s2c and cn != "unknown":
            if sn == "unknown":
                self.__class__ = CodeName
                self.__init__(cn, self.has_cursor)
            else:
                sql.set_match(sn, cn)
                self.__class__ = CodeName
                self.__init__(cn, self.has_cursor)
        elif not s2c and sn != "unknown":
            if cn == "unknown":
                self.__class__ = StringName
                self.__init__(sn, self.has_cursor)
            else:
                sql.set_match(sn, cn)
                self.__class__ = StringName
                self.__init__(sn, self.has_cursor)
            
    def place_cursor(self,):
        self.has_cursor = True
    
    def present(self,):
        if self.has_cursor:
            return self.string.replace("unknown", CURSOR_MARKER)
        else: return self.string


class StringName(Token):
    """Stringname Token
    Examples: a long river, sick cat, result value, 4 ints, FooBoo Gar dON
    illegal exambles: return value (keyword), apples (single word), too_long (underscore)

    Methods:
     convert:
      looks up string in local sql db for codename pair. If found, converts to codename. If not found, bangname
    """
    mergable_token_types = (BangName)
    
    def merge(self, token):
        self.__class__ = BangName
        self.__init__(self.string + token.string, self.has_cursor or token.has_cursor)
    
    @classmethod
    def parse_string(cls, string2parse):
        """Returns "" or a string that is a valid stringname at the beginning of string2parse"""
        name_string = []
        if not string2parse[0].isalnum(): 
            return ""
        for char in string2parse:
            if char == " ":
                #if the next char is not alunum or is a keyword
                #it marks the end of string_word
                #except in the case where the curser is after a space
                name_len = len(name_string)
                remainder = string2parse[name_len+1:]
                next_is_keyword = LanguageKeyWord.parse_string(remainder) #will capture language keyword or ""
                try:
                    next_is_alnum = remainder[0].isalnum()
                except IndexError:
                    return ""
                
                if next_is_keyword or not next_is_alnum:
                        break
            elif not char.isalnum():
                print "|%s| is not valid part of SN"%char
                if char == "_":
                    #Bumped into a code_word, remove chars untill " " is hit
                    name_string = "".join(name_string).rsplit(" ", 1)[0]
                break

            name_string.append(char)
        name_string = "".join(name_string)
        name_string = name_string.rstrip(" ")
        if name_string == "" or " " not in name_string:
            return ""
        return name_string.lower()

    def toggle(self,):
        sql = sqlHandle()
        cn = sql.val_lookup(self.string)
        if cn is None:
            self.merge(BangName("!!unknown"))
        else:
            self.__object__ = CodeName
            self.__init__(cn, self.has_cursor)

class CodeName(Token):
    re = "\w+"
    
    mergable_token_types = (BangName)
    
    def merge(self, token):
        self.__class__ = BangName
        self.__init__(self.string + token.string, self.has_cursor or token.has_cursor)
        
    def toggle(self,):
        sql = sqlHandle()
        sn = sql.val_lookup(self.string)
        if sn is None:
            self.merge(BangName("unknown!!"))
        else:
            self.__object__ = CodeName
            self.__init__(sn, self.has_cursor)
            
class NotName(Token):
    """Token that reperesents any chars that do not fit into any other tokens"""
    re = "[^\w]"
    
    def __init__(self, string, has_cursor = False):
        Token.__init__(self, string, has_cursor)
        self.string = list(string)
    
    def is_compatable(self, token):
        return isinstance(token, NotName)
    
    def merge(self, token):
        self.string += token.string
        self.has_cursor = self.has_cursor or token.has_cursor
    def present(self):
        self.string = "".join(self.string)
        return Token.present(self)

class CommentNotName(NotName):
    """Token for parsing out comments"""
    re = "#.*"

class QuoteNotName(NotName):
    """Token for parsing out comments"""
    re = '("""(.|\n)*""")|".*"|' + "'.*'"
