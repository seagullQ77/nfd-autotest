# 说明 
脚本使用python3编写,需要安装python3.

# 执行入口:
执行main目录下的main.py

# 需要安装的第三方库:
requests:Http库,用于模拟http请求

xlrd:读取excel

HTMLReport:HTML测试报告生成

PyMySQL:连接mysql

在终端下使用如下命令进行安装:

pip3 install requests xlrd HTMLReport PyMySQL

# 目录说明 
conf 配置文件
- conf.ini 用于定义系统公共参数

data 测试数据,测试数据可按照目录中格式进行新增

main 测试入口
- main.py 测试入口

public 公共库
- check.py 校验返回值等
- conf.py 读取配置文件相关
- db.py 操作数据库相关
- excel.py 操作excel相关
- login.py 登陆相关
- mail.py 发送邮件相关
- public.py 其他

report 测试报告生成目录

testcases 生成测试用例
- nfd_case.py 生成测试用例,创建测试集