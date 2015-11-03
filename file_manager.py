#Andrew Vieira
#File Manager - Used for saving and opening files

def load_file(filename):    
    file = open(filename, "r", encoding="utf-8")
    string = ""

    for line in file:
        string += line

    file.close()

    return string

def save_file(filename, string):
    file = open(filename, "w", encoding="utf-8")
    file.write(string)
    file.close()
