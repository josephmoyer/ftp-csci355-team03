#!/bin/python
from ftplib import FTP

global ftp

def callback(data):
    print data
    print
def login():
    global ftp
    ftp = FTP('ftp.drwestfall.net')
    ftp.login('ftp03', 'student')    # login into the ftp site with the correct credentials
def listFiles():
    global ftp
    # ftp.retrlines('LIST')     # Lists the contents of the directory
    print ftp.pwd()
    data = []
    data = ftp.nlst()
    return data
def getFile(filename):
    global ftp
    login()
    ftp.retrlines('RETR '+filename, callback)   #returns the contents of the file.
def upFile(filename):
    global ftp
    ftp.storlines('STOR'+filename, open(filename))   # uploads the file to the server
def GetCurrentDir():
    print ftp.pwd()
    return ftp.pwd()
def SetCurrentDir(nameOfDir):
    print "Setting curr dir"
    ftp.cwd(nameOfDir)
def deleteFile(fileName):
    ftp.delete(fileName)
def deleteDir(dirName):
    ftp.rmd(dirName)
def quit():
    global ftp
    ftp.quit()