#!/usr/bin/python

import streamrec_data
import sys

################################################
# Read input parameters 
################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
    print("ERROR: Uso -> " + list_argv[0] + " show_name")
    sys.exit()

show_tag = list_argv[1] 

################################################
# Print values 
################################################

str_line = '--------------------------------------------------------------'

radio_show = streamrec_data.RadioShow(show_tag)

print(str_line)
print(show_tag)
print(str_line)
print(radio_show)
print(str_line)

