import tkinter as tk
from tkinter import ttk

import file_manager as fm

class TextEditorApp(tk.Frame):
    def __init__ (self, *args, **kwargs):
        #Outer Frame of the application
        tk.Frame.__init__(self, *args, **kwargs)
        self.grid(sticky="nsew")

        #Name of the application at the top
        self.master.title("Text Editor")

        #Window Size Stuff
        self.master.geometry("640x480")
        self.master.minsize(320, 240)

        #Popup!
        self.master.bind("<Button-3>", self.popup)

        #Keep track of tabs
        #The reason this is here is because notebook does not return
        #child values of the tabs, so we have to keep track of it
        #ourselves
        self.tabs = {}

        #Create Widgets
        self.createWidgets()

    def createWidgets(self):
        #Set up top space
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        #The Notebook so user can quickly shift between files
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side="top", fill = "both", expand=True)
        
        #Menu Buttons
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar

        #File
        self.fileMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='New', command=self.newFile)
        self.fileMenu.add_command(label='Open', command=self.openFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Save', command=self.saveFile)
        self.fileMenu.add_command(label='Save As', command=self.saveAsFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Close', command=self.closeTab)
        self.fileMenu.add_command(label='Exit', command=quit)

        #Edit
        self.editMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Edit', menu=self.editMenu)
        self.editMenu.add_command(label='Undo', command=self.undo)
        self.editMenu.add_command(label='Redo', command=self.redo)

        #About
        self.helpMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About', command=self.about)

    #Find the value of the current tab textbox
    def getTabText(self):
        tabname = self.notebook.select()
        return self.tabs[tabname]

    #Close the current tab
    def closeTab(self):
        tabname = self.notebook.select()
        #Make sure there is a tab to even close
        if tabname != '':
            self.notebook.forget(self.tabs[tabname])

    #Creates a new textbox to edit files in
    def newTextBox(self):
        textbox = tk.Text(self, undo=True, autoseparators=True)
        textbox.pack(side="bottom", fill= "both", expand=True)

        self.tabs[str(textbox)] = textbox

        return textbox

    #Creates a new tab with a textbox
    def newFile(self, name="Untitled"):
        #Create new textbox
        newTextBox = self.newTextBox()
        
        #Add textbox to tabs
        self.notebook.add(newTextBox, text=name)

        #Focus on new tab with new textbox
        self.notebook.select(newTextBox)

    def openFile(self):
        #Get the filename and load the text
        filename = tk.filedialog.askopenfilename()
        loaded_text = fm.load_file(filename)

        #Open up a new tab to load the file in
        self.newFile()

        #Insert the text into the current text box
        textbox = self.getTabText()
        textbox.delete('1.0', tk.END)
        textbox.insert('1.0', loaded_text)

        #Add the file name to the title of the tab
        self.notebook.tab(textbox, text=filename)

    def saveFile(self):
        pass
        """
        #Get the current textbox
        textbox = self.getTabText()

        #Get current filename
        current_file = 
        
        #Save the file without creating a new file if we know it already exists
        if current_file != None:
            saved_text = textbox.get('1.0', tk.END)
            fm.save_file(current_file, saved_text)
        else:
            self.saveAsFile()"""

    def saveAsFile(self):
        #Get the current textbox
        textbox = self.getTabText()
        
        #Save the file by creating a new fill        
        filename = tk.filedialog.asksaveasfilename()
        saved_text = textbox.get('1.0', tk.END)

        fm.save_file(filename, saved_text)

        #Add the file name to the title of the tab
        self.notebook.tab(textbox, text=filename)
        #self.master.title("Text Editor - " + self.current_file)

    #Undo text edit in current textbox
    def undo(self):
        self.getTabText().edit_undo()

    #Redo text edit in current textbox
    def redo(self):
        self.getTabText().edit_redo()

    #Creates a new window with about info
    def about(self):
        aboutWindow = tk.Toplevel(self)
        aboutWindow.geometry("200x120")
        aboutWindow.minsize(200, 120)
        aboutWindow.maxsize(200, 120)
        
        aboutLabel = tk.Label(aboutWindow, text="Text Editor by Andrew Vieira")
        aboutLabel.pack(side="top")
        
        aboutWindow.grab_set()

    #Create a pop up menu
    def popup(self, event):
        popMenu = tk.Menu(self, tearoff=0)
        popMenu.add_command(label='New', command=self.newFile)
        popMenu.add_command(label='Close', command=self.closeTab)

        popMenu.post(event.x_root, event.y_root)

#Run the Program
if __name__ == "__main__":
    #Create the application object
    root = tk.Tk()
    app = TextEditorApp(root)

    #Run the Application
    app.mainloop()
