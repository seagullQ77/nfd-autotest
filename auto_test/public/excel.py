#!/usr/bin/python
#coding=utf-8

import sys
import os
import json
import xlrd

def open_excel(file):
    '''打开excel表格'''
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_by_index(filename,by_index,colnameindex=0):
    '''通过表格索引读取数据'''
    data = open_excel(filename)
    try:
        table = data.sheets()[by_index]
        nrows = table.nrows 
        ncols = table.ncols 
        colnames =  table.row_values(colnameindex)
        lst =[]
        for rownum in range(1,nrows):

            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    key = colnames[i]
                    value = row[i]
                    app[key] = value
                lst.append(app)
        return lst
    except Exception as e:
        print(str(e))

def excel_table_by_name(filename,by_name,colnameindex=0):
    '''通过表格名称读取数据'''
    data = open_excel(filename)
    try:
        table = data.sheet_by_name(by_name)
        nrows = table.nrows
        colnames =  table.row_values(colnameindex)
        lst =[]
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    key = colnames[i]
                    value = row[i]
                    app[key] = value
                lst.append(app)
        return lst
    except Exception as e:
        print(str(e))

if __name__=="__main__":
    filename = '../data/index.xlsx'
    tmp = excel_table_by_name(filename,'interfaces')
    for i in tmp:
        print(i)
