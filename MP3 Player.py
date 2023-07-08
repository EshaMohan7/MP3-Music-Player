import os
import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from random import shuffle
import tkinter.ttk as ttk
import datetime

root = Tk()
root.state("zoomed")
root.title("MP3 Music Player")

root.configure(background="#000000")
root.resizable(False, False)

width = root.winfo_screenwidth()


def wish_me():

    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:  # MORNING
        greeting = "Good Morning!"
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    return (greeting+"\nLet us groove to some tunes!")


mixer.init()


def AddMusic():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            if song.endswith(".mp3"):
                Playlist.insert(END, song)


def PlayMusic():
    # --song can play
    global stopped
    stopped = False

    global Music_Name
    Music_Name = Playlist.get(ACTIVE)
    # print(Music_Name(ACTIVE))
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play(loops=0)

    History.insert(END, Music_Name)
    # time.sleep(5)
    play_time()

    # get current volume

    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)

    # update song name
    current_song_name = Label(root, text=Music_Name, font=(
        "Calibri", 20, "bold"), background="#000000", foreground="#FFFFFF")
    current_song_name.place(relx=0.34, rely=0.75, height=70, width=500)

# def song_name():


global pause
pause = False


def paused(is_pause):

    global pause
    pause = is_pause
    if pause:
        mixer.music.unpause()
        pause = False
    else:

        mixer.music.pause()
        pause = True


global stopped
stopped = False


def stop():
    # reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # stop Song from Playing
    mixer.music.stop()
    Playlist.select_clear(ACTIVE)

    # clear status bar
    status_bar.config(text='')

    global stopped
    stopped = True


def next_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = Playlist.curselection()
    next_one = next_one[0]+1
    song = Playlist.get(next_one)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    History.insert(END, song)
    # Clear & Move active bar in playlist
    Playlist.selection_clear(0, END)
    Playlist.activate(next_one)
    Playlist.selection_set(next_one, last=None)

    # update song name
    current_song_name = Label(root, text=song, font=(
        "Calibri", 20, "bold"), background="#000000", foreground="#FFFFFF")
    current_song_name.place(relx=0.34, rely=0.75, height=70, width=500)
    slide()


def previous_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = Playlist.curselection()
    next_one = next_one[0]-1
    song = Playlist.get(next_one)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    History.insert(END, song)
    # Clear & Move active bar in playlist
    Playlist.selection_clear(0, END)
    Playlist.activate(next_one)
    Playlist.selection_set(next_one, last=None)

    # update song name
    current_song_name = Label(root, text=song, font=(
        "Calibri", 20, "bold"), background="#000000", foreground="#FFFFFF")
    current_song_name.place(relx=0.34, rely=0.75, height=70, width=500)


def delete_song():
    stop()
    Playlist.delete(ANCHOR)
    mixer.music.stop()


def delete_all_songs():
    stop()
    Playlist.delete(0, END)
    mixer.music.stop()


def play_time():

    if stopped:
        return

    current_time = mixer.music.get_pos()/1000

    # slider_label.config(text)

    converted_current_time = time.strftime(
        '%M:%S', time.gmtime(current_time))

    current_one = Playlist.curselection()
    song = Playlist.get(current_one)
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime(
        '%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(my_slider.get()) == int(song_length):

        status_bar.config(
            text=f'{converted_song_length} ')

    elif pause:
        pass

    elif int(my_slider.get()) == int(current_time):
        # slider hasnt been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # slider has been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        converted_current_time = time.strftime(
            '%M:%S', time.gmtime(int(my_slider.get())))

        status_bar.config(
            text=f' {converted_current_time}/{converted_song_length} ')

        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)

    # status_bar.config(
    #     text=f' {converted_current_time}/{converted_song_length} ')

    # update slider position value to current song position
    # my_slider.config(value=int(current_time))

    # update time
    status_bar.after(1000, play_time)
    # pass


def randomPlaylist():
    # current_one = Playlist.curselection()
    all_songs = Playlist.get(0, END)
    all_songs = list(all_songs)
    shuffle(all_songs)
    Playlist.delete(0, END)
    for song in all_songs:
        Playlist.insert(END, song)


def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')

    Music_Name = Playlist.get(ACTIVE)
    # print(Music_Name(ACTIVE))
    mixer.music.load(Music_Name)
    mixer.music.play(loops=0, start=int(my_slider.get()))


def volume(x):
    mixer.music.set_volume(volume_slider.get())

    # change volume meter picture
    current_volume = mixer.music.get_volume()
    current_volume = current_volume*100  # easier to work with

    if int(current_volume) < 1:
        volume_meter.config(image=vol0)

    elif int(current_volume) > 0 and int(current_volume) <= int(current_volume) <= 33:
        volume_meter.config(image=vol1)

    elif int(current_volume) > 33 and int(current_volume) <= int(current_volume) <= 66:
        volume_meter.config(image=vol2)

    elif int(current_volume) > 66 and int(current_volume) <= int(current_volume) <= 100:
        volume_meter.config(image=vol3)

    # get current volume
    # current_volume = mixer.music.get_volume()

    # lower_frame = Frame(root, bg="#000000", height=180, width=width)
    # lower_frame.pack(fill='x')
    # lower_frame.place(y=500)


bg = PhotoImage(file="framebg.png")
bgimg = Label(root, image=bg).pack()

f_bg = PhotoImage(file="framebg.png")

upper_left_frame = Frame(root, bg="#000000", height=180, width=350)
upper_left_frame.place(y=70, x=20)

lower_left_frame = Frame(root, bg="#000000", height=400, width=350)
lower_left_frame.place(y=300, x=20)

# mid_frame = Frame(root, bg="#9C44D3", height=630, width=850, bd=2)
# mid_frame.place(y=70, x=400)

right_frame = Frame(root, bg="#000000", height=580, width=230)
right_frame.place(y=118, x=1280)

image_logo = PhotoImage(file="logo2.png")
root.iconphoto(False, image_logo)

wish = Label(upper_left_frame, text=wish_me(), font=(
    "Brush Script MT", 24), background="#000000", foreground="#FFFFFF").place(rely=0.26, relx=0.06)

music_logo = PhotoImage(file="logo2.png")
logo = Label(root, image=music_logo, background="#000000").place(
    rely=0.13, relx=0.34)

# Menu = PhotoImage(file="black.png")
# Label(root, image=Menu).place(x=0, y=720, height=130, width=width)


Button(root, text="Browse Music", width=43, height=1, font=(
    "Calibri", 12, "bold"), fg="Black", bg="#FFFFFF", command=AddMusic).place(x=20, y=265)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=20, y=300, width=350, height=400)

ButtonPlay = PhotoImage(file="play.png")
Button(root, image=ButtonPlay, bg="#000000", bd=0, height=60,
       width=60, command=PlayMusic).place(relx=0.5, y=750)

ButtonStop = PhotoImage(file="stop.png")
Button(root, image=ButtonStop, bg="#000000", bd=0, height=60,
       width=60, command=stop).place(relx=0.45, y=750)

ButtonPause = PhotoImage(file="pause.png")
Button(root, image=ButtonPause, bg="#000000", bd=0, height=60,
       width=60, command=lambda: paused(pause)).place(relx=0.55, y=750)

# ButtonVolume = PhotoImage(file="volume.png")
# panel1 = Label(root, image=ButtonVolume, bg="#000000", height=60,
#    width=60).place(relx=0.75, y=750)
global vol0
global vol1
global vol2
global vol3

vol0 = PhotoImage(file="volume0.png")
vol1 = PhotoImage(file="volume1.png")
vol2 = PhotoImage(file="volume2.png")
vol3 = PhotoImage(file="volume3.png")

volume_meter = Label(root, image=vol3, bg="#000000", height=60,
                     width=60)
volume_meter.place(relx=0.75, y=750)

ButtonForward = PhotoImage(file="forward.png")
Button(root, image=ButtonForward, bg="#000000",
       bd=0, height=60, width=60, command=next_song).place(relx=0.6, y=750)

ButtonBackward = PhotoImage(file="backward.png")
Button(root, image=ButtonBackward, bg="#000000",
       bd=0, height=60, width=60, command=previous_song).place(relx=0.4, y=750)

ButtonRandom = PhotoImage(file="random.png")
Button(root, image=ButtonRandom, bg="#000000", bd=0, height=60,
       width=60, command=randomPlaylist).place(relx=0.35, y=750)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Calibri", 12), bg="#000000",
                   fg="#FFFFFF", selectbackground="gray", selectforeground="black", cursor="hand2", bd=0, yscrollcommand=Scroll.set)

Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

recent = Label(root, text="Recently Played", font=(
    "Calibri", 22), background="#000000", foreground="#FFFFFF").place(y=70, x=1295)

# History = Frame(root, bd=2, relief=RIDGE)
# History.place(y=70, x=1280, height=630, width=230)
History = Listbox(right_frame, width=70, font=("Calibri", 12), bg="#000000",
                  fg="#FFFFFF", selectbackground="gray", selectforeground="black", cursor="hand2", bd=0)

# History.pack(side=RIGHT, fill=BOTH)
History.place(height=580, width=230)

my_menu = Menu(root)
root.config(menu=my_menu)
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete one song", command=delete_song)
remove_song_menu.add_command(
    label="Delete all songs", command=delete_all_songs)

my_slider = ttk.Scale(root, from_=0, to=100,
                      orient=HORIZONTAL, value=0, command=slide, length=442)
my_slider.pack(pady=5)
my_slider.place(y=715, relx=0.35)

# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

status_bar = Label(root, text='', bd=2, relief=GROOVE, anchor=E)
# status_bar.pack(side=BOTTOM, ipady=2)
status_bar.place(relx=0.68, y=770)
# root.bind('<Configure>', resizer)

volume_slider = ttk.Scale(
    root, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=100)
volume_slider.place(relx=0.8, y=770)


root.mainloop()
