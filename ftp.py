#!/bin/python
from ftplib import FTP
import os.path
ftp = ''
sizeWritten = 0
totSize = 0
def callback(data):
	print data
	print
	
def progress(data):
    global sizeWritten
    sizeWritten += 8192
    print (str(round(sizeWritten / 1024. / 1024.,5)) + 'Mb / '+ (str(round(totSize / 1024. / 1024.,5)) + 'Mb'))
    
def login(addr, usr, pwd):
	global ftp
	ftp = FTP(addr)
	if '230' in ftp.login(user=usr, passwd=pwd):    # login into the ftp site with the correct credentials
		return True
	else:
		return False
def listFiles():
	ftp.retrlines('LIST') 	# Lists the contents of the directory
def getFile(filename):
    global sizeWritten
    global totSize
    ftp.retrbinary('RETR '+filename, progress, 8192) 	#returns the contents of the file.
    sizeWritten = 0
def upFile(filename):
    global sizeWritten
    global totSize
    direc, f = os.path.split(filename)
    os.chdir(direc)  #changes to the directory of the file
    totSize = os.path.getsize(f)
    ftp.storbinary('STOR '+f, open(f,'rb'), 8192, progress) 	 # uploads the file to the server
    #f.close()
    sizeWritten = 0
    totSize = 0
    print 'Done uploading'
def deleteFile(filename):
	ftp.delete(filename)
def changeDir(direc):
	ftp.cwd(direc)
def deleteDir(direc):
	ftp.rmd(direc)
def newDir(direc):
	ftp.mkd(direc)
def quit():
	ftp.quit()

