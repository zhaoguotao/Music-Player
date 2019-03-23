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
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

ScrolledTextattr = 1
SongFilenames = []
# SongTitles = []
index = 0  # current music file index
count = 0  # the numbers of music file
CurrVol = 0  # volume value


def ClearDisplay():
    app.clearTextArea("text")


#===============================================================================
# Text
# Display text in message box
#===============================================================================
def Text(text):
    global ScrolledTextattr
    app.setTextArea("text", text)
    ScrolledTextattr.see('end')


def TextwithTime(text):
    Text("[%s] %s" % (time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()), text))


def Callback_SaveMessage():
    # "message Dialog"
    save_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    text = app.getTextArea("text")
    if not text == "":
        ret = app.saveBox(title="save as...", fileName="pyMusicPlayer_log_" + save_time, \
                      fileTypes=[('txt', '*.txt'), ('all', '*')])
        if ret is not "":
            f = open(ret, 'w')
            f.write(text)
            f.close()
            app.infoBox("Info", "Log saved at: %s" % (ret))
    else:
        app.warningBox("Warning", "No content there, don't need save")


def Callback_MenuBarTools(value):
    if value == "Open program folder":
        filename = os.getcwd()
        if sys.platform == "win32":
            os.startfile(filename)
#             webbrowser.open(filename)
        else:
            # webbrowser.open(filename)
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    elif value == "Window Size":
        app_size = app.getSize()
        app.infoBox("GUI size", app_size)
    elif value == "On Top":
        ret = app.getMenuCheckBox("Tools", "On Top")
        if ret == True:
            app.configure(top=True)
        else:
            app.configure(top=False)
    elif value == "Resizable":
        ret = app.getMenuCheckBox("Tools", "Resizable")
        if ret == True:
            app.setResizable(canResize=True)
        else:
            app.setResizable(canResize=False)
    elif value == "Song Information":
        if SongFilenames:
            Text("------------Song Info----------------------\n")
            for item, value in MP3(SongFilenames[index], ID3=EasyID3).items():
                Text(str(item) + ": " + str(value) + "\n")
            SongInfo = MP3(SongFilenames[index]).info
            Text("pprint: %s\n" % (str(SongInfo.pprint())))
            Text("channels: %d\n" % SongInfo.channels)
            Text("length: %fs\n" % SongInfo.length)
            Text("mode: %d\n" % SongInfo.mode)
            Text("bitrate: %s bps\n" % SongInfo.bitrate)
            Text("bitrate_mode: %s\n" % SongInfo.bitrate_mode)
            Text("encoder_info: %s\n" % SongInfo.encoder_info)
            Text("encoder_settings: %s\n" % SongInfo.encoder_settings)
            Text("protected: %s\n" % SongInfo.protected)
            Text("sample_rate: %s Hz\n" % SongInfo.sample_rate)
            Text("sketchy: %s\n" % SongInfo.sketchy)
            Text("version: %d\n" % SongInfo.version)
            Text("--------------------------------------------\n")
    elif value == "Get Song":
        items = app.getAllListItems("Playlists")
        Text("\n--------------------------------------------\n")
        Text(SongFilenames)
        Text("\n--------------------------------------------\n")
        Text(items)
        Text("\n--------------------------------------------\n")
        print("Songs in ListBox      : ", items)
        print("Songs in SongFilenames: ", SongFilenames)


def Callback_SelectMusic():
    global index
    app.setListItemBg("Playlists", SongFilenames[index], "light gray")
    item = app.getListBox("Playlists")[0]
    index = SongFilenames.index(item)  # Update index to sync
    app.setListItemBg("Playlists", item, "red")
    try:
        pygame.mixer.music.load(item)  # load() requires filename is english
        TextwithTime("Playing: " + item + '\n')
        app.setScaleRange("music_progress", 0, MP3(item).info.length, curr=0)
        pygame.mixer.music.play()
        app.setButton("PlayOrPause", "Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: Select and play")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info', "Please add music file first")


def aboutme():
    '''
pyMusicPlayer

version: %(__version__)
Build Time: %(__BuildData__)
Auther: 赵国涛
    '''
    app.infoBox("about me", aboutme.__doc__.replace("%(__version__)", __version__).replace("%(__BuildData__)", __BuildData__))


def Web_me():
    webbrowser.open("http://www.baidu.com")


def Callback_AddMusicFolder():
    global count
    global index
    logging.info("Execute cmd: Open music folder")
    Fmusic = app.directoryBox(title="Open Music Folder...")
    if not Fmusic == None:
        TextwithTime("Load music folder: " + Fmusic + '\n')
        count = 0
        index = 0
        del SongFilenames[:]
#         del SongTitles[:]
        # os.chdir(Fmusic)
        for  files in os.listdir(Fmusic):
            try:
                if files.endswith(".mp3"):
                    realdir = os.path.join(Fmusic, files)  # os.path.realpath(files)  # F:\CloudMusic\Anesthesia.mp3
#                     SongTitles.append(ID3(realdir)['TIT2'].text[0])
                    SongFilenames.append(realdir)
            except Exception as e:
                logging.error(e)

        if SongFilenames == [] :
            app.infoBox('Info', "No songs found")
        else:
            app.setEntry("Fmp3", Fmusic)
            app.clearListBox("Playlists")
            for i in SongFilenames:
                count = count + 1
                # app.addListItem("Playlists", os.path.split(i)[1])
                app.addListItem("Playlists", i)
            pygame.mixer.init()
            pygame.mixer.music.load(SongFilenames[0])
            TextwithTime("Playing: " + SongFilenames[0] + '\n')
            app.setScaleRange("music_progress", 0, MP3(SongFilenames[index]).info.length, curr=0)
            pygame.mixer.music.play()
            app.setListItemBg("Playlists", SongFilenames[index], "red")
            app.setButton("PlayOrPause", "Play")  # Update button state
            Callback_DisplayCurrentSong("Playing...")
    else:
        return 1


def Callback_AddMusicFile():
    fname = app.openBox("Open Music file...", fileTypes=[('MP3', '*.mp3'), ('all', '*')])
    if not fname == "":
        Text("==============\n")
        Text(fname + '\n')
        Text("==============\n")

        if os.path.exists(fname):
            if os.path.isfile(fname):
                if fname.endswith(".mp3"):
                    app.addListItem("Playlists", fname)
        else:
            TextwithTime(fname + ' : The file(folder) does not exist\n')


def Callback_DisplayCurrentSong(state):
    global index
    app.setLabel("L_song", os.path.split(SongFilenames[index])[1] + "[%s]" % (state))


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
        if ret == 1:  # not stop
            if but_state == "Pause":
                app.setButton("PlayOrPause", "Play")
                Callback_DisplayCurrentSong("Playing...")
                if ret == 1:
                    logging.info("Execute cmd: unpause")
                    pygame.mixer.music.unpause()
                    TextwithTime("Unpaused: " + SongFilenames[index] + '\n')
                else:
                    logging.info("Execute cmd: play")
                    pygame.mixer.music.play()
                    TextwithTime("Play: " + SongFilenames[index] + '\n')
            else:
                app.setButton("PlayOrPause", "Pause")
                Callback_DisplayCurrentSong("Paused...")
                logging.info("Execute cmd: pause")
                pygame.mixer.music.pause()
                TextwithTime("Paused: " + SongFilenames[index] + '\n')
        else:  # if song is stopped, replay
            app.setButton("PlayOrPause", "Play")
            Callback_DisplayCurrentSong("Playing...")
            logging.info("Execute cmd: play")
            pygame.mixer.music.play()
            TextwithTime("Play: " + SongFilenames[index] + '\n')
    except Exception as e:
        logging.error(e)
        app.infoBox('Info', "Please add music file first")


def Callback_Stop():
    try:
        pygame.mixer.music.stop()
        Callback_DisplayCurrentSong("Stopped...")
        TextwithTime("Stoped: " + SongFilenames[index] + '\n')
        app.setScale("music_progress", 0, callFunction=False)
        app.setButton("PlayOrPause", "Play")
        logging.info("Execute cmd: stop")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info', "Please add music file first")


def Callback_Previous():
    global index
    app.setListItemBg("Playlists", SongFilenames[index], "light gray")
    index -= 1
    try:
        if index < 0:
            index = count - 1
        pygame.mixer.music.load(SongFilenames[index])
        TextwithTime("Playing: " + SongFilenames[index] + '\n')
        app.setScaleRange("music_progress", 0, MP3(SongFilenames[index]).info.length, curr=0)
        pygame.mixer.music.play()
        app.setListItemBg("Playlists", SongFilenames[index], "red")
        app.setButton("PlayOrPause", "Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: Previous and play")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info', "Please add music file first")


def Callback_Next():
    global index, count
    app.setListItemBg("Playlists", SongFilenames[index], "light gray")
    index += 1
    if index > count - 1:
        index = 0
    try:
        pygame.mixer.music.load(SongFilenames[index])  # load() requires filename is english
        TextwithTime("Playing: " + SongFilenames[index] + '\n')
        app.setScaleRange("music_progress", 0, MP3(SongFilenames[index]).info.length, curr=0)
        pygame.mixer.music.play()
        app.setListItemBg("Playlists", SongFilenames[index], "red")
        app.setButton("PlayOrPause", "Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: next and play")
    except Exception as e:
        logging.error(e)
        app.infoBox('Info', "Please add music file first")


def Callback_VolumeMute():
    global CurrVol
    if app.getButtonBg("Mute") == "gray":  # no mute
        try:
            CurrVol = app.getScale("Vol:")
            app.setScale("Vol:", 0, callFunction=False)
            pygame.mixer.music.set_volume(0)
            app.setButtonBg("Mute", "red")
            logging.info("Execute cmd: volume set to 0(mute)")
        except Exception as e:
            logging.error(e)
    else:
        try:
            app.setScale("Vol:", CurrVol, callFunction=False)
            vol = float(CurrVol) / 100
            pygame.mixer.music.set_volume(vol)
            app.setButtonBg("Mute", "gray")
            logging.info("Execute cmd: volume set: %f" % (vol))
        except Exception as e:
            logging.error(e)


def Callback_VolumeCtrl():
    global CurrVol
    try:
        CurrVol = app.getScale("Vol:")
        vol = float(CurrVol) / 100
        pygame.mixer.music.set_volume(vol)
        if vol == 0:
            app.setButtonBg("Mute", "red")
        else:
            app.setButtonBg("Mute", "gray")
        logging.info("Execute cmd: volume set: %f" % (vol))
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
    f_path = app.getEntry("Fmp3")
    if f_path == "":
        app.warningBox("Warning", "Import mp3 folder first")
        return -1
    try:
        webbrowser.open(f_path)
    except Exception as e:
        app.warningBox("Warning", e)
        logging.error(e)


def Callback_ChangeMusicPos():
    get_busy = Callback_MusicState()
    if get_busy:
        pos = app.getScale("music_progress")
        pygame.mixer.music.rewind()  # 重新开始播放音乐
        ret = pygame.mixer.music.set_pos(pos)
        but_state = app.getButton("PlayOrPause")
        if but_state == "Pause":
            app.setButton("PlayOrPause", "Play")
            logging.info("Execute cmd: unpause")
            pygame.mixer.music.unpause()
            TextwithTime("Unpaused: " + SongFilenames[index] + '\n')
        logging.info("Set pos: " + str(pos) + 's')
    else:
        app.setScale("music_progress", 0, callFunction=False)


def updateSong():
    get_busy = Callback_MusicState()
    if get_busy:
        # pygame.mixer.music.get_pos()此函数会获得音乐的播放时长（以毫秒为单数的数值）。返回值仅代表已经音乐已经播放了多久，并不考虑任何起始位置偏移量。
        curr_pos = pygame.mixer.music.get_pos()
        but_state = app.getButton("PlayOrPause")
        if but_state == "Pause":
            Callback_DisplayCurrentSong("Paused at %.2fs" % (curr_pos / 1000.0))
        else:
            Callback_DisplayCurrentSong("Playing...%.2fs" % (curr_pos / 1000.0))
            # app.setScale("music_progress", round(curr_pos/1000.0,2), callFunction=False)
    else:
        if SongFilenames:  # not none
            # print("SongFilenames:",SongFilenames)
            Callback_DisplayCurrentSong("Stopped...")


#-----------GUI------------
def GUI_LabelFrame_Music():
    app.startFrame("LF_Music", 0, 0)
    app.setSticky("ewn")
    app.startFrame("LF_Music_folder", 0, 0)
    app.setSticky("ewns")
    app.addEntry("Fmp3", 0, 0)
    app.setEntryDefault("Fmp3", "Import mp3 folder")
    app.setEntryWidth("Fmp3", 60)
    app.addNamedButton("Import", "BTN_1", Callback_AddMusicFolder, 0, 1)
    app.setButtonWidth("BTN_1", 10)
    app.setButtonHeight("BTN_1", 2)
    app.addNamedButton("Open Folder", "BTN_2", Callback_OpenMusicFolder, 0, 2)
    app.setButtonWidth("BTN_2", 10)
    app.setButtonHeight("BTN_2", 2)
    app.addLabelScale("Vol:", 0, 3)
#     app.setScaleWidth("Vol:", 10)
    app.showScaleValue("Vol:", show=True)
    app.setScale("Vol:", 100 * pygame.mixer.music.get_volume(), callFunction=False)
    app.setScaleChangeFunction("Vol:", Callback_VolumeCtrl)
    app.stopFrame()  # end LF_Music_folder

    app.startFrame("LF_Music_Button", 1, 0)
    app.setSticky("ewns")
    bnt_title_list = ["PlayOrPause", "Stop", "Previous", "Next", "Mute"]
    app.addButtons(bnt_title_list, Callback_Button, 0, 0)
    for i in bnt_title_list:
        app.setButtonWidth(i, 10)
        app.setButtonHeight(i, 2)
        app.setButtonBg(i, "gray")
    app.addLabel("L_song", "current song name", 0, 1)
    app.setLabelWidth("L_song", 40)
    app.setLabelHeight("L_song", 2)
    app.setLabelRelief("L_song", "groove")
    app.setLabelBg("L_song", "light green")
#     app.setPollTime(200)  # 0.2s
    app.registerEvent(updateSong)
    app.stopFrame()  # end LF_Music_Button
    app.startFrame("LF_Music_progress", 2, 0)
    app.setSticky("ewns")
    app.addScale("music_progress", 0, 0)
    app.showScaleValue("music_progress", show=True)
    app.setScaleRange("music_progress", 0, 240, curr=0)
    app.showScaleIntervals("music_progress", 25)
    app.setScaleChangeFunction("music_progress", Callback_ChangeMusicPos)
    app.stopFrame()  # end LF_Music_progress
    app.stopFrame()  # end LF_Music


def GUI_LabelFrame_Left():
    app.startScrollPane("Playlists", 0, 0)
    app.setSticky("ewns")
    app.startFrame("LF_left", 0, 0)
    app.setSticky("ewns")
    app.addListBox("Playlists", [], 0, 0)
    app.setListBoxHeight("Playlists", 25)
    app.setListBoxWidth("Playlists", 60)
    app.setListBoxBg("Playlists", "light gray")
    app.bindKey("<Double-Button-1>", Callback_SelectMusic)
    app.stopFrame()
    app.stopScrollPane()  # end


def GUI_LabelFrame_Mid():
    global ScrolledTextattr
    app.startLabelFrame("Info", 0, 1, label="Info")
#     app.setLabelFrameWidth("Info", 800)
    app.setSticky("ewn")
    ScrolledTextattr = app.addScrolledTextArea("text", 0, 0, colspan=2)
    app.setTextAreaHeight("text", 25)
    app.setTextAreaWidth("text", 40)
    app.setTextAreaFont("text", size=7, family="Verdana", slant="roman")
    Text("--------[Launch Information]---------\n")
    Text("Launch time: %s\n" % (time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())))
    Text(gui.SHOW_VERSION() + '\n')
    Text("Program path: %s\n" % (os.getcwd()))
    Text("--------------------------------------\n")
    app.startFrame("message_btn", 1, 0)
    app.addButton("Clear message", ClearDisplay, 1, 0)
    app.setButtonWidth("Clear message", 12)
    app.addButton("Save message as...", Callback_SaveMessage, 1, 1)
    app.setButtonWidth("Save message as...", 12)
    app.stopFrame()
    app.stopLabelFrame()


def Callback_MenuBarPlaylist(value):
    playList = ["New", "New from filter", "Configure Sorting", "Clear", "Shuffle", "Repeat All", "Repeat One"]
    if value == playList[0]:  # "New"
        print(value)
    elif value == playList[1]:
        print(value)
    elif value == playList[2]:
        print(value)
    elif value == playList[3]:  # "Clear"
        app.clearListBox("Playlists")
    elif value == playList[4]:
        print(value)
    elif value == playList[5]:
        print(value)
    elif value == playList[6]:  # "Repeat One"
        print(value)


def GUI_MenuBar():
    app.addMenuItem("Music", "Add music folder...", Callback_AddMusicFolder, shortcut="Control-o")
    app.addMenuItem("Music", "Add music file...", Callback_AddMusicFile, shortcut="Control-j")
    app.addMenuSeparator("Music")
    app.addMenuItem("Music", "Quit", app.stop, shortcut="Control-q")
    #-----------------------------------------------------------------------
    app.addMenuList("Playlist", ["New", "New from filter", "-", "Configure Sorting", "Clear", "Shuffle"], Callback_MenuBarPlaylist)
    app.addMenuSeparator("Playlist")
    app.addMenuCheckBox("Playlist", "Repeat All", Callback_MenuBarPlaylist)
    app.addMenuCheckBox("Playlist", "Repeat One", Callback_MenuBarPlaylist)
    #-----------------------------------------------------------------------
    app.addMenuList("Tools", ["Open program folder", "Song Information", "Get Song"], Callback_MenuBarTools)
    app.addMenuSeparator("Tools")
    app.addMenuItem("Tools", "Window Size", Callback_MenuBarTools)
    app.addMenuCheckBox("Tools", "On Top", Callback_MenuBarTools)
    app.addMenuCheckBox("Tools", "Resizable", Callback_MenuBarTools)
    res = app.getResizable()
    if res == True:
        app.setMenuCheckBox("Tools", "Resizable")
    on_top = app.getOnTop()
    if on_top == True:
        app.setMenuCheckBox("Tools", "On Top")
    #-----------------------------------------------------------------------
    app.addMenuItem("Help", "About", aboutme)
    app.addMenuItem("Help", "Web Link", Web_me)


if __name__ == '__main__':
    __version__ = "v0.02"  # define the version for tool
    __BuildData__ = "2019.3.23"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s  %(module)s(%(lineno)d):  %(message)s')

    pygame.mixer.init()
    app = gui("pyMusicPlayer %s" % (__version__))
    app.setSize("940x488")
    app.setFont(size=10, family="Verdana", slant="roman")
    try:
        app.setIcon("pymusic.ico")  # linux doesn't support this property
    except Exception as e:
        logging.error(e)
        pass
    app.setSticky("ewns")
    #-----------------------------------------------------------------------
    app.startFrame("main", 0, 0)
    app.setSticky("ewns")

    app.startFrame("sub_Frame_1", 0, 0)
    GUI_LabelFrame_Music()
    app.stopFrame()  # end sub_Frame_1

    app.startFrame("sub_Frame_2", 1, 0)
    app.setSticky("ewns")
    GUI_LabelFrame_Left()
    GUI_LabelFrame_Mid()
    app.stopFrame()  # end sub_Frame_2

    app.stopFrame()  # end main
    #-----------------------------------------------------------------------
    GUI_MenuBar()
    #-----------------------------------------------------------------------
    app.go()
