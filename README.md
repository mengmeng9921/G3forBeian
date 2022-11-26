# G3forBeian
红蓝对抗中，对目标单位名称使用天眼查，进行批量化查询。

# 使用方法 
python3 G3forBeian.py -h
``` 
    ▄████  ██▀███   ███▄ ▄███▓
   ██▒ ▀█▒▓██ ▒ ██▒▓██▒▀█▀ ██▒    备案查询工具
  ▒██░▄▄▄░▓██ ░▄█ ▒▓██    ▓██░
  ░▓█  ██▓▒██▀▀█▄  ▒██    ▒██     Coded By G3RM4
  ░▒▓███▀▒░██▓ ▒██▒▒██▒   ░██▒
   ░▒   ▒ ░ ▒▓ ░▒▓░░ ▒░   ░  ░    Ice technology
    ░   ░   ░▒ ░ ▒░░  ░      ░
  ░ ░   ░   ░░   ░ ░      ░       https[:]//github.com/mengmeng9921/
        ░    ░            ░

usage: G3forBeian.py [-h] [-n COMPANYNAME] [-nf COMPANYNAMEFILE] [-s SLEEPTIME] [-c COOKIE]

optional arguments:
  -h, --help            show this help message and exit
  -n COMPANYNAME, --companyname COMPANYNAME
                        -n companyname
  -nf COMPANYNAMEFILE, --companynamefile COMPANYNAMEFILE
                        -nf 1.txt
  -s SLEEPTIME, --sleeptime SLEEPTIME
                        -s 1
  -c COOKIE, --cookie COOKIE
                        -c cookie
```
# 参数详解
-h  使用帮助<br />
直接查询该公司的备案信息。<br />
-n  公司名称<br />
通过读取公司名称文件，批量化查询大量公司备案信息。<br />
-nf 公司名称文件.txt<br />
每一个网页请求的时间间隔<br />
-s  延时秒数<br />
添加cookie，可以使结果更加准确。<br />
-c  cookie<br />
