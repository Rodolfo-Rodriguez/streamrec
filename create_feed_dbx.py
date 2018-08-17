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

rss_path = input_data['rss_feeds_path'] 
rss_file_name = input_data['rss_file_name']
image_file = input_data['rss_image_file']

rss_base_url = input_data['rss_base_url']

################################################
# Read Input Parameters 
################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
    print("ERROR: Uso -> " + list_argv[0] + " show_name")
    sys.exit()

show_name = list_argv[1]

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
        stream_codec = item['stream_codec']
        podcast_name = item['podcast_name']
        podcast_desc = item['podcast_desc']
        show_url = item['show_url']
        station_name = item['station_name']
        show_present = True

if not(show_present):
    sys.exit()

dbx_root = dbx_path + '/' + record_dir
podcast_feed = rss_base_url + '/' + record_dir + '/' + rss_file_name
rss_full_file = rss_path + '/' + record_dir + '/' + rss_file_name 
image_link = rss_base_url + '/' + record_dir + '/' + image_file 


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

rss_fh = open(rss_full_file,'w')

rss_fh.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
rss_fh.write('<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">' + "\n")


rss_fh.write('   <channel>' + "\n")

rss_fh.write('      <title>' + podcast_name + '</title>' + "\n")
rss_fh.write('      <description>' + podcast_desc + '</description>' + "\n")
rss_fh.write('      <link>' + show_url + '</link>' + "\n")
rss_fh.write('      <itunes:author>' + station_name + '</itunes:author>' + "\n")
rss_fh.write('      <image>' + "\n")
rss_fh.write('         <url>' + image_link + '</url>' + "\n")
rss_fh.write('      </image>' + "\n")

pod_id = 0
for pod_f_md in pod_files_md:

    pod_link = pod_links[pod_id]
    pod_file_name = pod_f_md.name
    pod_file_size = pod_f_md.size
    pod_up_date = pod_f_md.client_modified
    pod_pub_date = pod_up_date.strftime('%a, %d %b %Y %H:%M:%S')

    rss_fh.write('      <item>' + "\n")
    rss_fh.write('         <guid>' + pod_link + '</guid>' + "\n")
    rss_fh.write('         <link>' + pod_link + '</link>' + "\n")
    rss_fh.write('         <title>' + pod_file_name + '</title>' + "\n")
    rss_fh.write('         <description>' + pod_file_name + '</description>' + "\n")
    rss_fh.write('         <pubDate>' + str(pod_pub_date) + ' +0000</pubDate>' + "\n")
    rss_fh.write('         <enclosure url=' + "\"" + pod_link + "\" type=\"audio/mpeg\" length=\"" + str(pod_file_size) + "\"/>" + "\n")
    rss_fh.write('      </item>' + "\n")

    pod_id = pod_id + 1

rss_fh.write('   </channel>' + "\n")

rss_fh.write('</rss>' + "\n")

rss_fh.close
