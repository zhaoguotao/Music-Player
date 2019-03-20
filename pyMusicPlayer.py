#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import re
import subprocess
import collections
import logging
from appJar import gui
import webbrowser
import pygame
from mutagen.id3 import ID3

ScrolledTextattr = 1

def ClearDisplay():
    app.clearTextArea("text")
    
def Callback_SaveMessage():
    save_time = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    ret = app.saveBox(title="save as...", fileName="pyMusicPlayer_log_"+save_time,fileTypes=[('txt', '*.txt'), ('all', '*')])
    if not ret == "":
        f = open(ret, 'w')
        text = app.getTextArea("text")
        f.write(text)
        f.close()


def Callback_MenuBarTools(value):
    if value == "Open program folder":
        filename = os.getcwd()
        if sys.platform == "win32":
            os.startfile(filename)
#             webbrowser.open(filename)
        else:
            #webbrowser.open(filename)
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
        
    elif value== "window size":
        app_size = app.getSize()
        app.infoBox("GUI size", app_size)
    elif value== "on top":
        ret = app.getMenuCheckBox("Tools", "on top")
        if ret == True:
            app.configure(top=True)
        else:
            app.configure(top=False)
    elif value== "resizable":
        ret = app.getMenuCheckBox("Tools", "resizable")
        if ret == True:
            app.setResizable(canResize=True)
        else:
            app.setResizable(canResize=False)
    
      
def aboutme():
    '''
pyMusicPlayer

version: %(__version__)
Build Time: %(__BuildData__)
Auther: 赵国涛
    '''
    app.infoBox("about me", aboutme.__doc__.replace("%(__version__)",__version__).replace("%(__BuildData__)",__BuildData__))
    
    
def Web_me():
    webbrowser.open("http://www.baidu.com")
    
def Callback_AddMusicFolder():
    Fmusic = app.directoryBox(title="Open Music Folder...")
    if not Fmusic == None:
        app.setTextArea("text","==============\n")
        app.setTextArea("text",Fmusic+'\n')
        app.setTextArea("text","==============\n")
        ScrolledTextattr.see('end')
        
        if os.path.exists(Fmusic):
            if os.path.isdir(Fmusic):
                app.clearListBox("Playlists")
                for (path,dirs,files) in os.walk(Fmusic):
                    for f_name in files:
                        if f_name.endswith(".mp3"):
                            f_name = os.path.join(path,f_name).replace("\\","/")
                            app.setTextArea("text",f_name + "\n")
                            ScrolledTextattr.see('end')
                            app.addListItem("Playlists", f_name)
        else:
            app.setTextArea("text", Fmusic + ' : The file(folder) does not exist\n')
            ScrolledTextattr.see('end')
        
    
def Callback_AddMusicFile():
    fname = app.openBox("Open Music file...",fileTypes=[('MP3', '*.mp3'),('all', '*')])
    if not fname == "":
        app.setTextArea("text","==============\n")
        app.setTextArea("text",fname+'\n')
        app.setTextArea("text","==============\n")
        ScrolledTextattr.see('end')
        
        if os.path.exists(fname):
            if os.path.isfile(fname):
                if fname.endswith(".mp3"):
                    app.addListItem("Musiclists", fname)
        else:
            app.setTextArea("text", fname + ' : The file(folder) does not exist\n')
            ScrolledTextattr.see('end')
  
def GUI_LabelFrame_Music():
    app.startFrame("LF_Music",0, 0)
    app.setSticky("wn")
    app.addMessage("112", "This feature is under development, will coming soon...\n\n\n")
    app.stopFrame()
          
def GUI_LabelFrame_Left():
    app.startScrollPane("Playlists",0,0)
#     app.startLabelFrame("LF_left",0, 0,label="Playlists")
    app.setSticky("ewns")
    app.addListBox("Playlists", [],0,0)
    app.setListBoxHeight("Playlists",25)
    app.setListBoxWidth("Playlists",30)
#     app.stopLabelFrame()
    app.stopScrollPane()#end 
         
def GUI_LabelFrame_Mid():
    global ScrolledTextattr
    app.startLabelFrame("Info",0,1,label="Info")
#     app.setLabelFrameWidth("Info", 800)
    app.setSticky("ewn")
    ScrolledTextattr = app.addScrolledTextArea("text",0,0,colspan=2)
    app.setTextAreaHeight("text",25)
    app.setTextAreaWidth("text", 40)
    app.setTextAreaFont("text", size=7, family="Verdana", slant="roman")
    app.setTextArea("text","==============\n")
    app.setTextArea("text",gui.SHOW_VERSION()+'\n')
    app.setTextArea("text","==============\n")
    app.startFrame("message_btn",1,0)
    app.addButton("Clear message",ClearDisplay,1,0)
    app.setButtonWidth("Clear message", 12)
    app.addButton("Save message as...", Callback_SaveMessage,1,1)
    app.setButtonWidth("Save message as...", 12)
    app.stopFrame()
    app.stopLabelFrame()  
    
def GUI_LabelFrame_Right():
    app.startScrollPane("Music list",0,2)
#     app.startLabelFrame("LF_right",0, 2,label="Music list")
    app.setSticky("wn")
    app.addListBox("Musiclists",[],0,0)
    app.setListBoxHeight("Musiclists",25)
    app.setListBoxWidth("Musiclists",30)
#     app.stopLabelFrame()
    app.stopScrollPane()#end 
    
def Callback_MenuBarPlaylist(value):
    print(value)
    
def GUI_MenuBar():
    app.addMenuItem("Music", "Add music folder...", Callback_AddMusicFolder,shortcut="Control-o")
    app.addMenuItem("Music", "Add music file...", Callback_AddMusicFile,shortcut="Control-j")
    app.addMenuSeparator("Music")
    app.addMenuItem("Music", "Quit", app.stop,shortcut="Control-q")
    #-----------------------------------------------------------------------
    app.addMenuList("Playlist", ["New","New from filter","-","Configure Sorting","Clear","Shuffle"], Callback_MenuBarPlaylist)
    app.addMenuSeparator("Playlist")
    app.addMenuCheckBox("Playlist", "Repeat All",Callback_MenuBarPlaylist)
    app.addMenuCheckBox("Playlist", "Repeat One",Callback_MenuBarPlaylist)
    #-----------------------------------------------------------------------
    app.addMenuList("Tools", ["Open program folder"], Callback_MenuBarTools)
    app.addMenuSeparator("Tools")
    app.addMenuItem("Tools","window size",Callback_MenuBarTools)
    app.addMenuCheckBox("Tools", "on top",Callback_MenuBarTools)
    app.addMenuCheckBox("Tools", "resizable",Callback_MenuBarTools)
    res = app.getResizable()
    if res == True:
        app.setMenuCheckBox("Tools", "resizable")
    on_top = app.getOnTop()
    if on_top == True:
        app.setMenuCheckBox("Tools", "on top")
    #-----------------------------------------------------------------------
    app.addMenuItem("Help","About",aboutme)
    app.addMenuItem("Help","Web Link",Web_me)
    
if __name__ == '__main__':
    __version__ = "v0.01"#define the version for tool
    __BuildData__ = "2019.3.20"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s  %(module)s(%(lineno)d):  %(message)s')
    
    
    app=gui("pyMusicPlayer %s"%(__version__))
    app.setSize("940x488")
    app.setFont(size=10, family="Verdana", slant="roman")
    try:
        app.setIcon("pymusic.ico")
    except Exception as e:
        logging.error(e)
        pass
    app.setSticky("ewns")
    #-----------------------------------------------------------------------
    app.startFrame("main",0,0)
    app.setSticky("ewns")
    
    app.startFrame("sub_Frame_1",0,0)
    GUI_LabelFrame_Music()
    app.stopFrame()#end sub_Frame_1
    
    app.startFrame("sub_Frame_2",1,0)
    app.setSticky("ewns")
    GUI_LabelFrame_Left()
    GUI_LabelFrame_Mid()
    GUI_LabelFrame_Right()
    app.stopFrame()#end sub_Frame_2
    
    app.stopFrame()#end main
    #-----------------------------------------------------------------------
    GUI_MenuBar()
    #-----------------------------------------------------------------------
    app.go()