#!/usr/bin/python

import streamrec_data
import os
import time 
import sys, getopt

error_msg = 'Uso: show_strec_log.py -s <show> -t -d <dd/mm/yyyy> -p <process>'

config_data = streamrec_data.ConfigData()
log_file = config_data.streamrec_log_file()

grep_cmd = "cat " + log_file 

list_argv = sys.argv

try:
    opts, args_left = getopt.getopt(list_argv[1:],"hs:d:p:t")
except getopt.GetoptError: 
    print error_msg 
    sys.exit(2)

for opt,arg in opts:
    if opt=='-h':
        print error_msg 
        sys.exit()
    elif opt=='-s':
        show_tag = arg
        grep_cmd = grep_cmd + " | grep " + show_tag
    elif opt=='-d':
        log_date = arg
        grep_cmd = grep_cmd + " | grep " + log_date 
    elif opt=='-t':
        log_date = time.strftime("%d/%m/%Y")
        grep_cmd = grep_cmd + " | grep " + log_date 
    elif opt=='-p':
        rec_proc = arg
        grep_cmd =  grep_cmd + " | grep " + rec_proc

os.system(grep_cmd)

