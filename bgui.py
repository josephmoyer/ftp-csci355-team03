#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Wed Mar  4 13:05:49 2015
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
from ftp import login,quit,getFile,upFile,listFiles
class MyFrame2(wx.Frame):
    global address
    address = ''
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame2.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("FTP"))
        self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Enter FTP server address:"))
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_2 = wx.Button(self, wx.ID_ANY, _("Connect"))
        self.button_1 = wx.Button(self, wx.ID_ANY, _("Click to select file to upload"))
        self.label_2 = wx.StaticText(self, wx.ID_ANY, _("File will appear here\n"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.TextHandler, self.text_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.Conn, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.FileUpload, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame2.__set_properties
        self.label_1.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Cantarell"))
        self.text_ctrl_1.SetMinSize((200, 30))
        self.label_2.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Cantarell"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame2.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_3.Add(self.label_3, 0, 0, 0)
        sizer_3.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_3.Add(self.button_2, 0, 0, 0)
        sizer_3.Add(self.button_1, 0, 0, 0)
        sizer_3.Add(self.label_2, 0, 0, 0)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)
        self.Layout()
        # end wxGlade

    def TextHandler(self, event):  # wxGlade: MyFrame2.<event_handler>
	    global address
	    address = event.GetString()

    def Conn(self, event):  # wxGlade: MyFrame2.<event_handler>
	    if not address:
		    wx.MessageBox('Please enter address first')
		    return
	    user = wx.TextEntryDialog(None,'Enter username','Login','')
	    if user.ShowModal() == wx.ID_OK:
		    user = user.GetValue()
		    pwd = wx.TextEntryDialog(None,'Enter password','Login','')
		    if pwd.ShowModal() == wx.ID_OK:
			    pwd = pwd.GetValue()
		    if not pwd or not user:
			   return
	    login(address, user, pwd)
	    

    def FileUpload(self, event):  # wxGlade: MyFrame2.<event_handler>
        filename = '' 
        dlg = wx.FileDialog(self, message="Choose a file")
        if dlg.ShowModal() == wx.ID_OK:
	        filename = dlg.GetPath()
        dlg.Destroy()
        if not filename:
		   return
        upFile(filename)
        self.label_2.SetLabel(filename)
        quit()

# end of class MyFrame2
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_3 = MyFrame2(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_3)
    frame_3.Show()
    app.MainLoop()
