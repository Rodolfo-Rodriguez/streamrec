#!/usr/bin/python

import streamrec_data

str_line = '----------------------------------------------------------------------------------------'

config_data = streamrec_data.ConfigData()
config_file = streamrec_data.read_config_file()

print(str_line)
print('config_file : ' + config_file)
print(str_line)
print(config_data)
print(str_line)

