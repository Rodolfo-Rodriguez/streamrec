import json

##################################################################################
# Return config file 
##################################################################################

def read_config_file():

    _config_file =  '/home/ec2-user/config/streamrec_config_3.json'

    return _config_file 

##################################################################################
# Return config data 
##################################################################################

def read_config_data():

    _config_file = read_config_file()

    f_conf = open(_config_file,'r')
    _config_data = json.load(f_conf)
    f_conf.close()

    return _config_data

##################################################################################
# Return radio show list 
##################################################################################

def radio_show_list():

    _conf_data = read_config_data()

    return _conf_data['radio_show_list']

##################################################################################
# Return Radio Show Data 
##################################################################################

def radio_show_data(_rs_tag):

    _conf_data = read_config_data()
    _show_list = _conf_data['radio_show_list']

    _show_data = {}
    for _show in _show_list:
        if (_rs_tag == _show['radio_show_tag']):
            _show_data = _show

    return _show_data

##################################################################################
# Write Config File 
##################################################################################

def write_config_data(_config_data):

    _config_file = read_config_file()

    f_out = open(_config_file,'w')
    f_out.write(json.dumps(_config_data,indent=4))
    f_out.close()

##################################################################################
# Config Data Class 
##################################################################################

class ConfigData:

    config_data = {}

    def __init__(self):
        self.config_data = read_config_data()

    def __str__(self):
        cd_str = ""
        for par_name in self.config_data:
            par_val = self.config_data[par_name]
            if (par_name != 'radio_show_list'):
                cd_str = cd_str + str(par_name) + " : " + str(par_val) + "\n"
            else:
                rs_list = par_val

        cd_str = cd_str + 'radio_show_list : ' + '\n' 

        rs_tag_list = []
        for rs in rs_list:
            rs_tag = rs['radio_show_tag']
            cd_str = cd_str + '\t' + rs_tag + '\n'


        cd_str = cd_str.rstrip()

        return cd_str

    def write_to_file(self):
        write_config_data(self.config_data)

    def get_par(self,_par_name):
        return self.config_data[_par_name]

    def set_par(self,_par_name,_par_value):
        self.config_data[_par_name] = _par_value

    def streamrec_log_file(self):
        return self.config_data['streamrec_log_file']

##################################################################################
# Radio Show Class 
##################################################################################

class RadioShow:

    radio_show_data = {} 

    def __init__(self,_rs_tag):
        self.radio_show_data = radio_show_data(_rs_tag) 

    def __str__(self):
        rs_str = "" 
        for par_name in self.radio_show_data:
            par_val = self.radio_show_data[par_name]
            rs_str = rs_str + str(par_name) + " : " + str(par_val) + "\n"
        rs_str = rs_str.rstrip()

        return rs_str

    def data(self):
        return self.radio_show_data

    def get_par(self,_par_name):
        return self.radio_show_data[_par_name]

    def set_par(self,_par_name,_par_value):
        self.radio_show_data[_par_name] = _par_value

##################################################################################
# Radio Show List Class 
##################################################################################

class RadioShowList:

    radio_show_dict = {}

    def __init__(self):

        rs_list = radio_show_list()
        for rs in rs_list:
            rs_tag = rs['radio_show_tag']
            rs = RadioShow(rs_tag)
            self.radio_show_dict[rs_tag] = rs

    def __str__(self):
        rsd_str = ""
        for rst in self.radio_show_dict:
            rsd_str = rsd_str + rst + " , "

        return rsd_str

    def radio_show_tag_list(self):

        rs_tag_list = []

        for tag in self.radio_show_dict:
            rs_tag_list.append(tag)

        return rs_tag_list

    def radio_show(self,_rs_tag):

        return self.radio_show_dict[_rs_tag]
