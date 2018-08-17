#!/usr/bin/python

import streamrec_data 
import sys
import os

temp_output = '/tmp/cronlist'

line_str = '-----------------------------------------------------------------------------'

radio_show_list = streamrec_data.RadioShowList()
radio_show_tag_list = radio_show_list.radio_show_tag_list()
config_file = streamrec_data.read_config_file()

os.system("crontab -l > " + temp_output)
cron_show_list = {}

with open(temp_output,'r') as f_cron:
    for line in f_cron:
        cron_item = line.split(" ")
        show_tag = cron_item[6].rstrip()
        cron_show_list[show_tag] = cron_item[4] + " @ " + cron_item[1] + ":" + cron_item[0]

f_cron.close()

print(line_str)
print("Radio Shows in -> " + config_file)
print(line_str)

for show_tag in radio_show_tag_list:

    radio_show = radio_show_list.radio_show(show_tag)

    record_file_time = radio_show.get_par('record_file_time')
    record_num_files = radio_show.get_par('record_num_files')
    radio_show_name = radio_show.get_par('radio_show_name')
    radio_name = radio_show.get_par('radio_name')

    if show_tag in cron_show_list:
        print(show_tag + ' -> ' + radio_show_name + ' (' + radio_name + ')' + ' [' + cron_show_list[show_tag] + ' - ' + str(record_num_files) + 'p,' + str(record_file_time) + 's]')
    else:
        print(show_tag + ' -> ' + radio_show_name + ' (' + radio_name + ')')


print(line_str)

os.remove(temp_output)
