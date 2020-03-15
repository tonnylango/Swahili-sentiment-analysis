import tkinter as tk
from tkinter.filedialog import askopenfilename
import Pmw
from joblib import load
from tkinter.messagebox import showerror

ALL = "all"
POSITIVES = "positives"
NEGATIVES = "negatives"
NOTHING = "nothing"

class Interface (tk.Frame):
    
    def __init__(self):
        tk.Frame.__init__(self)
        Pmw.initialise()
        self.pack(expand = tk.YES, fill = tk.BOTH)
        self.master.title("sentiment analyser")
        self.master.geometry("400x400")
        
        self.baloon = Pmw.Balloon(self)
        self.inputs = self.predictions = []
        
        self._setmenuBar()
        self._setentry()
        self._setdisplay()
        self._setbuttons()

        self.columnconfigure( 0, weight = 1)

        self.model = load("C:/users/tonny/desktop/project/Swahili-sentiment-analysis/model0.joblib")

    def _setentry(self):
        self.fileVariable = tk.StringVar()
        self.fileVariable.set("Enter file Location")
        self.fileEntry = tk.Entry(self, textvariable = self.fileVariable, name = "file")
        self.fileEntry.grid(row = 1, columnspan = 5, sticky = tk.W + tk.E, padx = 5, pady = 5)
        self.fileEntry.bind("<Return>", self.processinput)

        self.browseButton = tk.Button(self, text = "Add", command = self.browse_file)
        self.browseButton.grid(row = 1, column = 6, padx = 5)

        self.webVariable = tk.StringVar()
        self.webVariable.set("Enter URL here.")
        self.webEntry = tk.Entry(self, textvariable = self.webVariable, name = "web")
        self.webEntry.grid(row = 2, columnspan = 6, sticky = tk.W + tk.E, padx = 5, pady = 5)
        self.webEntry.bind("<Return>", self.processinput)

        buttonFrame = tk.Frame(self)
        self.processFile = tk.Button(buttonFrame, text = "Process File", command = self.process_file)
        self.processFile.pack(fill = tk.X, expand = tk.YES, side = tk.LEFT, padx = 5)
        
        self.processWeb = tk.Button(buttonFrame, text = "Process Web", command = self.process_web)
        self.processWeb.pack(fill = tk.X, expand = tk.YES, side = tk.LEFT, padx = 5)

        buttonFrame.grid(row = 3, columnspan = 6, sticky =tk. W + tk.E, padx = 5, pady = 5)
        
    def _setmenuBar(self):
        self.menubar = Pmw.MenuBar(self, balloon = self.baloon)
        self.menubar.grid(columnspan = 6, sticky = tk.W + tk.E )
        
        self.menubar.addmenu("File", "command")
        self.menubar.addmenuitem("File", "command", command = self.saveSentiment, label = "Save")

    def _setdisplay(self):
        self.text =  Pmw.ScrolledText(self, text_width = 25, text_height = 12, text_wrap = tk.WORD, hscrollmode = "static", vscrollmode = "static")
        self.text.grid(row = 4, columnspan = 6, sticky = tk.W + tk.E + tk.N + tk.S, padx = 5, pady = 5)
        self.text.bind("<Return>", self.processinput)
        self.rowconfigure(4, weight = 1)

        self.info = Pmw.ScrolledText(self, text_width = 25, text_height = 3, text_wrap = tk.WORD)
        self.post_results()
        self.info.grid(row = 5, columnspan = 6, sticky = tk.W + tk.E, padx = 5, pady = 5)

    def _setbuttons(self):
        holder = tk.Frame(self)
        positive = tk.Button(holder, text = "Positives", command = lambda : self.display(POSITIVES))
        positive.pack(fill = tk.X, expand = tk.YES, side = tk.LEFT)

        negative = tk.Button(holder, text = "Negatives", command = lambda : self.display(NEGATIVES))
        negative.pack(fill = tk.X, expand = tk.YES, side = tk.LEFT)

        clear = tk.Button(holder, text = "Clear", command = self.clear)
        clear.pack(fill = tk.X, expand = tk.YES, side = tk.LEFT)

        holder.grid(row = 6, columnspan = 6, sticky = tk.W + tk.E, padx = 5, pady = 5)
                                                              
    def saveSentiment(self):
        pass

    def browse_file(self):
        filename = askopenfilename(filetypes = [("Text files", '*.txt')])
        if filename != '':
            if self.fileVariable.get().endswith(';'):
                self.fileVariable.set(self.fileVariable.get() + filename + ';')
            else:
                self.fileVariable.set(filename + ';')
            
    def processinput(self, event):
        #acquire name of Entry component that generated event
        component = event.widget.winfo_name()
        if component == "name":
            pass

    def process_file(self):
        filesnotopened = 0
        lines = []
        for filename in self.fileVariable.get().split(';'):
            if filename != '':
                try:
                    with open(filename, 'r') as file:
                        lines += [line for line in file.read().split('\n') if line != '']
                except FileNotFoundError:
                    filesnotopened += 1

        #self.clear()
        self.inputs = list(lines)
        self.display(ALL)
        self.set_predictions()
        self.post_results()
        
        if filesnotopened > 0:
            showerror("Error",(str(filesnotopened) + " files " if filesnotopened > 1 else " file ") + "not opened")
        
    def set_predictions(self):
        self.predictions = [int(result) for result in self.model.predict(self.inputs)]

    def process_web(self):
        pass

    def display(self, what = "all"):
        self.text.configure(text_state = tk.NORMAL)
        if what.lower() == ALL:
            self.text.settext("\n".join(self.inputs))
        elif what.lower() == POSITIVES:
            self.text.settext("\n".join([self.inputs[i] for i in range(len(self.inputs)) if self.predictions[i] == 1]))
        elif what.lower() == NEGATIVES:
            self.text.settext("\n".join([self.inputs[i] for i in range(len(self.inputs)) if self.predictions[i] == 0]))
        elif what.lower() == NOTHING:
            self.text.settext("")

    def post_results(self):
        sentences = len(self.inputs)
        positives = len([i for i in self.predictions if i == 1])
        negatives = len([i for i in self.predictions if i == 0])
        self.info.configure(text_state = tk.NORMAL)
        self.info.settext("Sentences: %d\nPositives: %d\nNegatives: %d" % (sentences, positives, negatives))
        self.info.configure(text_state = tk.DISABLED)

    def clear(self):
        self.inputs.clear()
        self.predictions.clear()
        self.display(NOTHING)
        self.post_results()
        self.webVariable.set("Enter URL here.")
        self.fileVariable.set("Enter file Location")

def main():
    Interface().mainloop()
    
if __name__ == "__main__":
    main()
