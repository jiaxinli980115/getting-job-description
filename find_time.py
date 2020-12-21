#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:13:08 2020

@author: jiaxinli
"""

import re

def readlines(filepath):
	    fd = open(filepath, 'r')
	    lines = []
	    for line in fd:
	        ### Uncomment if needed to fileter things other that alphanum and $%
	        # line = re.sub(r"[^a-zA-Z0-9\%\$]+", ' ', line)
	        line = line.lower().strip()
	        lines.append(line)
	    fd.close()
	    return lines
 
# Description:
	 #  This function is used to find any dates within list of line
	 # 
	 # Input:
	 #  A list (array) of lines (text)
	 # Output:
	 #  A list of dates found from list of lines
    
def find_time(lines):
    potential_data_list = []
    for line in lines:
        potential_data_list += re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',line)   #for format 23-10-2002 23/10/2002 23/10/02 10/23/2002
        potential_data_list += re.findall(r'(?:\d{1,2} )?(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* (?:\d{1,2},)?\d{2,4}',line)   #for format 23 Oct 2002\n23 October 2002\nOct 23,2002\nOctober 23,2002\n
    return potential_data_list




    


lines = readlines('sample_cv.txt')
result = find_time(lines)

