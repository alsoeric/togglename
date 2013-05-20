#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  toggle_tests.py
#  
#  Copyright 2013 Tonis <Tonis@PLUTO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from tn import *
import pickle

test_set = [
                ("",1, 0 , ""),
                ("",0, 0 , ""),

                ("apple pie",1,0, "aplpie"),   
                ("apple pie",0,0, "apple pie"),
                ("apple pie",1,1, "apple pie"),
                ("apple pie",0,1, "apple pie"),
                
                ("aplpie", 0, 0,  "apple pie"),
                ("aplpie", 0, 1,  "aplpie"),
                ("aplpie", 1, 0,  "aplpie"),
                ("apl\x01pie",0 , 0,  "aplpie"),
                ("\x01aplpie",0 , 1,  "apple pie"),
                ("apl\x01pie",0 , 1,  "apple pie"),
                ("aplpie\x01",0 , 1,  "apple pie"),
                
                ("apple\x01 pie",1 , 1,  "aplpie"),
                ("apple \x01pie",1 , 1,  "aplpie"),
                ("apple pie",1 , 1,  "apple pie"),

                ("bang bang",1 , 0,  "bang bang!!unknown"),  
                
                
                
                
                ("if apple pie:", 1, 0, "if aplpie:"),
                ("if apple pie: print(aplpie)", 1, 0, "if aplpie: print(aplpie)"),
                ("if app\x01le pie: print(apple pie)", 1 ,1, "if aplpie: print(apple pie)"),
                
                ("if 'apple pie', print(apple pie)", 1, 0, "if 'apple pie', print(aplpie)"),
                
                ("defnot go", 1 ,0, "defnot_go"),

                ("def very simple \x01counter (simple string):",1,1, "def VsmplCntr (simple string):"),
                ("not very simple \x01counter = 1234+ simple string",1,1, "not VsmplCntr = 1234+ simple string"),
                ("not very sim\x01ple counter = 1234+ simple string",1,1, "not VsmplCntr = 1234+ simple string"),
                ("\x01simple counter = 1234+ simple string",1, 1, "smplCntr = 1234+ simple string"),
                ("simple counter = 1234+ sim\x01ple string",1, 1, "simple counter = 1234+ smplStr"),
                ("simple counter = 1234+ simple\x01 string",1, 1, "simple counter = 1234+ smplStr"),
                ("simple counter = 1234+ simple string\x01",1, 1, "simple counter = 1234+ smplStr"),
                ("i\x01f apple pie.is_delicious(): print(indeed so , \"yes yes\") #no it's not",1, 0, "if aplpie.is_delicious(): print(indeed so!!unknown , \"yes yes\") #no it's not"),
                #~ "if cursor is +  \x01   middle of whitespace":None,
                #~ "if cursor is +\x01= middle of namelimit":None,
                #~ "string word!!unknown == unknown!!codeName":None,
                #~ "the cursor is at end of line \x01":None,
                ("simple string \"in qu'otes\" apple pie '' ",1,0, "smplStr \"in qu'otes\" aplpie '' "),
                ("1234 simple string 1234",1,0, "1234 smplStr 1234"),
                #~ "40 foo += fourty 40":None,
                
                ("unknown!!codename(apple pie)", 1, 0, "codename(aplpie)"),
                ("unknown!!codename(apple pie)", 0, 0, "unknown!!codename(apple pie)"),
                ("string name!!unknown(aplpie)", 0, 0, "string name(apple pie)"),
                ("string name!!\x01unknown(apple pie)", 1, 1,  "string name!!unknown(apple pie)"),
                ("unknown!\x01!codename(apple pie)", 1, 1,  "codename(apple pie)"),
                
                ("apple pie \x01lambda",1 , 0,  "aplpie lambda"), # When the cursor is after a space that is at the end of a stringname, it might capture a following codename
                ("apple pie \x01code_name",1 , 0,  "aplpie code_name"),  
                
                #args Found a bug?
                ("function(apple pie,)", 1, 0, "function(aplpie,)"),
                ("function(apple pie,apple pie,apple pie)", 1, 0, "function(aplpie,aplpie,aplpie)"),
                ("function( apple pie ,)", 1, 0, "function( aplpie ,)"),
                
                # "!!unknown or !unknown!
                ("class !!unknown ()", 1,0, ""),
                ("""def Recursive add (digit):
    Great big some = great big some plus digit
    if great big some < 100:
        Recursive add (great big some)

    return great big some
""",1,0,""),
                ]
                
                

                
                
str_cods = {"apple pie" : "aplpie",
            "defnot go" : "defnot_go",
            "very simple counter": "VsmplCntr",
            "simple counter" : "smplCntr",
            "simple string" : "smplStr",
            } 







f = {
}    
    


sql = sqlHandle()
for sn, cn in str_cods.items():
    sql.set_match(sn, cn)
del(sql)
    
for test, s2c, cn, result in test_set:
    #~ print("Test: %s"%(test,))
    tn = ToggleName(test)
    ol = tn.toggle(s2c, cn)
    tr = tn.reasemble()
    if tr == result:
        print("Test passed: " + test)
    else:
        print("Test failed: Beginning data dump")
        print("Test:", test)
        print("Correct result: |%s|"%result)
        print("Actual result: |%s|"%tr)
        print("----")
        for i in tn.get_parsed_data():
            print("|%s|"%i.data)
            print(i.__class__.__name__)
            print("----")
        print("")


