# -*- coding: utf-8 -*-
'''
Created on 2018年6月6日
@author: zww
监控系统cpu、内存以及磁盘情况，提供屏幕输出以及写入文本
'''
import time,psutil
from handler import TxtOperating as TxtOp
cpu = {'user':0,'system':0,'idle':0,'percent':0}
memory = {'total':0,'available':0,'percent':0,'used':0,'free':0}
#将磁盘单位转换成G
def change2G(disk_memory):
return str(round((disk_memory/1024/1024/1024)))
def getCpuInfo():
cpu_info = psutil.cpu_times()
cpu['user'] = cpu_info.user
cpu['system'] = cpu_info.system
cpu['idle'] = cpu_info.idle
cpu['percent'] = psutil.cpu_percent(interval=1)
def getMemoryInfo():
memory_info = psutil.virtual_memory()
memory['total'] = change2G(memory_info.total)
memory['available'] = change2G(memory_info.available)
memory['percent'] = memory_info.percent
memory['used'] = change2G(memory_info.used)
memory['free'] = change2G(memory_info.percent)
def getDiskInfo():
#磁盘名称
disk_id = []
#将每个磁盘的total used free percent 分别存入到相应的list
disk_total = []
disk_used = []
disk_free = []
disk_percent = []
for id in psutil.disk_partitions():
if 'cdrom' in id.opts or id.fstype == '':
continue
disk_name = id.device.split(':')
s = disk_name[0]
disk_id.append(s)
disk_info = psutil.disk_usage(id.device)
disk_total.append(change2G(disk_info.total))
disk_used.append(change2G(disk_info.used))
disk_free.append(change2G(disk_info.free))
disk_percent.append(disk_info.percent)
return disk_id,disk_total,disk_used,disk_free,disk_percent
def formating(disk_id,disk_total,disk_used,disk_free,disk_percent):
all_str = ''
length_of_disk = len(disk_id)
for i in range(length_of_disk):
str = '磁盘 %s:总内存量 %sG,已用 %sG,剩余 %sG,使用率为%s%%'%(disk_id[i],disk_total[i],disk_used[i],disk_free[i],disk_percent[i])
# print(str) #需要输出在命令台则取消注释
all_str = ''.join([all_str,str,'\n'])
return all_str
def run():
while True:
runtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
getCpuInfo()
getMemoryInfo()
disk_id,disk_total,disk_used,disk_free,disk_percent = getDiskInfo()
cpu_str = ''.join(['CPU使用率:',str(cpu['percent'])])
memory_str = '內存 :总内存量 %sG,已用 %sG,剩余 %sG,使用率为%s%%'%(memory['total'],memory['used'],memory['available'],memory['percent'])
disk_str = formating(disk_id,disk_total,disk_free,disk_used,disk_percent)
str_all = ''.join([runtime,'\n',cpu_str,'\n',memory_str,'\n',disk_str])
print(str_all)
#构造监控文本存放的路径和命名
cur_dir = os.path.abspath(os.path.dirname(__file__))
run_time = time.strftime('%Y%m%d_%H%M%S',time.localtime())
result_path = ''.join([cur_dir,'\\MonitorResult\\',run_time,'sysMonitor.txt'])
TxtOp.write(str_all,result_path)
time.sleep(3)