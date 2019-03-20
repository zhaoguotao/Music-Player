#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pygame.mixer.music.load()  ——  载入一个音乐文件用于播放
pygame.mixer.music.play()  ——  开始播放音乐流
pygame.mixer.music.rewind()  ——  重新开始播放音乐
pygame.mixer.music.stop()  ——  结束音乐播放
pygame.mixer.music.pause()  ——  暂停音乐播放
pygame.mixer.music.unpause()  ——  恢复音乐播放
pygame.mixer.music.fadeout()  ——  淡出的效果结束音乐播放
pygame.mixer.music.set_volume()  ——  设置音量
pygame.mixer.music.get_volume()  ——  获取音量
pygame.mixer.music.get_busy()  ——  检查是否正在播放音乐
pygame.mixer.music.set_pos()  ——  设置播放的位置
pygame.mixer.music.get_pos()  ——  获取播放的位置
pygame.mixer.music.queue()  ——  将一个音乐文件放入队列中，并排在当前播放的音乐之后
pygame.mixer.music.set_endevent()  ——  当播放结束时发出一个事件
pygame.mixer.music.get_endevent()  ——  获取播放结束时发送的事件
'''

import os
import pygame
from mutagen.id3 import ID3
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askdirectory
import logging

SongFilenames=[]
SongTitles = []
index=0#current music file index
count=0#the numbers of music file

def Callback_DisplayCurrentSong(state):
    global index
    SongName.set(SongFilenames[index]+"[%s]"%(state))

def Callback_MusicState():
    '''
    0: song is stopped or not play
    1: song is playing
    '''
    ret = pygame.mixer.music.get_busy()
    return ret

def Callback_PlayOrPause():
    try:
        but_state = button_text.get()
        ret = pygame.mixer.music.get_busy()
        if ret == 1:#not stop
            if but_state == "Pause":
                button_text.set("Play")
                Callback_DisplayCurrentSong("Playing...")
                if ret == 1:
                    logging.info("Execute cmd: unpause")
                    pygame.mixer.music.unpause()
                else:
                    logging.info("Execute cmd: play")
                    pygame.mixer.music.play()
            else:
                button_text.set("Pause")
                Callback_DisplayCurrentSong("Paused...")
                logging.info("Execute cmd: pause")
                pygame.mixer.music.pause()
        else:#if song is stopped, replay
            button_text.set("Play")
            Callback_DisplayCurrentSong("Playing...")
            logging.info("Execute cmd: play")
            pygame.mixer.music.play()
    except Exception as e:
        logging.error(e)
        tkinter.messagebox.showinfo(title='Info',message="Please add music file first")

def Callback_Next():
    global index,count
    index += 1
    if index > count -1:
        index = 0
    try:
        pygame.mixer.music.load(SongFilenames[index])#load() requires filename is english
        pygame.mixer.music.play()
        button_text.set("Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: next and play")
    except Exception as e:
        logging.error(e)
        tkinter.messagebox.showinfo(title='Info',message="Please add music file first")
    
def Callback_Previous():
    global index
    index -= 1
    try:
        if index < 0:
            index = count-1
        pygame.mixer.music.load(SongFilenames[index])
        pygame.mixer.music.play()
        button_text.set("Play")
        Callback_DisplayCurrentSong("Playing...")
        logging.info("Execute cmd: Previous and play")
    except Exception as e:
        logging.error(e)
        tkinter.messagebox.showinfo(title='Info',message="Please add music file first")

def Callback_Stop():
    try:
        pygame.mixer.music.stop()
        Callback_DisplayCurrentSong("Stopped...")
        logging.info("Execute cmd: stop")
    except Exception as e:
        logging.error(e)
        tkinter.messagebox.showinfo(title='Info',message="Please add music file first")

def Callback_OpenMusicFolder():
    global count
    global index
    logging.info("Execute cmd: Open music folder")
    directory = askdirectory()
    if(directory):
        count=0
        index=0
        del SongFilenames[:]
        del SongTitles[:]
        os.chdir(directory)
        for  files in os.listdir(directory):
            try:
                if files.endswith(".mp3"):
                    realdir = os.path.realpath(files)#F:\CloudMusic\Anesthesia.mp3
                    SongTitles.append(ID3(realdir)['TIT2'].text[0])
                    SongFilenames.append(files)
            except Exception as e:
                logging.error(e)
                
        if SongFilenames == [] :
            tkinter.messagebox.showinfo(title='Info',message="No songs found")
        else:
            FolderName.set(directory)
            listbox.delete(0, END)
            '''
            SongTitles.reverse()#该方法没有返回值，但是会对列表的元素进行反向排序
             for items in SongTitles:
                listbox.insert(0, items)
            '''
            for i in SongFilenames:
                count = count + 1
                listbox.insert(0, i)
            SongFilenames.reverse()#listbox会把顺序颠倒，所以这里对列表的元素进行反向排序
            pygame.mixer.init()
            pygame.mixer.music.load(SongFilenames[0])
            pygame.mixer.music.play()
            button_text.set("Play")#Update button state
            Callback_DisplayCurrentSong("Playing...")
    else:
        return 1

def Callback_VolumeCtrl():
    try:
        pygame.mixer.music.set_volume(10)
        logging.info("Execute cmd: volume set")
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(name)s  %(levelname)s  %(module)s(%(lineno)d):  %(message)s')
    
    top = Tk()
    top.wm_title("MP3 Player")
    top.minsize(550,500)
    
    pygame.mixer.init()
    #music folder 
    FolderName =StringVar()
    FolderName.set("music folder is in here")
    Folderlabel =Label(top,textvariable=FolderName,width=80,bg='light gray',relief=GROOVE)
    Folderlabel.pack()
    #Song lists
    listbox=Listbox(top,selectmode=MULTIPLE,width=100,height=20,bg="grey",fg="black")
    listbox.pack(fill=X)
    #song name title and state
    SongName =StringVar()
    songlabel =Label(top,textvariable=SongName,width=80,bg='light green',relief=GROOVE)
    songlabel.pack()
    #---button------------------------------------------------
    Frame_Button =Frame(top,width=400,height=300)
    Frame_Button.pack()
    button_text=StringVar()
    button_text.set("Play")
    playbutton = Button(Frame_Button,text="Play",textvariable=button_text,width=12,command = Callback_PlayOrPause)
    playbutton.pack(side=LEFT)
    stopbutton = Button(Frame_Button,text="Stop",width=12,command = Callback_Stop)
    stopbutton.pack(side=LEFT)
    previousbutton = Button(Frame_Button,text="Previous",width=12,command = Callback_Previous)
    previousbutton.pack(side=LEFT)
    nextbutton = Button(Frame_Button,text="Next",width=12,command = Callback_Next)
    nextbutton.pack(side=LEFT)
    mutebutton = Button(Frame_Button,text="Mute",width=12,command = Callback_VolumeCtrl)
    mutebutton.pack(side=LEFT)
    
    #　创建一个菜单栏，这里我们可以把它理解成一个容器，在窗口的上方
    menubar = Menu(top)
    #　定义一个空的菜单单元
    filemenu = Menu(menubar, tearoff=0)  # tearoff意为下拉
    #　将上面定义的空菜单命名为`File`，放在菜单栏中，就是装入那个容器中
    menubar.add_cascade(label='File', menu=filemenu)
    #　在`文件`中加入`新建`的小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
    #　如果点击这些单元, 就会触发`None`的功能
    filemenu.add_command(label='Add music folder...', command=Callback_OpenMusicFolder)
    filemenu.add_command(label='Add music file...', command=None)
    # 分隔线
    filemenu.add_separator()
    filemenu.add_command(label='Quit', command=top.quit)
    '''
            #在‘文件’下拉菜单中创建二级菜单
    submenu = Menu(filemenu) 
    filemenu.add_cascade(label='导入', menu=submenu, underline=0)
    submenu.add_command(label='导入图片', command=None)
    '''
    # Create help menubar
    HelpMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=HelpMenu)
    HelpMenu.add_command(label='About', command=None)
     
    top.config(menu=menubar)  # 加上这代码，才能将菜单栏显示
    top.mainloop()
