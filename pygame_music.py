# -*- coding: cp936 -*-
import pygame,time
 
pygame.init()
# pygame.mixer.init() 
 
print("播放音乐2")
track1=pygame.mixer.music.load("F:/CloudMusic/LoveStory.mp3")
print(track1)
ret = pygame.mixer.music.play()
print(ret)
time.sleep(10)
pygame.mixer.music.stop()
 
# print("播放音乐3")
# track2=pygame.mixer.Sound("F:/CloudMusic/LoveStory.mp3")
# print(track2)