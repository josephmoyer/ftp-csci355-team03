#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Thu Mar 19 16:33:14 2015
#

import wx
import time
# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
import os
import stat
# from self.ftp import login,quit,getFile,upFile,listFiles,GetCurrentDir,SetCurrentDir,deleteFile,deleteDir,CreateNewDir
from ftplib import FTP
from threading import Thread
# ShowPath

from wx.lib.pubsub import Publisher

class MyFrame(wx.Frame):
    address = ''
    user = ''
    pwd = ''
    sizeWritten = 0
    totSize = 0
    ftp = ''

# Login
    def login(self, addr, usr, pwd):
        # global ftp
        self.ftp = FTP(addr)
        if '230' in self.ftp.login(user=usr, passwd=pwd):    # login into the ftp site with the correct credentials
            return True
        else:
            return False


# List Files
    def listFiles(self):
        # global self.ftp
        # self.ftp.retrlines('LIST')     # Lists the contents of the directory
        print self.ftp.pwd()
        data = []
        data = self.ftp.nlst()
        return data

# Get Files 
    def getFile(self, path):
        self.sizeWritten = 0
        self.totSize = 0
        self.percent = 0

        print path
        localDirec, f = os.path.split(path)

        self.totSize = self.getFileSize(f)
        os.chdir(localDirec)

        with open(f, 'wb') as fhandle:
            def callback(chunk):
                fhandle.write(chunk)
                self.sizeWritten += 8192

                self.percent = int(100 * float(self.sizeWritten)/float(self.totSize))
                wx.Yield()
                self.gauge_1.SetValue(self.percent)
            self.ftp.retrbinary('RETR ' + f, callback, 8192)


        # fhandle = open(filename, 'wb')
        # self.ftp.retrbinary('RETR ' + f, open(f, 'wb').write, 8192, self.downProgress)
        # fhandle.close()
        # f.close()



        self.gauge_1.SetValue(0)
        print 'Done downloading'

# Up File
    def upFile(self, event, filename):
        self.sizeWritten = 0
        self.totSize = 0
        self.percent = 0

        direc, f = os.path.split(filename)
        os.chdir(direc)  #changes to the directory of the file
        self.totSize = os.path.getsize(f)

        # self.ftp.storlines('STOR '+f, open(f))    # uploads the file to the server

        self.ftp.storbinary('STOR '+f, open(f,'rb'), 8192, self.fileProgress)    # uploads the file to the server
        # f.close()
        time.sleep(2)
        self.gauge_1.SetValue(0)
        print 'Done uploading'

# Delete Files 
    def deleteFile(self, filename):
        self.ftp.delete(filename)

# Get Current File 
    def GetCurrentDir(self):
        # print self.ftp.pwd()
        return self.ftp.pwd()

# Set Current Directory
    def SetCurrentDir(self, nameOfDir):
        # print "Setting curr dir"
        # print nameOfDir
        self.ftp.cwd(nameOfDir)

# Create New Directory 
    def CreateNewDir(self, name):
        self.ftp.dir()
        # os.chdir(GetCurrentDir())
        self.ftp.mkd(name)

# Delete File 
    def deleteFile(self, fileName):
        self.ftp.delete(fileName)

# Delete Directory 
    def deleteDir(self, dirName):
        self.ftp.rmd(dirName)

# Set Permissions 
    def setMode(self, mode,filename):
        self.ftp.sendcmd('SITE CHMOD ' + str(mode) + ' ' + filename)
        print "Permissions have been set"
        # self.seePerm(filename)

    # def seePerm(self, filename):
    #     self.ftp.sendcmd('SITE ls -l ' + filename)

    def fileProgress(self, data):
        self.sizeWritten += 8192
        print self.sizeWritten
        print self.totSize
        # # self.label_2.SetLabel(str(round(self.sizeWritten / 1024. / 1024.,4)) + 'Mb / '+ (str(round(self.totSize / 1024. / 1024.,4)) + 'Mb'))
        # print (str(round(self.sizeWritten / 1024. / 1024.,4)) + 'Mb / '+ (str(round(self.totSize / 1024. / 1024.,4)) + 'Mb'))
        # self.currentSize = self.totSize - self.sizeWritten
        self.percent = int(100 * float(self.sizeWritten)/float(self.totSize))

        print self.percent

        wx.Yield()
        self.gauge_1.SetValue(self.percent)

        print 'File Progress'

    def getFileSize(self, filename):
        self.ftp.sendcmd("TYPE i")
        return self.ftp.size(filename)
# Quit
    def quit(self):
        self.ftp.quit()




# Def Init
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Host Address:"))
        self.txtHostAddress = wx.TextCtrl(self, wx.ID_ANY, "")
        self.btnConnect = wx.Button(self, wx.ID_ANY, _("Connect..."))
        self.static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Current Path:"))
        self.txtPath = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.listboxFiles = wx.ListBox(self, wx.ID_ANY, choices=[])
        self.btnUpload = wx.Button(self, wx.ID_ANY, _("Upload File..."))
        self.btnDownload = wx.Button(self, wx.ID_ANY, _("Download File..."))
        self.static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        self.btnOpenDir = wx.Button(self, wx.ID_ANY, _("Open Folder"))
        self.btnNewDir = wx.Button(self, wx.ID_ANY, _("New Folder..."))
        self.btnDel = wx.Button(self, wx.ID_ANY, _("Delete"))
        self.static_line_3 = wx.StaticLine(self, wx.ID_ANY)
        self.btnProperties = wx.Button(self, wx.ID_ANY, _("Properties..."))
        self.gauge_1 = wx.Gauge(self, wx.ID_ANY, range=100)

        self.__set_properties()
        self.__do_layout()

        # self.Bind(wx.EVT_TEXT, self.txtHostAddress_Changed, self.txtHostAddress)
        self.Bind(wx.EVT_BUTTON, self.btnConnect_Click, self.btnConnect)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.listboxFiles_DoubleClick, self.listboxFiles)
        # self.Bind(wx.EVT_LISTBOX, self.listboxFiles_Click, self.listboxFiles)
        self.Bind(wx.EVT_BUTTON, self.btnUpload_Click, self.btnUpload)
        self.Bind(wx.EVT_BUTTON, self.btnDownload_Click, self.btnDownload)
        self.Bind(wx.EVT_BUTTON, self.btnOpenDir_Click, self.btnOpenDir)
        self.Bind(wx.EVT_BUTTON, self.btnNewDir_Click, self.btnNewDir)
        self.Bind(wx.EVT_BUTTON, self.btnDel_Click, self.btnDel)
        self.Bind(wx.EVT_BUTTON, self.btnProperties_Click, self.btnProperties)
        # end wxGlade



        # Used in conjunction with the easy login
        # login()
        # self.showFiles()

# Set Properties
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("self.ftp Client"))
        self.SetSize((600, 300))
        self.label_3.SetMinSize((100, 17))
        self.txtHostAddress.SetMinSize((400, 27))
        self.btnConnect.SetMinSize((100, 29))
        self.static_line_1.SetMinSize((600, 5))
        self.label_1.SetMinSize((100, 17))
        self.txtPath.SetMinSize((350, 27))
        self.listboxFiles.SetMinSize((450, 218))
        self.btnUpload.SetMinSize((150, 29))
        self.btnDownload.SetMinSize((150, 30))
        self.static_line_2.SetMinSize((148, 5))
        self.btnOpenDir.SetMinSize((150, 29))
        self.btnNewDir.SetMinSize((150, 29))
        self.btnDel.SetMinSize((150, 29))
        self.static_line_3.SetMinSize((148, 5))
        self.btnProperties.SetMinSize((150, 29))
        self.gauge_1.SetMinSize((600, 15))
        # end wxGlade

# Do Layout
    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.txtHostAddress, 0, 0, 0)
        sizer_2.Add(self.btnConnect, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND | wx.SHAPED, 0)
        sizer_1.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_8.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.txtPath, 0, 0, 0)
        sizer_7.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_7.Add(self.listboxFiles, 0, 0, 0)
        sizer_6.Add(sizer_7, 3, wx.EXPAND, 0)
        sizer_9.Add(self.btnUpload, 0, 0, 0)
        sizer_9.Add(self.btnDownload, 0, 0, 0)
        sizer_9.Add(self.static_line_2, 0, wx.EXPAND, 0)
        sizer_9.Add(self.btnOpenDir, 0, 0, 0)
        sizer_9.Add(self.btnNewDir, 0, 0, 0)
        sizer_9.Add(self.btnDel, 0, 0, 0)
        sizer_9.Add(self.static_line_3, 0, wx.EXPAND, 0)
        sizer_9.Add(self.btnProperties, 0, 0, 0)
        sizer_6.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 8, wx.EXPAND, 0)
        sizer_1.Add(self.gauge_1, 0, 0, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade


# Button Connect Click
    def btnConnect_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        # event.Skip()
        address = self.txtHostAddress.GetLineText(0)
        print address

        if address == '':
            wx.MessageBox('Please enter address first')
            return

        user = wx.TextEntryDialog(None,'Enter username','Login','')
        if user.ShowModal() == wx.ID_OK:
            user = user.GetValue()
            pwd = wx.TextEntryDialog(None,'Enter password','Login','')
            if pwd.ShowModal() == wx.ID_OK:
                pwd = pwd.GetValue()
            if not pwd or not user:
                wx.MessageBox('username/password cannot be blank')
                return
        if self.login(address, user, pwd) == False:
            wx.MessageBox('Check login credentials')
            return
        else:
            wx.MessageBox('Login Successful')
            self.showFiles()
            self.updatePath('/')


# Button Double Click
    def listboxFiles_DoubleClick(self, event):  # wxGlade: MyFrame.<event_handler>
        # global fullPath
        print "Entered view dir"

        try:        
            if self.listboxFiles.GetStringSelection() == '<--':
                self.SetCurrentDir('..')
                # self.fullPath.pop()
                currDir = self.GetCurrentDir()
                self.updatePath(currDir)
            else:
                self.SetCurrentDir(self.listboxFiles.GetStringSelection())
                # print self.listboxFiles.GetStringSelection()
                currDir = self.GetCurrentDir()
                print currDir
                # self.fullPath.append(currDir)
                self.updatePath(currDir)
        except:
            print "Unexpected error:"
            raise

        
        # GetCurrentDir()

        self.listboxFiles.Clear()

        if self.GetCurrentDir() != '/':
            self.listboxFiles.Append('<--')
        else:
            self.listboxFiles.Delete(0)

        self.showFiles()



# Upload Click
    def btnUpload_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        filename = ''
        dlg = wx.FileDialog(self, message="Choose a file")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
        if not filename:
           return
        self.upFile(event, filename)
        self.listboxFiles.Clear()
        self.showFiles()
        # event.Skip()


# Download Click
    def btnDownload_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        filename = self.listboxFiles.GetStringSelection()

        msg = "Save " + filename + " file"

        save_dlg = wx.FileDialog(self, msg,"",filename,"",wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if save_dlg.ShowModal() == wx.ID_CANCEL:
            return

        path = save_dlg.GetPath()

        self.getFile(path)


# Directory Button Click
    def btnOpenDir_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        self.listboxFiles_DoubleClick(event)


# New Directory Button Click
    def btnNewDir_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        # os.chdir(GetCurrentDir())

        dir_name = wx.TextEntryDialog(None,'Enter directory name','Name','')

        if dir_name.ShowModal() == wx.ID_CANCEL:
            return

        self.CreateNewDir(dir_name.GetValue())

        self.listboxFiles.Clear()

        self.listboxFiles.Append('<--')

        self.showFiles()


# Delete Button Click
    def btnDel_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        item = self.listboxFiles.GetStringSelection()

        if item.find('.') != -1:
            self.deleteFile(item)
        else:
            self.deleteDir(item)

        self.listboxFiles.Clear()

        self.showFiles()



    def btnProperties_Click(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = MyDialog(self)

        if dlg.ShowModal() == wx.ID_OK:
            mode = 0
            filename = self.GetCurrentDir() + self.listboxFiles.GetStringSelection()
            print filename #DEBUG
        
            if(dlg.chkOwnRead.GetValue()): mode += 400
            if(dlg.chkOwnWrite.GetValue()): mode += 200
            if(dlg.chkOwnExe.GetValue()): mode += 100
            if(dlg.chkGrpRead.GetValue()): mode += 40
            if(dlg.chkGrpWrite.GetValue()): mode += 20
            if(dlg.chkGrpExe.GetValue()): mode += 10
            if(dlg.chkPubRead.GetValue()): mode += 4
            if(dlg.chkPubWrite.GetValue()): mode += 2
            if(dlg.chkPubExe.GetValue()): mode += 1
            self.setMode(mode,filename)
        dlg.Destroy()

# Show Files
    def showFiles(self):
        data = self.listFiles()

        for x in data:
            self.listboxFiles.Append(x)


# Update Path
    def updatePath(self, currDir):
        # filename = self.listboxFiles.GetStringSelection()
        # path = str(ShowPath(filename))
        self.txtPath.Clear()
        # path = ''.join(self.fullPath)
        self.txtPath.WriteText(currDir)


# end of class MyFrame

# MyDialog Class
class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.chkOwnRead = wx.CheckBox(self, wx.ID_ANY, _("Read"))
        self.chkOwnWrite = wx.CheckBox(self, wx.ID_ANY, _("Write"))
        self.chkOwnExe = wx.CheckBox(self, wx.ID_ANY, _("Execute"))
        self.sizer_16_staticbox = wx.StaticBox(self, wx.ID_ANY, _("Owner Permissions"))
        self.chkGrpRead = wx.CheckBox(self, wx.ID_ANY, _("Read"))
        self.chkGrpWrite = wx.CheckBox(self, wx.ID_ANY, _("Write"))
        self.chkGrpExe = wx.CheckBox(self, wx.ID_ANY, _("Execute"))
        self.sizer_17_staticbox = wx.StaticBox(self, wx.ID_ANY, _("Group Permissions"))
        self.chkPubRead = wx.CheckBox(self, wx.ID_ANY, _("Read"))
        self.chkPubWrite = wx.CheckBox(self, wx.ID_ANY, _("Write"))
        self.chkPubExe = wx.CheckBox(self, wx.ID_ANY, _("Execute"))
        self.sizer_18_staticbox = wx.StaticBox(self, wx.ID_ANY, _("Public Permissions"))
        self.btnPropOK = wx.Button(self, wx.ID_ANY, _("OK"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.btnPropOK_Click, self.btnPropOK)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle(_("Properties"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_18_staticbox.Lower()
        sizer_18 = wx.StaticBoxSizer(self.sizer_18_staticbox, wx.HORIZONTAL)
        self.sizer_17_staticbox.Lower()
        sizer_17 = wx.StaticBoxSizer(self.sizer_17_staticbox, wx.HORIZONTAL)
        self.sizer_16_staticbox.Lower()
        sizer_16 = wx.StaticBoxSizer(self.sizer_16_staticbox, wx.HORIZONTAL)
        sizer_16.Add(self.chkOwnRead, 0, 0, 0)
        sizer_16.Add(self.chkOwnWrite, 0, 0, 0)
        sizer_16.Add(self.chkOwnExe, 0, 0, 0)
        sizer_15.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_17.Add(self.chkGrpRead, 0, 0, 0)
        sizer_17.Add(self.chkGrpWrite, 0, 0, 0)
        sizer_17.Add(self.chkGrpExe, 0, 0, 0)
        sizer_15.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_18.Add(self.chkPubRead, 0, 0, 0)
        sizer_18.Add(self.chkPubWrite, 0, 0, 0)
        sizer_18.Add(self.chkPubExe, 0, 0, 0)
        sizer_15.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_15.Add(self.btnPropOK, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_15)
        sizer_15.Fit(self)
        self.Layout()
        # end wxGlade

    def btnPropOK_Click(self, event):  # wxGlade: MyDialog.<event_handler>
        print "Event handler 'btnPropOK_Click' not implemented!"
        self.EndModal(wx.ID_OK)
        event.Skip()


# end of class MyDialog

# MyApp Class
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

# Main
if __name__ == "__main__":
    gettext.install("FTP_Client") # replace with the appropriate catalog name

    FTP_Client = MyApp(0)
    FTP_Client.MainLoop()
