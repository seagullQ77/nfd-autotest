#!/usr/bin/env python3
#coding=utf-8

import os
import sys
current_path = os.path.abspath(os.path.dirname(__file__))
path = current_path + os.sep + '..'
sys.path.append(path)

import time
import unittest
import HTMLReport
from public import excel
from public import mail
from public import conf
from testcases.nfd_case import MyTestCase

def read_data(data_conf_file):
    '''
    读取测试数据
    '''
    data_list_final = []
    interface_list = excel.excel_table_by_name(data_conf_file, 'interfaces')

    for interface in interface_list:
        if interface.get('Flag') == 'y' or interface.get('Flag') == 'Y':
            try:
                dir_name = interface.get('Module1')
                file_name = interface.get('Module2')
                interface_name = interface.get('Interface_Name')
                data_path = os.path.dirname(data_conf_file)
                data_fullpath = data_path + os.sep + dir_name + os.sep + file_name + '.xlsx'
                data_list = excel.excel_table_by_name(data_fullpath, interface_name)
            except Exception as e:
                print(e)

            for data in data_list:
                data['Interface_Name'] = interface.get('Interface_Name')
                data['Method'] = interface.get('Method')
                data['Connect'] = interface.get('Connect')
                data_list_final.append(data)
    return data_list_final

def generate_cases(case_list_final):
    '''
    生成测试用例方法
    '''
    for case in case_list_final:
        setattr(MyTestCase,'test_%s'%case['CaseName'],MyTestCase.get_test_func(case))

def creat_suit():
    '''
    创建测试用例集
    '''
    suit = unittest.TestSuite()
    loader = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    suit.addTests(loader)

    #unittest.TextTestRunner(verbosity=2).run(suit)
    return suit

def create_report(suit):
    output_path = current_path + os.sep + '..' + os.sep + conf.get_conf('report','output_path')
    now = time.strftime("%Y%m%d%H%M%S",time.localtime())
    report_file_name = now
    report_fullpath = output_path + os.sep + report_file_name + '.html'
    runner = HTMLReport.TestRunner  (
                                    report_file_name=report_file_name,
                                    output_path=output_path,
                                    verbosity=2,
                                    title='接口测试报告',
                                    description='用例执行情况:',
                                    thread_count=1,
                                    sequential_execution=False
                                    )
    runner.run(suit)
    return report_fullpath

def main():
    '''
    测试执行入口
    '''

    # 读取excel用例数据
    data_conf = conf.get_conf('data','data_conf')
    data_conf_file = conf.get_conf('data','data_conf_file')
    data_conf = current_path + os.sep + '..' + os.sep + data_conf
    data_conf_file = data_conf + os.sep + data_conf_file

    data_list_final = read_data(data_conf_file)

    # 生成测试用例
    generate_cases(data_list_final)

    #创建测试用例集
    suit = creat_suit()

    # 生成测试报告
    test_report = create_report(suit)

    # 邮件发送测试报告
    # flag  0:不发送邮件/1:发送邮件
    flag = conf.get_conf('mail','flag','int')
    if flag == 1:
        mail.sendmail(test_report)



if __name__ == '__main__':
    main()

