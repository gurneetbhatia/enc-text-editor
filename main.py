from tkinter import *
from filesystem import FileSystem

# constants are declared here
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

class Application(object):

    def __init__(self, master):
        self.master = master
        self.master.title("Molecule")
        self.canvas = Canvas(self.master,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#292C33')

        self.init_menu()

    def init_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="New File")
        file.add_command(label="Load File")
        file.add_command(label="Save File")
        file.add_command(label="Decrypt File")
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Copy Path")
        edit.add_command(label="Paste")
        edit.add_command(label="Select All")
        edit.add_command(label="Toggle Comments")
        edit_lines = Menu(edit)
        edit_lines.add_command(label="Indent")
        edit_lines.add_command(label="Outdent")
        edit_lines.add_command(label="Autodent")
        edit_lines.add_command(label="Move line up")
        edit_lines.add_command(label="Move line down")
        edit_lines.add_command(label="Duplicate Lines")
        edit_lines.add_command(label="Delete Lines")
        edit.add_cascade(label="Lines", menu=edit_lines)
        edit_text = Menu(edit)
        edit_text.add_command(label="Upper Case")
        edit_text.add_command(label="Lower Case")
        edit.add_cascade(label="Text", menu=edit_text)
        menu.add_cascade(labe="Edit", menu=edit)

        organisation = Menu(menu)
        organisation.add_command(label="Login")
        organisation.add_command(label="Create Organisation")
        organisation.add_command(label="View Organisations")
        menu.add_cascade(label="Organisation", menu=organisation)

        run = Menu(menu)
        run.add_command(label="Run")
        run.add_command(label="Run with Arguments")
        menu.add_cascade(label="Run", menu=run)




if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
