#!/bin/python
from ftplib import FTP

def callback(data):
	print data
	print

ftp = FTP('ftp.drwestfall.net')
ftp.login(user='ftp03', passwd='student')    # login into the ftp site with the correct credentials
ftp.getwelcome() 	# does not do anything at the moment
ftp.retrlines('LIST') 	# Lists the contents of the directory
ftp.retrlines('RETR test.txt', callback) 	#returns the contents of the file. 
ftp.storlines('STOR newfile.txt', open('newfile.txt')) 	 # uploads the file to the server
ftp.retrlines('RETR newfile.txt', callback)

ftp.quit()


