import os
import sys
import subprocess
import pickle
import pip
from tkinter import *
import tkinter.messagebox as messagebox

default_database_directory_path = "database"
default_playlist_directory_path="playlist"

def modulesinstaller():
      def newframe():
            nf=Frame(sideframe,background="#FFFFFF")
            lbl7=Label(nf, text = "all modules already present/installed close this frame and start app again",bg="#FFFFFF")
            lbl7.pack()
            nf.grid(row=5,column=1,sticky='w')
      global l1
      l1=[0,0]
      def install(package):
            subprocess.check_call([sys.executable,"-m","pip", "install", package])
            chkpkg()

      def b4():
            def install1():
                  l1[0]=2
                  btn2.destroy()
                  lbl6=Label(sideframe, text = "installed",bg="#FFFFFF")
                  lbl6.grid(row=2,column=1)
                  install("mutagen")
            def install2():
                  l1[1]=2
                  btn3.destroy()
                  lbl6=Label(sideframe, text = "installed",bg="#FFFFFF")
                  lbl6.grid(row=3,column=1)
                  install("pygame")
                  
            global l1
            if l1[0]==0:
                  l1[0]=2
                  lbl4=Label(sideframe, text = "already present",bg="#FFFFFF")
                  lbl4.grid(row=2,column=1)
            if l1[0]==1:
                  btn2=Button(sideframe, text = "install mutagen",bg="#FFFFFF",command=install1)
                  btn2.grid(row=2,column=1)
            if l1[1]==0:
                  l1[1]=2
                  lbl5=Label(sideframe, text = "already present",bg="#FFFFFF")
                  lbl5.grid(row=3,column=1)
            if l1[1]==1:
                  btn3=Button(sideframe, text = "install pygame",bg="#FFFFFF",command=install2)
                  btn3.grid(row=3,column=1)
            if l1==[2,2]:
                  newframe()

      def chkpkg():
            global l1
            for i in range (0,2):
                  if i==0:
                        try:
                              import mutagen
                        except ModuleNotFoundError:
                              l1[0]=1
                  if i==1:
                        try:
                              import pygame
                        except ModuleNotFoundError:
                              l1[1]=1
            b4()
                  
      sideframe=Tk()
      sideframe.title("modules installer_Music player")
      sideframe.geometry("500x300")
      sideframe.configure(bg="#FFFFFF")
      lbl1=Label(sideframe, text = "Checking for modules", font=('Calibri',15),bg="#FFFFFF")
      lbl1.grid(row=1,column=1)
      lbl2=Label(sideframe, text = "mutagen", bg="#FFFFFF")
      lbl2.grid()
      lbl3=Label(sideframe, text = "pygame", bg="#FFFFFF")
      lbl3.grid()
      chkpkg()


def startapp():
      global default_database_directory_path
      global default_playlist_directory_path
      root.destroy()
      path1='./settings'
      try:
              os.mkdir(default_database_directory_path)
              os.mkdir(default_playlist_directory_path)
              messagebox.showinfo("Thank you", "Thank you for choosing music player.\nFirst add songs to database folder which will be created shortly.\nYou can save the playlist to playlist folder and load it from there when required")
              import main3
      except FileExistsError:
                import main3
              
def moduleschecker():
      def c2():
            try:
                  import pygame
                  startapp()
            except ModuleNotFoundError:
                  modulesinstaller()

      def c1():
            try:
                  import mutagen
                  c2()
            except ModuleNotFoundError:
                  modulesinstaller()
      c1()

root= Tk()
root.title("Songs manager")
root.geometry("500x300")
root.configure(bg="#FFFFFF")
#root.iconbitmap("Cash-App-Logo.ico")
frame1 = Frame(root,background="#FFFFFF")
lbl1= Label(root, text = "Music Player", font=('Vladimir Script',25,'bold'),bg="#FFFFFF",fg='#00FFFF')
btn1=Button(frame1, text="start app", command=moduleschecker,font=('Calibri',10),width=25)
lbl1.pack()
btn1.pack(pady=100)
frame1.pack()
frame2=Frame(root,background="#AFFFFF")
lbl1=Label(root, text = "Version : 1.0.01", font=('Calibri',15),bg="#FFFFFF")
lbl1.pack()
frame2.pack()
root.mainloop()
