import os
import glob
import threading
import queue
import time
import pandas as pd
from random import randint
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


from pygame import mixer

root = tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("plastik")         # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 12')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    """
    Finds all files in the directory chosen by the user
    """
    global filename_path
    filename_path = filedialog.askdirectory()
    x = ''
    index = 0

    songs_list = pd.DataFrame(columns = ['ID', 'Path'])
    for x in glob.glob(filename_path + '/*.mp3'):
        add_to_playlist(x, index)
        songs_list.loc[index] = [index, x]
        index +=1
    for x in glob.glob(filename_path + '/**/*.mp3'):
        add_to_playlist(x, index)
        songs_list.loc[index] = [index, x]
        index +=1

    print ('PLAYLIST DONE')
    print (x)
    mixer.music.queue(x)
    songs_list.to_csv('song_data.csv', index = False)

def add_to_playlist(filename_path, index):
    """
    Adds a file to the playlist

    Args:

    filename_path : path to the music file to be added to the playlist
    index : index of the entry in the playlist
    """
    
    print ()
    filename = os.path.basename(filename_path)
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)


mixer.init()  # initializing the mixer

root.title("Melody")
#root.iconbitmap(r'images/melody.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

bottomframe = Frame(rightframe)
bottomframe.pack()

titlelabel = ttk.Label(topframe, text = '')
titlelabel.pack(pady = 5)

artistlabel = ttk.Label(topframe, text = '')
artistlabel.pack(pady = 5)

currenttimelabel = ttk.Label(topframe, text=' --:--', relief=GROOVE)
currenttimelabel.pack()


song_run_time = 0
selected_song = 0
skipped = False

def show_details(play_song):
    """
    Displays the details of the currently playing song on the screen

    Args:
    play_song : the music file currently being played
    
    """
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    audio = EasyID3(play_song)
    title = audio['title'][0]
    artist = audio['artist'][0]
    album = audio['album'][0]
    
    titlelabel['text'] = title
    artistlabel['text'] = artist + ' - ' + album

    
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    

def start_count(t):
    """
    Time counter for display of current time on the screen

    Args:
    t : total length of the song in seconds
    
    """
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0

    mins, secs = divmod(t, 60)
    mins = round(mins)
    secs = round(secs)
    totaltimeformat = '{:02d}:{:02d}'.format(mins, secs)
    print ('total time : ', t)
    print (mixer.music.get_busy())
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = timeformat + ' / ' + totaltimeformat
            time.sleep(1)
            if current_time<=25:
                global song_run_time
                song_run_time = current_time
            current_time += 1
    
    mins, secs = divmod(current_time, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    currenttimelabel['text'] = timeformat + ' / ' + totaltimeformat
    
    print (current_time)
    print (song_run_time)


def play_music():
    """
    Plays the music
    """
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        
            try:
                '''
                SONG_END = pygame.USEREVENT + 1

                pygame.mixer.music.set_endevent(SONG_END)
                '''
                stop_music()
                time.sleep(1)
                global skipped
                if skipped == False:
                    select = playlistbox.curselection()
                    global selected_song
                    selected_song = int(select[0])
                skipped = False
                print ('selected song : ', selected_song)
                playlistbox.selection_clear(0, END)
                playlistbox.selection_set(selected_song)
                play_it = playlist[selected_song]
                mixer.music.load(play_it)
                
                mixer.music.play()
                print ('pos', mixer.music.get_pos())
                statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
                '''
                while True:
                    for event in pygame.event.get():        
                        if event.type == SONG_END:
                            print("the song ended!")
                            break
                '''
                show_details(play_it)

                print ('completed')
            except:
                tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    """
    Stops music play
    """
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    """
    Pauses the currently playing song
    """
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def skip_music():
    """
    Goes to the next song queued
    """
    mixer.music.stop()
    print ('skipped')
    global skipped
    skipped = True
    global selected_song
    print ('1 : ', selected_song)
    selected_song = randint(0, len(playlist))
    print ('2 : ', selected_song)
    statusbar['text'] = "Music skipped"
    play_music()


def set_vol(val):
    """
    Sets the volume of music play

    Args:

    val : value of volume to be set
    """
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    """
    Mutes the song if it is unmuted, and unmutes it if it is muted
    """
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

nextPhoto = PhotoImage(file='images/next.png')
nextBtn = ttk.Button(bottomframe, image=nextPhoto, command=skip_music)
nextBtn.grid(row=0, column=0, padx = 10)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1, padx = 10)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    """
    Closes the player
    """
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
