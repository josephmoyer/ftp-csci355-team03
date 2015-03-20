from ftplib import FTP
import os
import sys
ftp = FTP('ftp.drwestfall.net')
if '230' in ftp.login('ftp03','student'):
	print 'success'
ftp.retrlines('LIST')

totSize = os.path.getsize('10mb.txt')
totSizeMB = str(round(totSize / 1024. / 1024.,2)) + ' Mb'
sizeWritten = 0

def handler(data):
	global sizeWritten
	sizeWritten += 8192
	print (str(round(sizeWritten / 1024. /1024.,2)) + 'Mb'),
	print '/'+totSizeMB

print 'calling storlines'
ftp.storbinary('STOR 10mb.txt', open('10mb.txt','rb'), 8192, handler)

print 'Finish'
#print ftp.delete('blank.txt')
#ftp.cwd('newdir')
#ftp.retrlines('LIST')
ftp.quit()
