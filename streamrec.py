#!/usr/bin/python

import time
import sys
import os
import json
import dropbox
import eyed3

gen_config_file = '/home/ec2-user/config/gen_config.json'

###########################################################################################################################
# Funciones 
###########################################################################################################################

def write_log(log_f,log_str,show_n):

	f_log = open(log_f,'a')
	time_str = time.strftime("%d/%m/%Y-%H:%M:%S")
	f_log.write(time_str + " -> [" + show_n + "] " + log_str + '\n')
	f_log.close()
	
	return True

def tag_file(f_name,p_name,date_s,track_n,image_f):

    audiofile = eyed3.load(f_name)
    audiofile.initTag()

    tag_u = (p_name + ' del ' + date_s.replace("_","/") + ' Parte ' + str(track_n)).decode('utf-8') 
    audiofile.tag.title = tag_u 

    tag_u = p_name.decode('utf-8') 
    audiofile.tag.artist = tag_u 

    tag_u = date_s.decode('utf-8') 
    audiofile.tag.album = tag_u 

    audiofile.tag.track_num = track_n 

    imagedata = open(image_f,"rb").read()
    audiofile.tag.images.set(3,imagedata,"image/jpeg",u"description")

    audiofile.tag.save()

###########################################################################################################################
# Lee Parametros de archivo de configuracion 
###########################################################################################################################

f_conf = open(gen_config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

config_file = input_data['streamrec_config_file'] 
log_file = input_data['streamrec_log_file']

audio_path = input_data['podcasts_path']
dbx_path = input_data['dropbox_path']

strrip_exe = input_data['streamripper_exe']
create_feed_exe = input_data['create_feed_exe'] 
create_pls_exe = input_data['create_pls_exe'] 
	
dbx_auth_token = input_data['dropbox_access_token'] 

rss_image_file = input_data['rss_image_file']
rss_feeds_path = input_data['rss_feeds_path']

###########################################################################################################################
# Lee Parametros de Entrada  
###########################################################################################################################

list_argv = sys.argv
num_argv_in = len(list_argv)

if (num_argv_in < 2):
	print("ERROR: Uso -> " + list_argv[0] + " show_name")
	sys.exit()

show_name = list_argv[1]

###########################################################################################################################
# Lee Archivo de Configuracion
###########################################################################################################################

f_conf = open(config_file,'r')
input_data = json.load(f_conf)
f_conf.close()

show_present = False
for item in input_data:
	if (show_name == item['show_name']):
		stream_url = item['stream_url']
		stream_codec = item['stream_codec']
		record_time = int(item['record_time'])
		record_files = int(item['record_files'])
		min_file_size = int(item['min_file_size']) * 1024
		record_dir = item['record_dir']
		podcast_name = item['podcast_name']
		show_present = True

if not(show_present):
	sys.exit()

date_str = time.strftime("%Y_%m_%d")
file_name_base = show_name + '-' + date_str
image_file = rss_feeds_path + "/" + record_dir + "/" + rss_image_file
	
log_string = '[main] Iniciando grabacion de ' + podcast_name + ' -> ' + str(record_files) + ' partes de ' + str(record_time) + ' segundos' 
write_log(log_file,log_string,show_name)	

###########################################################################################################################
# Graba el Stream
###########################################################################################################################

for file_id in range(1,record_files+1):

    file_name = audio_path + '/' + record_dir + "/" + file_name_base + "-" + str(file_id) + "." + stream_codec
    dbx_file = dbx_path + '/' + record_dir + "/" + file_name_base + "-" + str(file_id) + "." + stream_codec
	
    log_string = '[rec] Grabando parte ' + str(file_id) + ' de ' + str(record_files) + ' por ' + str(record_time) + ' segundos ' 
    write_log(log_file,log_string,show_name)	

    cmd_str = strrip_exe + " " + stream_url + " -l " + str(record_time) + " -d " + audio_path + " -a " + file_name + " -A --quiet -u \"test\" -o always"
    os.system(cmd_str)
	
    log_string = '[rec] Grabacion guardada en ' + file_name
    write_log(log_file,log_string,show_name)	

###########################################################################################################################
# Recorre archivos, borra los chicos y crea lista 
###########################################################################################################################

root_dir = audio_path + '/' + record_dir
recorded_files = []

for root, dirs, files in os.walk(root_dir):

    for f_name in files:

        if date_str in f_name:    

            full_file_name = os.path.join(root, f_name)
            f_size = os.stat(full_file_name).st_size

            if f_size < min_file_size:
                os.remove(full_file_name)
                log_string = '[del] Borrando archivo ' + full_file_name + ' por ser menor a ' + str(min_file_size) + ' Bytes'
                write_log(log_file,log_string,show_name)	
            else:
                recorded_files.append(f_name)

recorded_files.sort()

###########################################################################################################################
# Sube archivos a dropbox 
###########################################################################################################################

dbx = dropbox.Dropbox(dbx_auth_token)
track_count = 1

for f_name in recorded_files:

    full_file_name = audio_path + '/' + record_dir + '/' + f_name 
    new_file_name = audio_path + '/' + record_dir + '/' + file_name_base + "-p" + str(track_count) + "." + stream_codec  

    os.rename(full_file_name,new_file_name)

    #tag_file(new_file_name,podcast_name,date_str,track_count,image_file)

    dbx_file = dbx_path + '/' + record_dir + '/' + file_name_base + "-p" + str(track_count) + "." + stream_codec 
    with open(new_file_name,'rb') as f:
        data = f.read()
        dbx.files_upload(data,dbx_file)

    log_string = '[dbx] Subiendo a Dropbox ' + dbx_file
    write_log(log_file,log_string,show_name)	

    track_count = track_count + 1


###########################################################################################################################
# Actualizando Feed 
###########################################################################################################################

genfeed_cmd = "python " + create_feed_exe + " " + show_name 
os.system(genfeed_cmd)

genpls_cmd = "python " + create_pls_exe + " " + show_name 
os.system(genpls_cmd)

log_string = '[feed] Actualizando Feed'
write_log(log_file,log_string,show_name)	

###########################################################################################################################
# Borra Archivos 
###########################################################################################################################

track_count = 1
for f_name in recorded_files:

    new_file_name = audio_path + '/' + record_dir + '/' + file_name_base + "-p" + str(track_count) + "." + stream_codec  
    os.remove(new_file_name)

    log_string = '[clean] Borrando Archivo Local ' + new_file_name
    write_log(log_file,log_string,show_name)	

    track_count = track_count + 1


log_string = '[main] Grabacion de ' + podcast_name + ' finalizada'
write_log(log_file,log_string,show_name)	
