#!/usr/bin/python

import sys
import os
import dropbox

dbx_path = '/Podcasts/'

dbx_auth_token = ''

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 3):
	print("ERROR: Uso -> " + list_argv[0] + " file_name dir")
	sys.exit()

file_name = list_argv[1]
pod_dir = list_argv[2]

base_name = os.path.basename(file_name)

################################################
# Upload to Dropbox
################################################

dbx = dropbox.Dropbox(dbx_auth_token)

dbx_file = dbx_path + pod_dir + '/' + base_name

print(file_name + ' -> ' + dbx_file)

with open(file_name,'rb') as f:
    data = f.read()
    dbx.files_upload(data,dbx_file)

