#!/usr/bin/python

import json
import sys
import os

gen_config_file = '/home/ec2-user/config/gen_config.json'

line_str = '--------------------------------------------------------------'

################################################
# Read input parameters
################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
    print("ERROR: Uso -> " + list_argv[0] + " show_name")
    sys.exit()

show_name = list_argv[1] 

################################################
# Read General Parameters from file
################################################

f_conf = open(gen_config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

config_file = input_data['streamrec_config_file'] 

################################################
# Read Parameters from file
################################################

f_conf = open(config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

first_item = input_data[0]
new_item = {}

for par_name in first_item:
    new_item[par_name] = ""

new_item['show_name'] = show_name

input_data.append(new_item)

################################################
# Write file
################################################

f_out = open(config_file,'w')
f_out.write(json.dumps(input_data,indent=4))
f_out.close()
