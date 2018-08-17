#!/usr/bin/python

import dropbox
import datetime
import json
import sys

gen_config_file = '/home/ec2-user/config/gen_config.json'

################################################
# Read General Parameters from file
################################################

f_conf = open(gen_config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

config_file = input_data['streamrec_config_file'] 

access_token = input_data['dropbox_access_token'] 
dbx_path = input_data['dropbox_path'] 

pls_path = input_data['pls_path'] 

################################################
# Read Input Parameters 
################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
    print("ERROR: Uso -> " + list_argv[0] + " show_name")
    sys.exit()

show_name = list_argv[1]
pls_file_name = show_name + ".m3u" 

################################################
# Read Parameters from file
################################################

f_conf = open(config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

show_present = False
for item in input_data:
    if (show_name == item['show_name']):
        record_dir = item['record_dir']
        podcast_name = item['podcast_name']
        show_present = True

if not(show_present):
    sys.exit()

dbx_root = dbx_path + '/' + record_dir
pls_full_file = pls_path + '/' + record_dir + '/' + pls_file_name 


###########################################################################
# Get files list from Dropbox 
###########################################################################

dbx = dropbox.Dropbox(access_token)

pod_files_md = []
for entry in dbx.files_list_folder(dbx_root).entries:
    pod_files_md.append(entry)


###########################################################################
# Get shared links list 
###########################################################################

pod_links = []
for pod_f_md in pod_files_md:
    link_metadata = dbx.sharing_create_shared_link(pod_f_md.path_display)
    s_link = link_metadata.url.replace('dl=0','dl=1')
    pod_links.append(s_link)

###########################################################################
# Create RSS Feed 
###########################################################################

pls_fh = open(pls_full_file,'w')

pod_id = 0
for pod_f_md in pod_files_md:

    pod_link = pod_links[pod_id]
    pls_fh.write(pod_link + "\n")
    pod_id = pod_id + 1

pls_fh.close
