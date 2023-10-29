
# Work in progress

from tkinter import *
main_app = Tk()
anime_name_input=tkinter.StringVar()
anime_name = Label(main_app, textvariable = anime_name_input, text='Anime Search string').grid(row=0) 
e1 = Entry(main_app)
e1.grid(row=0, column=1)
print(anime_name_input)
print(anime_name)
mainloop() 