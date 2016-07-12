# -*- coding:utf-8 -*-
#需要安装pywin32第三方库
import MySQLdb
import datetime
import time
import win32clipboard as w
import win32con
def getText():#取剪切板
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d
fullTime=time.strftime("%Y-%m-%d %X",time.localtime())
p2pValueDate=datetime.date.today()
targetCode=getText()
a=targetCode
targetTitle='种植贷'+str(a)
try:
    conn = MySQLdb.connect(host='112.74.197.103', user='SecureTeam', passwd='Aqdy(%@#', port=9527,charset="utf8")
    cur = conn.cursor()
    conn.select_db('omega')
    cur.execute('select target_status from withdrawal_split_target WHERE target_code=%s'%targetCode)
    result=None
    result = cur.fetchone()
    if result==('DFB',):
        cur.execute("update withdrawal_split_target set target_status='DFK',target_title='%s',target_p2p_value_date='%s',target_full_time='%s' WHERE target_code=%s"%(targetTitle,p2pValueDate,fullTime,targetCode))
        print '编辑成功!','标的:%s'%targetCode,'p2p起息日：%s'%p2pValueDate,"p2p满标时间:%s"%fullTime
    else:
        print "没有改成功!标的编号错啦？标的状态是："+str(result)
    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print '修改失败！'
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
print '任意键退出！'