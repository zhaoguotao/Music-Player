#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mutagen.mp3 import MP3
import mutagen.id3
from mutagen.easyid3 import EasyID3

def print_id3(id3):
    print()
    print('%-13s\t%s' % ('Field', 'Value'))
    print('-' * 70)
    for k, v in id3info.items():
        print('%-13s\t%s' % (k, v and v[0]))
    print('-' * 70)

if __name__ == '__main__':
    id3info = MP3("F:/CloudMusic/By my side.mp3", ID3=EasyID3)
    print(id3info)
    print_id3(id3info)
    '''
    # change the title.
    print("# change the title..............")
    old_title = id3info['title']
    id3info['title'] = u'Love_Story'
    id3info.save()
    print_id3(id3info)

    # change the title back.
    print("# change the title back...............")
    id3info['title'] = old_title
    id3info.save()
    print_id3(id3info)
    '''