#!/bin/python
from ftplib import FTP
import os.path
ftp = ''
def callback(data):
	print data
	print
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
	ftp.retrlines('RETR '+filename, callback) 	#returns the contents of the file. 
def upFile(filename):
	direc, f = os.path.split(filename)
	os.chdir(direc)  #changes to the directory of the file
	ftp.storlines('STOR '+f, open(f)) 	 # uploads the file to the server
def deleteFile(filename):
	ftp.delete(filename)
def changeDir(direc):
	ftp.cwd(direc)
def deleteDir(direc):
	ftp.rmd(direc)
def newDir(direc)
	ftp.mkd(direc)
def quit():
	ftp.quit()

