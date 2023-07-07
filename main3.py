from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import tkinter.font as font
import pygame.mixer as mixer
from mutagen.mp3 import MP3
import os
import threading
import pickle
import time

# Initializing the mixer
mixer.init()
songsinsideplaylist=[]
default_database_directory_path = "./database"
default_playlist_directory_path="./playlist"
listofsongs = []

def play_song(song_name: StringVar,songs_list, status: StringVar):
    def arrange_list(user_position, my_list):
        if user_position < 1 or user_position > len(my_list):
            return None  # Invalid user position

        part = [my_list[user_position]]
        part1 = my_list[user_position + 1:]
        part2 = my_list[:user_position]
        arranged_list = part + part1 + part2
        return arranged_list

    def is_song_playing():
        return mixer.music.get_busy()

    def play_song_thread():
        global queuelength
        global songstatus
        global currentpos
        global current_pos
        while queuelength > 0 and songstatus==1:
            mixer.music.load(queue[0])
            song_name.set(queue[0])
            if currentpos==0:
                mixer.music.play()
            elif currentpos!=0:
                mixer.music.play(start=currentpos)
            status.set("Song PLAYING")
            while mixer.music.get_busy():
                songname = MP3(queue[0])
                current_pos = mixer.music.get_pos() / 1000
                song_length = songname.info.length
                if current_pos >= song_length:
                    x=queue.pop(0)
                    playedqueue.append(x)
                    playedqueue.reverse()
                    current_pos=0
                    break
            queuelength = len(queue)

    global listofsongs
    global queue
    global queuelength
    global queuelistbox
    global playedqueue
    global currentindex
    global songstatus
    songstatus=1

    current_index = songs_list.curselection()
    if queue == [] or currentindex!=current_index:
        queuelistbox.delete(0, END)
        current_index = songs_list.curselection()
        currentindex=current_index
        if current_index == ():
            for i in listofsongs:
                queuelistbox.insert(END, i)
                queue.append(i)
        elif current_index[0] != 0:
            queue = arrange_list(current_index[0], listofsongs)
            for j in queue:
                queuelistbox.insert(END, j)
        elif current_index[0] == 0:
            for i in listofsongs:
                queue.append(i)
                queuelistbox.insert(END, i)
    else:
        pass

    queuelength = len(queue)
    print(queue)
    threading.Thread(target=play_song_thread).start()

def stop_song(status: StringVar):
    global songstatus
    global currentpos
    currentpos=0
    songstatus=0
    mixer.music.stop()
    status.set("Song STOPPED")

def load(listbox):
    global listofsongs
    global lengthoflist
    global default_database_directory_path
    global queue
    queue=[]
    listofsongs=[]
    stop_song(song_status)
    os.chdir(default_database_directory_path)
    listbox.delete(0, END)
    tracks = os.listdir()
    for track in tracks:
        if track.endswith(".mp3"):
            listofsongs.append(track)
            listbox.insert(END, track)
    lengthoflist = len(listofsongs)


def pause_song(status: StringVar):
    global songstatus
    global current_pos
    global currentpos
    currentpos=current_pos
    songstatus=0
    mixer.music.pause()
    status.set("Song PAUSED")

def resume_song(status: StringVar):
    global songstatus
    songstatus=0
    mixer.music.unpause()
    status.set("Song RESUMED")

def next_song(current_song, songs_list, song_status):
    global queue
    global playedqueue
    global songstatus
    global currentpos
    global queuelistbox
    currentpos=0
    songstatus=0
    mixer.music.stop()
    x=queue.pop(0)
    playedqueue.append(x)
    playedqueue.reverse()
    queuelistbox.delete(0, END)
    for j in queue:
        queuelistbox.insert(END, j)
    print(playedqueue)
    play_song(current_song,playlist, song_status)

def previous_song(current_song, songs_list, song_status):
    global queue
    global playedqueue
    global songstatus
    global currentpos
    global queuelistbox
    currentpos=0
    songstatus=0
    mixer.music.stop()
    try:
        x=playedqueue.pop(0)
        queue.reverse()
        queue.append(x)
        queue.reverse()
        queuelistbox.delete(0, END)
        for j in queue:
            queuelistbox.insert(END, j)
        play_song(current_song,playlist, song_status)
    except:
        pass

class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class PlaylistManager:
    global songsinsideplaylist
    def __init__(self):
        self.start = None
        self.top = None

    def create(self, playlist_name):
        self.start = Node(playlist_name)
        self.top = None

    def add_node(self, song):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        current = self.start
        while current.next is not None:
            current = current.next

        new_node = Node(song)
        new_node.prev = current
        current.next = new_node
        messagebox.showinfo("Success", "Song added successfully.")

    def delete_node(self, song):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        current = self.start
        while current is not None:
            if current.song == song:
                if current.prev is None:
                    self.start = current.next
                else:
                    current.prev.next = current.next
                    if current.next is not None:
                        current.next.prev = current.prev
                messagebox.showinfo("Success", "Song deleted successfully.")
                return
            current = current.next

        messagebox.showwarning("Not Found", "Song not found in the playlist.")

    def display_playlist(self):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        playlist_window = tk.Toplevel(root)
        playlist_window.title("Playlist")
        playlist_window.geometry("300x300")

        label = tk.Label(playlist_window, text="Playlist Name: " + self.start.song)
        label.pack()

        current = self.start.next
        while current is not None:
            label = tk.Label(playlist_window, text=current.song)
            label.pack()
            current = current.next

    def count_nodes(self):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        count = 0
        current = self.start
        while current is not None:
            count += 1
            current = current.next

        messagebox.showinfo("Total Songs", "Total songs in the playlist: " + str(count-1))

    def search_song(self, song):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        current = self.start
        while current is not None:
            print(song)
            print(current.song)
            if current.song == song:
                messagebox.showinfo("Song Found", "The song is in the playlist.")
                return
            current = current.next

        messagebox.showinfo("Song Not Found", "The song is not in the playlist. Maybe you missed the file extension?")

    def push(self, song):
        if self.top is None:
            self.top = Node(song)
        elif self.top.song != song:
            new_node = Node(song)
            new_node.next = self.top
            self.top.prev = new_node
            self.top = new_node

    def displaysortedplaylist(self):
        global queue
        global listofsongs
        global playlist
        global songsinplaylistbox
        playlist.delete(0,END)
        songsinplaylistbox.delete(0,END)
        queue=[]
        listofsongs=[]
        current = self.start.next
        while current is not None:
            listofsongs.append(current.song)
            playlist.insert(END,current.song)
            songsinplaylistbox.insert(END,current.song)
            current = current.next
            
    def sort_playlist(self):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        if self.start.next is None:
            messagebox.showinfo("Sorted Playlist", "Playlist is already sorted.")
            return

        sorted_playlist = PlaylistManager()
        sorted_playlist.create(self.start.song)

        current = self.start.next
        while current is not None:
            sorted_playlist.add_node(current.song)
            current = current.next

        sorted_playlist.start.next = self.sort(sorted_playlist.start.next)
        sorted_playlist.displaysortedplaylist()

    def sort(self, start):
        a = None
        b = None
        c = None
        e = None
        tmp = None

        while e != start.next:
            c = a = start
            b = a.next

            while a != e:
                if a.song > b.song:
                    if a == start:
                        tmp = b.next
                        b.next = a
                        a.next = tmp
                        start = b
                        c = b
                    else:
                        tmp = b.next
                        b.next = a
                        a.next = tmp
                        c.next = b
                        c = b
                else:
                    c = a
                    a = a.next
                b = a.next
                if b == e:
                    e = a
        return start

    def save_playlist(self):
        if self.start is None:
            messagebox.showerror("Error", "Please create a playlist first.")
            return

        playlist_name = self.start.song
        file_path = filedialog.asksaveasfilename(title="Save Playlist", filetypes=[("Text Files", "*.txt")], defaultextension=".txt", initialfile=playlist_name)
        if file_path == "":
            return

        try:
            with open(file_path, "w") as file:
                current = self.start
                while current is not None:
                    file.write(current.song + "\n")
                    current = current.next

            messagebox.showinfo("Success", "Playlist saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", "Failed to save playlist.\nError: " + str(e))


    def load_playlist(self):
        global songsinsideplaylist
        global default_playlist_directory_path
        global listofsongs
        listofsongs=[]
        file_path = filedialog.askopenfilename(title="Load Playlist", filetypes=[("Text Files", "*.txt")],initialdir= default_playlist_directory_path)
        if file_path == "":
            return

        try:
            with open(file_path, "r") as file:
                playlist_name = file.readline().strip()
                self.create(playlist_name)

                for line in file:
                    song = line.strip()
                    self.add_node(song)
                    songsinsideplaylist.append(song)

            messagebox.showinfo("Success", "Playlist loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", "Failed to load playlist.\nError: " + str(e))

def create_playlist():
    global songsinplaylistbox
    global playlist
    global listofsongs
    global queue
    queue=[]
    listofsongs=[]
    songsinplaylistbox.delete(0,END)
    stop_song(song_status)
    playlist.delete(0,END)
    playlist_name = playlist_entry.get()
    if playlist_name == "":
        messagebox.showwarning("Invalid Input", "Please enter a playlist name.")
        return

    manager.create(playlist_name)
    messagebox.showinfo("Success", "Playlist created successfully.")
    playlist_entry.delete(0, tk.END)

def add_song():
    global songsinplaylistbox
    global songsinplaylist
    global listofsongs
    global playlist
    global default_playlist_directory_path
    file_path = filedialog.askopenfilename(title="Select MP3 File", filetypes=[("MP3 Files", "*.mp3")],
                                           initialdir=default_database_directory_path)
    if file_path == "":
        return
    
    song = os.path.basename(file_path)
    songsinplaylistbox.insert(END,song)
    playlist.insert(END,song)
    songsinplaylist.append(song)
    listofsongs.append(song)
    manager.add_node(song)
    song_entry.delete(0, tk.END)

def delete_song():
    global songsinplaylistbox
    global listofsongs
    global playlist
    x=(songsinplaylistbox.curselection())
    selected_item = songsinplaylistbox.get(songsinplaylistbox.curselection())
    songsinplaylistbox.delete(songsinplaylistbox.curselection())
    playlist.delete(x)
    listofsongs.remove(selected_item)
    manager.delete_node(selected_item)
    song_entry.delete(0, tk.END)

def display_playlist():
    manager.display_playlist()

def count_songs():
    manager.count_nodes()

def search_song():
    song = song_entry.get()
    if song == "":
        messagebox.showwarning("Invalid Input", "Please enter a song name.")
        return

    manager.search_song(song)
    song_entry.delete(0, tk.END)

def sort_playlist():
    manager.sort_playlist()

def save_playlist():
    manager.save_playlist()

def load_playlist():
    global playlist
    global listofsongs
    global songsinsideplaylist
    global songsinplaylistbox
    global default_database_directory_path
    
    manager.load_playlist()
    os.chdir(default_database_directory_path)
    playlist.delete(0, END)
    songsinplaylistbox.delete(0,END)
    tracks = os.listdir()
    if songsinsideplaylist!=[]:
        for track in tracks:
            if track.endswith(".mp3"):
                if track in songsinsideplaylist:
                    listofsongs.append(track)
                    playlist.insert(END, track)
                    songsinplaylistbox.insert(END,track)
    else:
        print("playlist empty")    

def About():
    textfile=open("Aboutus.txt",'r')
    l1=textfile.readline()
    l2=textfile.readline()
    l3=textfile.readline()
    textfile.close()
    abt=Tk()
    abt.geometry("500x200")
    abt.configure(bg="#FFFFFF")
    lbl1=Label(abt, text=l1,bg="#FFFFFF")
    lbl2=Label(abt,text=l2,bg="#FFFFFF")
    lbl3=Label(abt,text=l3,bg="#FFFFFF")
    lbl1.pack()
    lbl2.pack()
    lbl3.pack()

def usage():
    textfile=open("usage_v1.txt",'r')
    n1=textfile.read()
    textfile.close()
    log=Tk()
    log.geometry("500x300")
    log.configure(bg="#FFFFFF")
    lbl1=Label(log, text=n1,bg="#FFFFFF")
    lbl1.pack()

currentpos=0
queue = []
playedqueue=[]
currentindex=0
# Creating the master GUI
root = Tk()
root.geometry('900x671')
root.title("Music Player")
root.resizable(0, 0)
menu = Menu(root)
root.configure(menu=menu)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='Usage',command=usage)
helpmenu.add_command(label='About',command=About)
title = Frame(root,height=50,width=900,background="#FFFFFF") 
Label(title, text="Music Player", font=('Vladimir Script',25,'bold'),bg="#FFFFFF",fg='#00FFFF').place(x=360,y=0)
title.place(x=0,y=0)

# All the frames
song_frame = LabelFrame(root, text='Current Song', bg='LightBlue', width=600, height=80)
song_frame.place(x=0, y=50)

button_frame = LabelFrame(root, text='Control Buttons', bg='Turquoise', width=600, height=120)
button_frame.place(y=130)

listbox_frame = Frame(root, bg='RoyalBlue')
inside_frame1=LabelFrame(listbox_frame, text='list of songs', bg='RoyalBlue')
inside_frame1.place(x=0,y=0,height=300,width=300)
inside_frame2=LabelFrame(listbox_frame, text='queue of songs', bg='RoyalBlue')
inside_frame2.place(x=0,y=301,height=300,width=300)
listbox_frame.place(x=600, y=50, height=600, width=300)

playlist_frame=LabelFrame(root,text='playlist' ,bg='#49b8ff')
inside_frame3=LabelFrame(playlist_frame,text='songs in playlist', bg='RoyalBlue')
inside_frame3.place(x=330,y=10,height=300,width=230)
playlist_frame.place(x=0,y=250,height=400,width=600)

# All StringVar variables
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

# Playlist ListBox
global playlist
playlist = Listbox(inside_frame1, font=('Helvetica', 11), selectbackground='Gold')
scroll_bar = Scrollbar(inside_frame1, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)
playlist.place(x=5,y=5,height=270,width=270)

#queue Listbox
global queuelistbox
queuelistbox=Listbox(inside_frame2, font=('Helvetica', 11), selectbackground='Gold')
scroll_bar = Scrollbar(inside_frame2, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)
queuelistbox.place(x=5,y=5,height=270,width=270)

#songs in playlistbox
global songsinplaylistbox
global songsinplaylist
songsinplaylist=[]
songsinplaylistbox=Listbox(inside_frame3, font=('Helvetica', 11), selectbackground='Gold')
scroll_bar = Scrollbar(inside_frame3, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)
songsinplaylistbox.place(x=5,y=15,height=250,width=200)

# SongFrame Labels
Label(song_frame, text='CURRENTLY PLAYING:', bg='LightBlue', font=('Times', 10, 'bold')).place(x=5, y=20)
song_lbl = Label(song_frame, textvariable=current_song, bg='Goldenrod', font=("Times", 12), width=25)
song_lbl.place(x=150, y=20)

# Buttons in the main screen
previous_btn = Button(button_frame, text='Previous', bg='Aqua', font=("Georgia", 13), width=7,
                      command=lambda: previous_song(current_song, playlist, song_status))
previous_btn.place(x=15, y=10)

pause_btn = Button(button_frame, text='Pause', bg='Aqua', font=("Georgia", 13), width=7,
                    command=lambda: pause_song(song_status))
pause_btn.place(x=105, y=10)

stop_btn = Button(button_frame, text='Stop', bg='Aqua', font=("Georgia", 13), width=7,
                  command=lambda: stop_song(song_status))
stop_btn.place(x=195, y=10)

play_btn = Button(button_frame, text='Play', bg='Aqua', font=("Georgia", 13), width=7,
                  command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=285, y=10)

resume_btn = Button(button_frame, text='Resume', bg='Aqua', font=("Georgia", 13), width=7,
                    command=lambda: resume_song(song_status))
resume_btn.place(x=375, y=10)

next_btn = Button(button_frame, text='Next', bg='Aqua', font=("Georgia", 13), width=7,
                  command=lambda: next_song(current_song, playlist, song_status))
next_btn.place(x=465, y=10)

load_btn = Button(button_frame, text='Load Directory', bg='Aqua', font=("Georgia", 13), width=52,
                  command=lambda: load(playlist))
load_btn.place(x=15, y=55)

manager = PlaylistManager()

playlist_label = Label(playlist_frame, text="Playlist Name:",bg='#49b8ff', font=("Georgia", 10))
playlist_label.place(x=10,y=10)

playlist_entry = Entry(playlist_frame)
playlist_entry.place(x=125,y=10)

create_btn = Button(playlist_frame, text="Create Playlist", command=create_playlist, bg='Aqua', font=("Georgia", 10))
create_btn.place(x=75,y=40)

song_label = Label(playlist_frame, text="Song Name:",bg='#49b8ff', font=("Georgia", 10))
song_label.place(x=10,y=75)

song_entry = Entry(playlist_frame)
song_entry.place(x=125,y=75)

add_btn = Button(playlist_frame, text="Add Song", command=add_song, bg='Aqua', font=("Georgia", 10))
add_btn.place(x=80,y=105)

delete_btn = Button(playlist_frame, text="Delete Song", command=delete_song, bg='Aqua', font=("Georgia", 10))
delete_btn.place(x=75,y=140)

'''
display_btn = Button(playlist_frame, text="Display Playlist", command=display_playlist)
display_btn.place(x=0,y=100)
'''

count_btn = Button(playlist_frame, text="Count Songs", command=count_songs, bg='Aqua', font=("Georgia", 10))
count_btn.place(x=20,y=175)

search_btn = Button(playlist_frame, text="Search Song", command=search_song, bg='Aqua', font=("Georgia", 10))
search_btn.place(x=120,y=175)

sort_btn = Button(playlist_frame, text="Sort Playlist", command=sort_playlist, bg='Aqua', font=("Georgia", 10))
sort_btn.place(x=78,y=210)

save_btn = Button(playlist_frame, text=" Save Playlist", command=manager.save_playlist, bg='Aqua', font=("Georgia", 10))
save_btn.place(x=20,y=245)

load_btn = Button(playlist_frame, text="Load Playlist", command=load_playlist, bg='Aqua', font=("Georgia", 10))
load_btn.place(x=120,y=245)

# Label at the bottom that displays the state of the music
Label(root, textvariable=song_status, bg='SteelBlue', font=('Times', 9), justify=LEFT).pack(side=BOTTOM, fill=X)

# Finalizing the GUI
root.update()
root.mainloop()
