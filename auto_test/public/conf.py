#!/usr/bin/env python3
#coding=utf-8

import os
import configparser

current_path = os.path.abspath(os.path.dirname(__file__))
conf_file = current_path + os.sep + '..'+ os.sep + 'conf' + os.sep + 'conf.ini'

def get_conf(section,key,data_type=None):
    cf = configparser.ConfigParser()
    cf.read(conf_file,encoding='utf-8')
    if data_type == 'int':
        value = cf.getint(section,key)
    elif data_type == 'float':
        value = cf.getfloat(section,key)
    elif data_type == 'boolean':
        value = cf.getboolean(section,key)
    else:
        value = cf.get(section,key)
    return value

if __name__ == '__main__':
    print(type(get_conf('mail','flag')))