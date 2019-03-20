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
SongFilenames=[]
SongTitles = []
index=0#current music file index
count=0#the numbers of music file
CurrVol = 0#volume value

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
    global count
    global index
    logging.info("Execute cmd: Open music folder")
    Fmusic = app.directoryBox(title="Open Music Folder...")
    if not Fmusic == None:
        app.setTextArea("text","Load music folder: " + Fmusic+'\n')
        ScrolledTextattr.see('end')
        count=0
        index=0
        del SongFilenames[:]
        del SongTitles[:]
        os.chdir(Fmusic)
        for  files in os.listdir(Fmusic):
            try:
                if files.endswith(".mp3"):
                    realdir = os.path.realpath(files)#F:\CloudMusic\Anesthesia.mp3
                    SongTitles.append(ID3(realdir)['TIT2'].text[0])
                    SongFilenames.append(files)
            except Exception as e:
                logging.error(e)
                
        if SongFilenames == [] :
            app.infoBox('Info',"No songs found")
        else:
            app.setEntry("Fmp3", Fmusic)
            app.clearListBox("Playlists")
            for i in SongFilenames:
                count = count + 1
                app.addListItem("Playlists", i)
            pygame.mixer.init()
            pygame.mixer.music.load(SongFilenames[0])
            app.setTextArea("text","Playing: " + SongFilenames[0] +'\n')
            ScrolledTextattr.see('end')
            pygame.mixer.music.play()
            app.setButton("PlayOrPause", "Play")#Update button state
            Callback_DisplayCurrentSong("Playing...")
    else:
        return 1        
    
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
                    app.addListItem("Playlists", fname)
        else:
            app.setTextArea("text", fname + ' : The file(folder) does not exist\n')
            ScrolledTextattr.see('end')
  
def Callback_DisplayCurrentSong(state):
    global index
    app.setLabel("L_song", SongFilenames[index]+"[%s]"%(state))

def Callback_MusicState():
    '''
    0: song is stopped or not play
    1: song is playing
    '''
    ret = pygame.mixer.music.get_busy()
    return ret

def Callback_PlayOrPause():
    try:
        but_state = app.getButton("PlayOrPause")
        ret = pygame.mixer.music.get_busy()
        if ret == 1:#not stop
            if but_state == "Pause":
                app.setButton("PlayOrPause", "Play")
                Callback_DisplayCurrentSong("Playing...")
                if ret == 1:
                    logging.info("Execute cmd: unpause")
                    pygame.mixer.music.unpause()
                    app.setTextArea("text","Unpaused: " + SongFilenames[index] +'\n')
                    ScrolledTextattr.see('end')
                else:
                    logging.info("Execute cmd: play")
                    pygame.mixer.music.play()
                    app.setTextArea("text","Play: " + SongFilenames[index] +'\n')
                    ScrolledTextattr.see('end')
            else:
                app.setButton("PlayOrPause", "Pause")
                Callback_DisplayCurrentSong("Paused...")
                logging.info("Execute cmd: pause")
                pygame.mixer.music.pause()
                app.setTextArea("text","Paused: " + SongFilenames[index] +'\n')
                ScrolledTextattr.see('end')
        else:#if song is stopped, replay
            app.setButton("PlayOrPause", "Play")
            Callback_DisplayCurrentSong("Playing...")
            logging.info("Execute cmd: play")
            pygame.mixer.music.play()
            app.setTextArea("text","Play: " + SongFilenames[index] +'\n')
            ScrolledTextattr.see('end')
    except Exception as e:
        logging.error(e)
        app.infoBox('Info',"Please add music file first")
        
def Callback_Stop():
    try:
        pygame.mixer.music.stop()
        Callback_DisplayCurrentSong("Stopped...")
        app.setTextArea("text","Stoped: " + SongFilenames[index] +'\n')
        ScrolledTextattr.see('end')
        logging.info("Execute cmd: stop")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info',"Please add music file first")
        
def Callback_Previous():
    global index
    index -= 1
    try:
        if index < 0:
            index = count-1
        pygame.mixer.music.load(SongFilenames[index])
        app.setTextArea("text","Playing: " + SongFilenames[index] +'\n')
        ScrolledTextattr.see('end')
        pygame.mixer.music.play()
        app.setButton("PlayOrPause", "Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: Previous and play")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info',"Please add music file first")
        
def Callback_Next():
    global index,count
    index += 1
    if index > count -1:
        index = 0
    try:
        pygame.mixer.music.load(SongFilenames[index])#load() requires filename is english
        app.setTextArea("text","Playing: " + SongFilenames[index] +'\n')
        ScrolledTextattr.see('end')
        pygame.mixer.music.play()
        app.setButton("PlayOrPause", "Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: next and play")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info',"Please add music file first")
      
def Callback_VolumeMute():
    global CurrVol
    if app.getButtonBg("Mute") == "SystemButtonFace":#no mute
        try:
            CurrVol = app.getScale("Vol:")
            app.setScale("Vol:", 0,callFunction=False)
            pygame.mixer.music.set_volume(0)
            app.setButtonBg("Mute", "red")
            logging.info("Execute cmd: volume set to 0(mute)")
        except Exception as e:
            logging.error(e)
    else:
        try:
            app.setScale("Vol:", CurrVol,callFunction=False)
            vol = float(CurrVol)/100
            pygame.mixer.music.set_volume(vol)
            app.setButtonBg("Mute", "SystemButtonFace")
            logging.info("Execute cmd: volume set: %f"%(vol))
        except Exception as e:
            logging.error(e)
          
def Callback_VolumeCtrl():
    global CurrVol
    try:
        value = app.getScale("Vol:")
        CurrVol = app.getScale("Vol:")
        vol = float(value)/100
        pygame.mixer.music.set_volume(vol)
        if vol == 0:
            app.setButtonBg("Mute", "red")
        else:
            app.setButtonBg("Mute", "SystemButtonFace")
        logging.info("Execute cmd: volume set: %f"%(vol))
    except Exception as e:
        logging.error(e)
        
def Callback_Button(value):
    if value == "PlayOrPause":
        Callback_PlayOrPause()
    elif value == "Stop":
        Callback_Stop()
    elif value == "Previous":
        Callback_Previous()
    elif value == "Next":
        Callback_Next()
    elif value == "Mute":
        Callback_VolumeMute()

def Callback_OpenMusicFolder():
    f_path=app.getEntry("Fmp3")
    if f_path == "":
        app.warningBox("Warning","Import mp3 folder first")
        return -1
    try:
        webbrowser.open(f_path)
    except Exception as e:
        app.warningBox("Warning",e)
        logging.error(e)
        
#-----------GUI------------
def GUI_LabelFrame_Music():
    app.startFrame("LF_Music",0, 0)
    app.setSticky("wn")
    app.startFrame("LF_Music_folder",0, 0)
    app.setSticky("ewns")
    app.addEntry("Fmp3",0,0)
    app.setEntryDefault("Fmp3", "Import mp3 folder")
    app.setEntryWidth("Fmp3", 60)
    app.addNamedButton("Import","BTN_1",Callback_AddMusicFolder,0,1)
    app.setButtonWidth("BTN_1", 10)
    app.setButtonHeight("BTN_1",2)
    app.addNamedButton("Open Folder","BTN_2",Callback_OpenMusicFolder,0,2)
    app.setButtonWidth("BTN_2", 10)
    app.setButtonHeight("BTN_2",2)
    
    app.addLabelScale("Vol:",0,3)
#     app.setScaleWidth("Vol:", 10)
    app.showScaleValue("Vol:", show=True)
    app.setScale("Vol:", 100*pygame.mixer.music.get_volume(),callFunction=False)
#     app.setScaleRange("Vol:",0,1,curr=pygame.mixer.music.get_volume())
    app.setScaleChangeFunction("Vol:", Callback_VolumeCtrl)
    
    app.stopFrame()#end LF_Music_folder
    app.startFrame("LF_Music_Button",1, 0)
    app.setSticky("ewns")
    bnt_title_list = ["PlayOrPause","Stop","Previous","Next","Mute"]
    app.addButtons(bnt_title_list, Callback_Button,0,0)
    for i in bnt_title_list:
        app.setButtonWidth(i, 10)
        app.setButtonHeight(i,2)
#         app.setButtonTooltip(i, "help")
        
    app.addLabel("L_song", "current song name",0,1)
    app.setLabelWidth("L_song", 30)
    app.setLabelHeight("L_song", 2)
    app.setLabelRelief("L_song", "groove")
    app.setLabelBg("L_song", "light green")
    app.stopFrame()#end LF_Music_Button
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
    
def Callback_MenuBarPlaylist(value):
    playList = ["New","New from filter","Configure Sorting","Clear","Shuffle","Repeat All","Repeat One"]
    if value == playList[0]:#"New"
        print(value)
    elif value == playList[1]:
        print(value)
    elif value == playList[2]:
        print(value)
    elif value == playList[3]:#"Clear"
        app.clearListBox("Playlists")
    elif value == playList[4]:
        print(value)
    elif value == playList[5]:
        print(value)
    elif value == playList[6]:#"Repeat One"
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
    
    pygame.mixer.init()
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
    app.stopFrame()#end sub_Frame_2
    
    app.stopFrame()#end main
    #-----------------------------------------------------------------------
    GUI_MenuBar()
    #-----------------------------------------------------------------------
    app.go()