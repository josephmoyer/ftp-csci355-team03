#!/bin/python
from ftplib import FTP

def callback(data):
	print data
	print
def login(addr, usr, pwd):
	ftp = FTP(addr)
	ftp.login(user=usr, passwd=pwd)    # login into the ftp site with the correct credentials
def listFiles():
	ftp.retrlines('LIST') 	# Lists the contents of the directory
def getFile(filename):
	ftp.retrlines('RETR '+filename, callback) 	#returns the contents of the file. 
def upFile(filename):
	ftp.storlines('STOR '+filename, open(filename)) 	 # uploads the file to the server
def quit():
	ftp.quit()

