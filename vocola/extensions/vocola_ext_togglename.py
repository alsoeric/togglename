#!/bin/env python

# import rpdb2; rpdb2.start_embedded_debugger("123456")
# system imports:
import sys
import string
import re
import time
import sqlite3dbm
import logging
from optparse import OptionParser
import traceback
import os




clippy_filename = os.path.expanduser("~/tn_clippy.txt")

try:
    user_dir = os.environ['USERPROFILE']
except KeyError:
    user_dir = os.environ["HOME"]

log_path = os.path.abspath(os.path.join(user_dir,'Documents/toggle_name/'))
log_name = 'toggle_name.log'

if not os.path.exists(log_path):
    os.mkdir(log_path)
logging.basicConfig(filename=os.path.join(log_path,log_name),
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)
logging.debug('------------ start of run ------------------')

#This comment is to test github's commiting and pushing

# local imports:

from tn import *
# description:
#
# togglename.py
#
# site control variables
toggle_name_DB = os.path.join(user_dir,"/Documents/toggle_name/togglename.sqlite")

#Commandline processing
######### helper functions ##########
def commandline():
    """process commandline"""
        
    # get user data from command line
    component_list = [] # rubbish? :S

    usage = "I'm sorry Dave, I can't do that."
    parser = OptionParser(usage)
  
    parser.add_option("-m", type="string", dest='operational_mode',
        default = "st", 
        help="""Choose c[t|f|r] for clipboard, s[t|f|r] for stdin, t = test
        t - toggle
        f - fixunknown
        r - reverse toggle""" #This doesn't print right in the [-h]elp page...
                      )
    
    parser.add_option("-c", "--cursor", action = "store_true",
                      dest = "cn", default = False,
                      help = "Cursor needed. Use if you only want to effect where the cursor is"
                      )
        
    (options, parse_args) = parser.parse_args()

    return options.operational_mode , options.cn 


class winclip:
# clipboard access class.  handles psudo clipboard if testing
    try: 
        import win32clipboard
        import win32con

        def clipboard_wait_open(self):
            while(True):
                try:    
                    self.win32clipboard.OpenClipboard()
                    return
                except Exception, error:
                    logging.debug( "CWO %s"%(repr(error)))
                    time.sleep(0.1)

        def clipboard_get(self):
            self.clipboard_wait_open()   
            result = ""
            if self.win32clipboard.IsClipboardFormatAvailable(self.win32con.CF_TEXT):
                result=self.win32clipboard.GetClipboardData(self.win32con.CF_TEXT)

            self.win32clipboard.CloseClipboard()
            #find cursor possition 
            null = string.find(result, chr(0))
            if null > 0:
                result = result[0:null]
            #~ else:
                #~ logging.error("null not found in clipboard get")
            return result

        def clipboard_set(self,aString):
            self.clipboard_wait_open()
            self.win32clipboard.EmptyClipboard()
            self.win32clipboard.SetClipboardData(self.win32con.CF_TEXT,aString)
            self.win32clipboard.CloseClipboard()
            return

    except ImportError:
        logging.debug("clipboard import error")
        fake_clip = None

        def clipboard_wait_open(self):
            return True

        def clipboard_get(self):
            return self.fake_clip

        def clipboard_set(self, aString):
            self.fake_clip=aString
            return True

class fileclip:
    def __init__(self):
        self.fh = None
        
    # clipboard access class using file as clipboard
    def clipboard_wait_open(self,rw="r"):
        # file does not need to wait.  maybe if we used locking
        self.fh = open(clippy_filename,rw)
        
    def clipboard_get(self):
        self.clipboard_wait_open("r")   
        result = self.fh.read()
        self.fh.close()
        return result

    def clipboard_set(self,aString):
        self.clipboard_wait_open("w")
        self.fh.seek(0)
        self.fh.truncate()
        self.fh.write(aString)
        self.fh.close()
        return


class vocola_interface:
    def __init__(self):
        self.ID = "VI"
        self.clipboard_instance = None
        self.clipboard_string = ""
        self.stdin_string = ""
        self.result = ""
        self.tn = None
    
    def read_clipboard( self):
        try:
            self.clipboard_instance = fileclip()  
            self.clipboard_string = self.clipboard_instance.clipboard_get()    
            logging.debug( "%s clip result = |%s|" % (self.ID, self.clipboard_string))
            self.tn = ToggleName(self.clipboard_string)
        except Exception, error:
            logging.debug( "CLIP: %s %s" %(self.ID, repr(error)))
            traceback_string = traceback.format_exc()
            logging.debug( "%s TB %s" % (self.ID, traceback_string))
        
    def write_clipboard (self):
        self._reasemble()
        self.clipboard_instance.clipboard_set(self.result)

    def read_stdin(self):
        try:
            self.stdin_string = sys.stdin.read()
            logging.debug( "%s stdin result = |%s|" % (self.ID, self.stdin_string))
            self.tn = ToggleName(self.stdin_string)
        except Exception, error:
            logging.debug( "STDIN:%s %s" %(self.ID, repr(error)))
            traceback_string = traceback.format_exc()
            logging.debug( "%s TB %s" % (self.ID, traceback_string))
            
    def write_stdout(self):
        self._reasemble()
        sys.stdout.write(self.result)

    def _reasemble(self):
        # reassemble and log
        self.result = self.tn.reasemble()
        logging.debug("%s result = |%s|" % (self.ID, self.result))

    def action(self, gs2c=1, gcn=0): 

        """ this is an empty method in the abstract
        class only copying input from the clipboard to the result
        output variable."""

        self.result = self.clipboard_string 
    


class vocola_toggle_name(vocola_interface):
    def __init__(self):
        vocola_interface.__init__(self)
        self.ID = "VTN"
        
    def action(self, gs2c=1, gcn=0):
        self.tn.toggle(s2c=int(gs2c),cn=int(gcn))


class vocola_fix_unknown(vocola_interface):
    def __init__(self):
        vocola_interface.__init__(self)
        self.ID = "VFXU"
        
    def action(self, gs2c=1, gcn=0):
        self.tn.toggle(s2c=1,cn=0)
        self.tn.fix_unknown()

# may be redundant
class vocola_toggle_fix(vocola_interface):
    def __init__(self):
        vocola_interface.__init__(self)
        self.ID = "VTF"
        
    def action(self, gs2c=1, gcn=0):
        self.tn.toggle(s2c=int(gs2c),cn=int(gcn))
        self.tn.fix_unknown()

class vocola_first_unknown(vocola_interface):
    def __init__(self):
        vocola_interface.__init__(self)
        self.ID = "V1stU"
        
    def action(self):
        self.tn.fix_unknown()

# vocola interfaces
# Vocola function: toggle.name, 2-
def vc_toggle_name(gs2c=1, gcn=0):
    interface = vocola_toggle_name()
    interface.read_clipboard()
    interface.action(gs2c, gcn)

    # place back in the clipboard
    interface.write_clipboard()
    return ""

# Vocola function: toggle.fix_unknown 
def vc_fix_unknown():
    interface = vocola_fix_unknown()
    interface.read_clipboard()
    interface.action()

    # place back in the clipboard
    interface.write_clipboard()
    return ""

# Vocola function: toggle.firstunknown
def vc_first_unknown():
    interface = vocola_first_unknown()
    interface.read_clipboard()
    interface.action()

    # place back in the clipboard
    interface.write_clipboard()
    return ""


# STDIN functions: 
def stdin_toggle_name(gs2c=1, gcn=0):
    interface = vocola_toggle_name()
    interface.read_stdin()
    interface.action(gs2c, gcn)

    # write to stdout
    interface.write_stdout()
    return ""
 
def stdin_fix_unknown():
    interface = vocola_fix_unknown()
    interface.read_stdin()
    interface.action()

    # write to stdout
    interface.write_stdout()
    return ""

def stdin_first_unknown():
    interface = vocola_first_unknown()
    interface.read_stdin()
    interface.action()

    # write to stdout
    interface.write_stdout()
    return ""
    
### Old tests need to be updated to include toggle_tests.py
def tests():
    
    #Unit test is kind of weird. Put test data into the clipboard then
    #run the program and look at the results in the clipboard. Yeah,
    #kind of weird.
    test_set = {        
        "not very simple \x01counter = 1234+ simple string": "smplCntr = 1234+ simple string",
        "not very sim\x01ple counter = 1234+ simple string": "smplCntr = 1234+ simple string",
        "\x01simple counter = 1234+ simple string": "smplCntr = 1234+ simple string",
        "simple counter = 1234+ sim\x01ple string": "simple counter = 1234+ smplStr",
        "simple counter = 1234+ simple\x01 string": "simple counter = 1234+ smplStr",
        "simple counter = 1234+ simple string\x01": "simple counter = 1234+ smplStr",
        }

    seed_set = {        
        "not very simple counter": "NsmplCntr",
        "simple string": "smplStr",
        "simple counter": "simpCnt",
        }
    seed_fill = {        
        "not very simple counter!!unknown": "NsmplCntr",
        "simple string!!unknown": "smplStr",
        "simple counter!!unknown": "simpCnt",
        }
    tni = tn()
    
    if False:
        logging.debug("single item test")
        (j,k) = test_set.items()[4]
        tni.test_case(j,k)
    else:
        logging.debug("multi item test")
        for j,k in test_set.items():
            tni.test_case(j,k)

if '__main__'==__name__ :
   
    mode, cn = commandline()
    if mode == "t":
        tests()
    elif mode == "ct": 
        vc_toggle_name(True, cn)

    elif mode == "cr":
        vc_toggle_name(False, cn)

    elif mode == "cf": 
        vc_fix_unknown()

    elif mode == "st":
        stdin_toggle_name(True, cn)
 
    elif mode == "sr": 
        stdin_toggle_name(False, tn)     
         
    elif mode == "sf": 
        stdin_fix_unknown()

    else:
        raise hell #Wrong argumetns were added. Nothing will happen, better do something?
