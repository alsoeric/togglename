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

user_dir = os.environ['USERPROFILE']
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
    component_list = []

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

# vocola interfaces
# Vocola function: toggle.name, 2-
def vc_toggle_names(gs2c=1, gcn=0):
    
    logging.debug("VTN start 0 %s, %s"%(int(gs2c),int(gcn)))
    try:
        clipboard_instance = winclip()  
        clipboard_string = clipboard_instance.clipboard_get()    
        logging.debug( "result from clip = |%s|" % clipboard_string)
        
        if clipboard_string:
            logging.debug("Starting ToggleBox: s2c = %s, cn = %s"%(gs2c, gcn))
            tn = ToggleName(clipboard_string)
            tn.toggle(s2c=int(gs2c),cn=int(gcn))
            result = tn.reasemble()
            logging.debug("parsed component counts: nn=%s, bn=%s, sn=%s, cn=%s"%(tn.get_count())) 
            
            # place back in the clipboard
            clipboard_instance.clipboard_set(result)
            logging.debug( "toggle result = |%s|" % result)
            # logging.Debux("VTN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "VTN %s" %(repr(error)))
        traceback_string = traceback.format_exc()
        logging.debug( "VTN TB %s" % traceback_string)

    return ""

# Vocola function: toggle.unknown
def vc_fix_unknown():
    logging.debug("VFU start 0")
    try:
        clipboard_instance = winclip()  
        clipboard_string = clipboard_instance.clipboard_get()    
        #~ logging.debug( "clip result = |%s|" % clipboard_string)
        
        if clipboard_string:
            logging.debug("VFU start 1 |%s|" % clipboard_string)
            tn = ToggleName(clipboard_string)
            tn.toggle(s2c=1,cn=0)
            #tn.goto_start() #Not needed, fix_unknown() does a test if nessasarry.
            tn.fix_unknown()
            result = tn.reasemble()
            logging.debug( "VFU result = |%s|" % result)
            
            # place back in the clipboard
            clipboard_instance.clipboard_set(result)
            # logging.Debux("VTN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "VFU %s" %(repr(error)))
        traceback_string = traceback.format_exc()
        logging.debug( "VFU TB %s" % traceback_string)

    return ""

# Vocola function: toggle.firstunknown
def vc_first_unknown():
    logging.debug("VFU start 0")
    try:
        clipboard_instance = winclip()  
        clipboard_string = clipboard_instance.clipboard_get()    
        #~ logging.debug( "clip result = |%s|" % clipboard_string)
        
        if clipboard_string:
            logging.debug("VFU start 1 |%s|" % clipboard_string)
            tn = ToggleName(clipboard_string)
            tn.fix_unknown()
            result = tn.reasemble()
            
            # place back in the clipboard
            clipboard_instance.clipboard_set(result)
            logging.debug( "result = |%s|" % result)
            # logging.Debux("VTN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "VFU %s" %(repr(error)))
        traceback_string = traceback.format_exc()
        logging.debug( "VFU TB %s" % traceback_string)

    return ""

### Old tests need to be updated to inlude toggle_tests.py
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
        vc_toggle_names(True, cn)

    elif mode == "cr":
        vc_toggle_names(False, cn)

    elif mode == "cf": 
        vc_fix_unknown()

    elif mode == "st": 
        stdio_toggle_name() # no such things    
        
    elif mode == "sm": 
        stdio_match_name()    
