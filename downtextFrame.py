__author__ = 'reem'
from Tkinter import Frame, Label
from constants import *

class DowntextFrame(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master=master, cnf=cnf, **kw)
        self.master = master
        self.countdownText = ''
        self.countdown_label = Label(master = self, text = 'initializing...', font = FONT_DOWNTEXT_FONT, fg = 'black')
        self.borderLabel = Label(master = self, text = '   ', font = FONT_DOWNTEXT_FONT, fg = 'black')
        self.anotherLabel = Label(master = self, text = '', font = FONT_DOWNTEXT_FONT, fg = 'black')


    def grid(self, cnf={}, **kw):
        Frame.grid(self, cnf=cnf, **kw)
        self.countdown_label.grid(row = 0, column = 0)
        self.borderLabel.grid(row = 0, column = 1)
        self.anotherLabel.grid(row = 0, column = 2)


    def update_countdown(self, text):
        self.countdownText = text
        self.countdown_label.config(text = str(text))
        # todo continue