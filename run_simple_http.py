#!/usr/bin/python

import subprocess, signal
import os
import sys

Base_dir = '/home/ec2-user/HttpRoot'
Process_log = '/home/ec2-user/log/simpleHTTP_log.txt'
Process_cmd = 'nohup /usr/bin/python -m SimpleHTTPServer 8080 2> ' + Process_log + ' &'
Process_name = 'SimpleHTTPServer'

def kill_process(p_name):

    p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    p_killed = False
    for line in out.splitlines():
        if p_name in line:
            pid = int(line.split()[1])
            os.kill(pid, signal.SIGKILL)
            p_killed = True
            print("Process " + str(pid) + " Killed")

    if not(p_killed):
        print("Process Not Running")

def start_process(p_name,p_cmd):

    os.system(p_cmd)
    print("Starting " + p_name + " ...")

def check_status(p_name):

    p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    p_running = False
    for line in out.splitlines():
        if p_name in line:
            pid = line.split()[1]
            p_running = True
            print(p_name + " is running with PID " + pid) 

    if not(p_running):
        print(p_name + "is NOT Running")

##################################################################################################
# Main
##################################################################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
    print("ERROR: Uso -> " + list_argv[0] + " start/stop/show")
    sys.exit()

option = list_argv[1]

if option=='start':
    os.chdir(Base_dir)
    start_process(Process_name,Process_cmd)
elif option=='stop':
    kill_process(Process_name) 
elif option=='status':
    check_status(Process_name)
elif option=='restart':
    kill_process(Process_name) 
    os.chdir(Base_dir)
    start_process(Process_name,Process_cmd)
else:
    print('WRONG OPTION')
