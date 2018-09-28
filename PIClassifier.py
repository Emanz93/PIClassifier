# -*- coding: utf-8 -*-
import platform
from GUI.InitialMenu import InitialMenu
from tkinter import *
from os import getcwd

if __name__ == '__main__':
    root = Tk()
    #if platform.system() != 'Darwin':
    #    img = PhotoImage(file=getcwd() + '/res/img/breath.png')
    #    root.tk.call('wm', 'iconphoto', root._w, img)
    InitialMenu(root)
    root.mainloop()
