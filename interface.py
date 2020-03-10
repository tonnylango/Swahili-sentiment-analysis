from tkinter import *
import Pmw

class Interface (Frame):
    
    def __init__(self):
        Frame.__init__(self)
        Pmw.initialise()
        self.pack(expand = YES, fill = BOTH)
        self.master.title("sentiment analyser")
        self.master.geometry("400x400")
        
        self.baloon = Pmw.Balloon(self)
        
        self._setMenuBar()
        self._setEntry()
        self._setDisplay()
        self. _setButtons()

    def _setEntry(self):
        self.fileEntry = Entry(self, name = "file")
        self.fileEntry.grid(row = 1, columnspan = 5, sticky = W + E, padx = 5, pady = 5)
        self.fileEntry.insert(INSERT, "Enter location of file here.")
        self.fileEntry.bind("<Return>", self.process)

        self.browseButton = Button(self, text = "...", command = self.browseFile)
        self.browseButton.grid(row = 1, column = 6, padx = 5)

        self.webEntry = Entry(self, name = "web")
        self.webEntry.grid(row = 2, columnspan = 6, sticky = W + E, padx = 5, pady = 5)
        self.webEntry.insert(INSERT, "Enter URL here.")
        self.webEntry.bind("<Return>", self.process)

        self.columnconfigure( 0, weight = 1)
        
    def _setMenuBar(self):
        self.menubar = Pmw.MenuBar(self, balloon = self.baloon)
        self.menubar.grid(columnspan = 6, sticky = W + E )
        #self.menubar.pack(fill = tk.X)
        
        self.menubar.addmenu("File", "command")
        self.menubar.addmenuitem("File", "command", command = self.saveSentiment, label = "Save")

    def _setDisplay(self):
        self.text =  Pmw.ScrolledText( self, text_width = 25, text_height = 12, text_wrap = WORD, hscrollmode = "static", vscrollmode = "static" )
        self.text.grid(row = 3, columnspan = 6, sticky = W + E + N + S, padx = 5, pady = 5)
        self.text.bind("<Return>", self.process)
        self.rowconfigure(3, weight = 1)

        self.info = Pmw.ScrolledText(self, text_width = 25, text_height = 3)
        self.info.insert(INSERT, "Sentences:\nPositives:\nNegatives:\n")
        self.info.configure(text_state = DISABLED)
        self.info.grid(row = 4, columnspan = 6, sticky = W + E, padx = 5, pady = 5)

    def _setButtons(self):
        holder = Frame(self)
        positive = Button(holder, text = "Positives", command = self.displayPositives)
        positive.pack(fill = X, expand = YES, side = LEFT)

        negative = Button(holder, text = "Negatives", command = self.displayNegatives)
        negative.pack(fill = X, expand = YES, side = LEFT)

        clear = Button(holder, text = "Clear", command = self.clear)
        clear.pack(fill = X, expand = YES, side = LEFT)

        holder.grid(row = 5, columnspan = 6, sticky = W + E, padx = 5, pady = 5)
                                                              
    def saveSentiment(self):
        pass

    def browseFile(self):
        pass

    def process(self, event):
        pass

    def displayPositives(self):
        pass

    def displayNegatives(self):
        pass

    def clear(self):
        pass

def main():
    Interface().mainloop()
    
if __name__ == "__main__":
    main()
