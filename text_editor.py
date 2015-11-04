import tkinter as tk
from tkinter import ttk

import file_manager as fm

class TextEditorApp(tk.Frame):
    def __init__ (self, master=None):
        #Outer Frame of the application
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.grid(sticky="nsew")

        #Name of the application at the top
        self.master.title("Text Editor")

        #Create Widgets
        self.createWidgets()

        #Other Variables
        #Current File keeps track of which file the user is currently editing
        self.current_file = None

    def createWidgets(self):
        #Set up top space
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        #The text box to edit code
        self.textBox = tk.Text(self)
        self.textBox.grid(row=0, column=0)

        #Menu Buttons
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar
        self.fileMenu = tk.Menu(self.menuBar)

        #File
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open', command=self.openFile)
        self.fileMenu.add_command(label='Save', command=self.saveFile)
        self.fileMenu.add_command(label='Save As', command=self.saveAsFile)
        self.fileMenu.add_command(label='Exit', command=quit)

    def openFile(self):
        #Get the filename and load the text
        filename = tk.filedialog.askopenfilename()
        loaded_text = fm.load_file(filename)

        #Insert the text into the text box
        self.textBox.delete('1.0', tk.END)
        self.textBox.insert('1.0', loaded_text)

        #Change the current file and add the file name to the title
        self.current_file = filename
        self.master.title("Text Editor - " + self.current_file)

    def saveFile(self):
        #Save the file without creating a new file if we know it already exists
        if self.current_file != None:
            saved_text = self.textBox.get('1.0', tk.END)
            fm.save_file(self.current_file, saved_text)
        else:
            self.saveAsFile()

    def saveAsFile(self):
        #Save the file by creating a new file
        filename = tk.filedialog.asksaveasfilename()
        saved_text = self.textBox.get('1.0', tk.END)

        fm.save_file(filename, saved_text)

        #Change the current file and add the file name to the title
        self.current_file = filename
        self.master.title("Text Editor - " + self.current_file)

#Run the Program
if __name__ == "__main__":
    #Create the application object
    root = tk.Tk()
    app = TextEditorApp(root)

    #Run the Application
    app.mainloop()
