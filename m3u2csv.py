# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:26:46 2016

@author: behinger
"""

import os
#from pandas import DataFrame,concat
from glob import glob

#import re
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp4 import MP4
from chardet import detect
from io import open as open
def parse_m3u_musicbee(infile,encoding="auto"):
    try:
        if encoding=="auto":
            rawdata = open(infile,'rb').read()
            result = detect(rawdata)
            encoding = result['encoding']
        
            print('Confidence for automatic encoding detection is',result["confidence"],':',encoding)
        inf = open(infile,'r', encoding=encoding)
       
        # initialize playlist variables before reading file
        playlist=[]
    
        
        for line in inf:
            line=line.strip()
            if "#EXTM3U" in line:
                continue
            
            # if we find a line with #extinf we skip :)
            if "#EXTINF" in line:
                continue
            line=line.replace("file://","")      
            playlist.append(line)
    
        inf.close()
    except UnicodeEncodeError as e:
        if encoding!="UTF-8":
            print("unicodeEncodeError, trying as UTF-8")
            playlist = parse_m3u_musicbee(infile,encoding="UTF-8")
        else:
            raise(e)
    
    return playlist

def parse_path_list(playlist):
   
    df = dict(artist=[],title=[],genre=[],length=[],year=[],album=[],origName=[])
    for song in playlist:        
        try:
            extension = os.path.splitext(song)[1]

            if extension == '.m4a':
                tmpMP4 = MP4(song)
                length = tmpMP4.info.length
                a = {}
                a["artist"] = tmpMP4['\xa9ART'][0]
                a["title"] = tmpMP4['\xa9nam'][0]                
                a["genre"] = tmpMP4['\xa9gen'][0]
                try:
                    a["date"]  = tmpMP4['\xa9day'][0]
                except:
                    pass
                try:
                    a["album"] = tmpMP4['\xa9alb'][0]
                except:
                    pass
            elif extension == '.ogg':
                a = OggVorbis(song)
                length = a.info.length
            else:
                a = EasyID3(song)
                b = MP3(song)
                
                length = b.info.length
            try:
                artist = a["artist"][0]
            except KeyError:
                artist = 'unknown'
            try:
                title = a["title"][0]
            except KeyError:
                title= 'unknown'
            try:
                genre = a["genre"][0]
            except KeyError:
                genre= 'unknown'
            
            try:
                year = a["date"][0]
            except KeyError:
                year = 'unknown'
            try:
                album= a["album"][0]
            except KeyError:
                album = "unknown"
           # if length < 60:
           #     genre = 'cortina'
            df["artist"].append(artist)
            df["title"].append(title)
            df["genre"].append(genre)
            df["length"].append(length)
            df["year"].append(year)
            df["album"].append(album)
            df["origName"].append('"'+song+'"')
                
        except (OSError, IOError) as e:
            [df[k].append("NA") for k in df.keys()]
            try:
                print("Could not find or access file: " + song)
                df['origName'][-1] = song
            except:
                print("File not found, cannot display which one")                            

            
        except ID3NoHeaderError:
            print("Could not find ID3 Tag for file: " + song)
            [df[k].append("NA") for k in df.keys()]
            df['origName'][-1] = song
            
        except Exception as e:
            print("an unknown error occured:" + e)
            
    df["number"]=list(range(len(df["artist"])))
    return df
    
try:
    #from tkinter import filedialog
    #allPlaylists = filedialog.askopenfilenames(defaultextension="m3u")
    import easygui
    allPlaylists = easygui.fileopenbox(default="*.m3u",filetypes=["*.m3u"],multiple=True)
    #allPlaylists = glob(r'./m3u/*.m3u')
    df = dict(artist=[],title=[],genre=[],length=[],year=[],album=[],origName=[],identification=[],number=[])
    text = 'Trying to read %d playlist(s) \n' %len(allPlaylists)
    print(text)
    #tandaIdx = 0
    for pl in allPlaylists:
        playlist = parse_m3u_musicbee(pl)
        playlist[0] = playlist[0].replace(u'\ufeff', '') #happens for some decoding schemes.
        dfsingle = parse_path_list(playlist)
        #dfsingle = add_tandas.add_tandas(dfsingle)
        dfsingle["identification"] = ['"'+pl+'"']*len(dfsingle["artist"])
        #dfsingle["tanda"] = dfsingle["tanda"]+tandaIdx
        
        for k in dfsingle.keys():
            df[k] = df[k] + dfsingle[k]
        
        text = 'Playlist %s successfull \n' %pl
        print(text)
        
    
    from csv import writer
    import time
    

#    with os.fdopen(os.open(time.strftime("%Y-%m-%d_%H-%M-%S")+'_output.csv',os.O_CREAT | os.O_RDWR ),'w') as myfile:
    with open(time.strftime("%Y-%m-%d_%H-%M-%S")+'_output.csv','w',encoding="utf-8") as myfile:
        curr_writer = writer(myfile,lineterminator='\n')
        curr_writer.writerow(df.keys())
        for r in range(len(df["artist"])):
            curr_writer.writerow([df[out][r] if isinstance(df[out][r],str) else df[out][r] for out in df.keys()])
    input("Finished... press ENTER to continue")
except Exception as e:
    try:
     from sys import exc_info
     exc_type, exc_obj, exc_tb = exc_info()
     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
     print(exc_type, fname, "line_no:", exc_tb.tb_lineno)
     print(e)
    except:
     pass
    input('an Error occured, please send the m3u and the errorcode to tango@benediktehinger.de - press ENTER to abort')
