from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from filesystem import FileSystem

# constants are declared here
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 70

class CreateOrganisationCredentials():

    def __init__(self, master, keydirpath):
        self.keydirpath = keydirpath
        self.master = Toplevel(master)
        self.master.title("Organisation Credentials")
        self.canvas = Canvas(self.master,
        highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.configure(background='#2D2D2D')

        self.name = Label(self.master, text="Name:")
        self.name.place(relx=0.1, rely=0.1)
        self.nameVal = Entry(self.master)
        self.nameVal.place(relx=0.3, rely=0.1)

        self.password = Label(self.master, text="Password:")
        self.password.place(relx=0.0, rely=0.4)
        self.passwordVal = Entry(self.master)
        self.passwordVal.place(relx=0.3, rely=0.4)

        self.enter = Button(self.master, text='Create', command=self.create)
        self.enter.place(relx=0.45, rely=0.7)

    def create(self):
        organisation = self.nameVal.get()
        password = self.passwordVal.get()
        if (len(organisation) == 0 or len(password) == 0):
            messagebox.showerror("Error", "Please provide valid inputs for organisation and password!")
        else:
            fs = FileSystem(self.keydirpath)
            fs.createOrganisation(organisation, password)
            self.master.destroy()


class Application(object):

    def __init__(self, master):
        self.master = master
        self.master.title("Molecule")

        self.init_menu()
        self.editor = Text(self.master,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        highlightthickness=0,
        padx=20,
        fg="white",
        background="#292C33")
        self.editor.pack()

        # represents whether the current text in the editor is saved or not
        self.saved = False

        self.localkeys_dir = self.get_localkeys_dir()

        self.fs = FileSystem(self.localkeys_dir)

        self.organisation = None
        self.password = None

    def get_localkeys_dir(self):
        localkeys_dir = filedialog.askdirectory(initialdir="./")
        return localkeys_dir if localkeys_dir != None else "localkeys"

    def init_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="New File", command=self.new_file)
        file.add_command(label="Load File", command=self.load_file)
        file.add_command(label="Import File", command=self.load_file)
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
        organisation.add_command(label="Create Organisation", command=self.create_organisation)
        organisation.add_command(label="View Organisations")
        menu.add_cascade(label="Organisation", menu=organisation)

        run = Menu(menu)
        run.add_command(label="Run")
        run.add_command(label="Run with Arguments")
        menu.add_cascade(label="Run", menu=run)

        help = Menu(menu)
        help.add_command(label="Instructions")
        help.add_command(label="Welcome Guide")
        menu.add_cascade(label="Help", menu=help)

    def new_file(self):
        # open a new tab/window of the editor
        pass

    def load_file(self):
        # ask the user to select a file
        # change the initialdir arg later
        selected_file = filedialog.askopenfile(mode='r',
        initialdir='./',
        filetypes=[("encrypted files", "*.enc")])
        if(selected_file != None):
            pass

    def create_organisation(self):
        # prompt the user for an organisation name and password
        print('here1')
        popup = CreateOrganisationCredentials(self.master, self.localkeys_dir)



if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
