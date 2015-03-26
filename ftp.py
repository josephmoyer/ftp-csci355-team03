#!/bin/python
from ftplib import FTP
import os, os.path
global ftp
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

# Easy login to skip entering data
# def login():
# 	global ftp
# 	ftp = FTP('ftp.drwestfall.net')

# 	ftp.login('ftp03', 'student')

def listFiles():
    global ftp
    # ftp.retrlines('LIST')     # Lists the contents of the directory
    print ftp.pwd()
    data = []
    data = ftp.nlst()
    return data
def getFile(path):
	direc, filename = os.path.split(path)
	os.chdir(direc)
	fhandle = open(filename, 'wb')
	ftp.retrbinary("RETR " + filename, fhandle.write)
	fhandle.close()

	# ftp.retrlines('RETR '+filename, callback) 	#returns the contents of the file. 
def upFile(filename):
	direc, f = os.path.split(filename)
	os.chdir(direc)  #changes to the directory of the file
	ftp.storlines('STOR '+f, open(f)) 	 # uploads the file to the server
def deleteFile(filename):
	ftp.delete(filename)
def GetCurrentDir():
    # print ftp.pwd()
    return ftp.pwd()
def SetCurrentDir(nameOfDir):
    # print "Setting curr dir"
    # print nameOfDir
    ftp.cwd(nameOfDir)
def CreateNewDir(name):
	ftp.dir()
	# os.chdir(GetCurrentDir())
	ftp.mkd(name)
def deleteFile(fileName):
    ftp.delete(fileName)
def deleteDir(dirName):
    ftp.rmd(dirName)
# def ShowPath(filename):
# 	print os.path.realpath(filename)
# 	return os.path.realpath(filename)
def quit():
	ftp.quit()

