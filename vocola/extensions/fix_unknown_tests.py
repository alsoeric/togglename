#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fix_unknown_tests.py
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

cursor = "\x01" 

tests = [ ("", cursor),
		  (cursor, cursor),
		  ("class !!unknown():", "class "+cursor+"():"),
		  ("foo bar!!unknown", "foo bar!!"+cursor),
		  ("unknown!!foo", cursor + "!!foo"),
		  ("unkno"+cursor+"wn!!foo",cursor + "!!foo"),  
		]
for test, result in tests:
	
    tn = ToggleName(test)
    tn.fix_unknown()
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
