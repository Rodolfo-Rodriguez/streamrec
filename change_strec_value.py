#!/usr/bin/python

import json
import sys
import os

config_file = '/home/ec2-user/config/streamrec_config_2.json'

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 4):
    print("ERROR: Uso -> " + list_argv[0] + " show_name par_name par_val")
    sys.exit()

show_name = list_argv[1]
par_name = list_argv[2]
par_val = list_argv[3]

if par_name=='show_name':
    print("No se puede cambiar " + par_name)
    sys.exit()

################################################
# Read Parameters from file
################################################

f_conf = open(config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

for item in input_data:
    if item['show_name'] == show_name:
        if (par_name in item):
            item[par_name] = par_val 
        else:
            print("El Paramtero " + par_name + " no existe")
            sys.exit()

f_out = open(config_file,'w')
f_out.write(json.dumps(input_data,indent=4))
f_out.close()

os.system("/home/ec2-user/bin/show_strec_config.py " + show_name)
