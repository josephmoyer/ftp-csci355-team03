#!/bin/python
from ftplib import FTP
ftp = FTP('ftp.drwestfall.net')
ftp.login(user='ftp03', passwd='student')
ftp.retrlines('LIST')
ftp.mkd('newdir')
ftp.quit()


