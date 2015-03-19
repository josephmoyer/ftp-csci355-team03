from ftplib import FTP
ftp = FTP('ftp.drwestfall.net')
if '230' in ftp.login('ftp03','student'):
	print 'success'
ftp.retrlines('LIST')
#print ftp.delete('blank.txt')
#ftp.cwd('newdir')
#ftp.retrlines('LIST')
ftp.quit()
