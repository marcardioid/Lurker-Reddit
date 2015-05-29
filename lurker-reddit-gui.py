#!/usr/bin/python

import tkinter
import subprocess

class simpleapp_tk(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        # SUBREDDIT
        self.labelVariableSubreddit = tkinter.StringVar()
        labelSubreddit = tkinter.Label(self, textvariable=self.labelVariableSubreddit, anchor="w", fg="black", bg="white")
        labelSubreddit.grid(column=0, row=0, sticky="EW")
        self.labelVariableSubreddit.set(u"Subreddit:")
        self.entryVariableSubreddit = tkinter.StringVar()
        self.entrySubreddit = tkinter.Entry(self, textvariable=self.entryVariableSubreddit)
        self.entrySubreddit.grid(column=1, row=0, sticky="EW")
        self.entryVariableSubreddit.set(u"")

        # COUNT
        self.labelVariableCount = tkinter.StringVar()
        labelCount = tkinter.Label(self, textvariable=self.labelVariableCount, anchor="w", fg="black", bg="white")
        labelCount.grid(column=0, row=1, sticky="EW")
        self.labelVariableCount.set(u"Posts:")
        self.entryVariableCount = tkinter.StringVar()
        self.entryCount = tkinter.Entry(self, textvariable=self.entryVariableCount)
        self.entryCount.grid(column=1, row=1, sticky="EW")
        self.entryVariableCount.set(u"")

        # CATEGORY
        self.labelVariableCategory = tkinter.StringVar()
        labelCategory = tkinter.Label(self, textvariable=self.labelVariableCategory, anchor="w", fg="black", bg="white")
        labelCategory.grid(column=0, row=2, sticky="EW")
        self.labelVariableCategory.set(u"Category:")
        optionList = ("hot", "top-all", "top-day", "top-hour", "top-month", "top-month", "top-week",
                                 "top-year", "con", "con-all", "con-day", "con-hour", "con-month", "con-week",
                                 "con-year", "hot", "new", "new-bydate", "new-byrising", "random", "rising")
        self.optionVariable = tkinter.StringVar()
        self.optionVariable.set(optionList[0])
        option = tkinter.OptionMenu(self, self.optionVariable, *optionList)
        option.grid(column=1, row=2, sticky="EW")

        # SUBMIT
        self.submit = tkinter.Button(self, text=u"Download", command=self.OnSubmit)
        self.submit.grid(column=1, row=3)

        self.grid_columnconfigure(0, weight=1)
        self.minsize(width=300,height=20)
        self.resizable(False, False)
        self.update()
        self.geometry(self.geometry())

        self.entrySubreddit.focus_set()
        self.entrySubreddit.selection_range(0, tkinter.END)

    def OnSubmit(self):
        subprocess.call("python.exe lurker-reddit.py --count " + self.entryVariableCount.get() + " --output reddit --category " + self.optionVariable.get() + " " + self.entryVariableSubreddit.get())

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.configure(background="white")
    app.title("Lurker for Reddit")
    app.mainloop()