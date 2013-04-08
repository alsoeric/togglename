#!/bin/env python

# system imports:
import sys
import string
import re
import time
import sqlite3dbm
import logging
from optparse import OptionParser
import traceback

logging.basicConfig(filename='C:/Users/esj/Documents/toggle_name/toggle_name.log',
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
toggle_name_DB = "C:/Users/esj/Documents/toggle_name/togglename.sqlite"

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
        help="choose c[t|m] for clipboard, s[t|m] for stdin, t = test"
                      )
    
    (options, parse_args) = parser.parse_args()

    return (options.operational_mode)    


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
            null = string.find(result, chr(0))
            if null >0:
                result = result[0:null]
            return result

        def clipboard_set(self,aString):
            self.clipboard_wait_open()
            self.win32clipboard.EmptyClipboard()
            self.win32clipboard.SetClipboardData(self.win32con.CF_TEXT,aString)
            self.win32clipboard.CloseClipboard()
            return

    except ImportError:
        fake_clip = None

        def clipboard_wait_open(self):
            return True

        def clipboard_get(self):
            return self.fake_clip

        def clipboard_set(self, aString):
            self.fake_clip=aString
            return True

# vocola interfaces
# Vocola function: toggle.name
def vc_toggle_name():
    logging.debug("VTN start 0")
    try:
        clipboard_instance = winclip()  
        clipboard_string = clipboard_instance.clipboard_get()    
        #logging.debug( "clip result = |%s|" % result
        if clipboard_string:
            logging.debug("VTN start 1 %s" % clipboard_string)
            tn = ToggleName(clipboard_string,s2c=True,cn=True)
            tn.toggle()
            result = tn.reasemble()
            
            # place back in the clipboard
            clipboard_instance.clipboard_set(result)
            logging.debug( "result = |%s|" % result)
            # logging.Debux("VTN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "VTN %s" %(repr(error)))
        traceback_string = traceback.format_exc()
        logging.debug( "VTN TB %s" % traceback_string)

    return ""

# Vocola function: match.name
def vc_match_name():
    logging.debug("VMN start")
    try:
        tni = tn()
        result = tni.clip_instance.clipboard_get()
        logging.debug( "clip result = |%s|" % result)
        if result:
            (left_code, code_name, right_code) = tni.match_name(result)
            tni.clip_instance.clipboard_set(left_code+code_name+right_code)
    except Exception, error:
        logging.debug( "VMN %s" %(repr(error)))
        traceback_string = traceback.format_exc()
        logging.debug( "VMN TB %s" % traceback_string)

    return ""


def stdio_toggle_name():
    logging.debug("STN start 0")
    try:
        tni = tn()
        logging.debug("STN start 1")
        string = sys.stdin.read()
        (left_code, code_name, right_code) = tni.toggle_name(string)
        # place back in the clipboard
        #logging.debug( "result = |%s|" % plain_name
        sys.stdio.write( left_code+code_name+right_code)
        logging.debug("STN start 2 %s" %repr(ignore_data))
    except Exception, error:
        logging.debug( "STN %s" %(repr(error)))

    return ""

#
def stdio_match_name():
    logging.debug("SMN start")
    try:
        logging.debug( "SMN stdio result = |%s|" % result)
        tni = tn()
        string = sys.stdin.read()
        ignore_data = tni.match_name(string)
        sys.stdio.write(left_code + code_name + right_code)
    except Exception, error:
        logging.debug( "SMN %s" %(repr(error)))

    return ""

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
   
    mode = commandline()
    if mode == "t":
        tests()
    elif mode == "ct": 
        vc_toggle_name()

    elif mode == "cm": 
        vc_match_name()

    elif mode == "st": 
        stdio_toggle_name()
        
    elif mode == "sm": 
        stdio_match_name()    
