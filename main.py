from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from filesystem import FileSystem
from pygments import lex
from pygments.lexers import PythonLexer
from lexer import *

# constants are declared here
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 70

class CreateOrganisationCredentials():

    def __init__(self, master, keydirpath, editor):
        self.editor = editor
        self.keydirpath = keydirpath
        self.master = Toplevel(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
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
            # change the currently logged in organisation
            Application.organisation, Application.password = organisation, password
            self.editor.configure(state=NORMAL)
            self.master.destroy()

    def on_closing(self):
        self.editor.configure(state=NORMAL)
        self.master.destroy()


class LoginOrganisationCredentials():

    def __init__(self, master, keydirpath, editor):
        self.editor = editor
        self.keydirpath = keydirpath
        self.master = Toplevel(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
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

        self.enter = Button(self.master, text='Login', command=self.validate)
        self.enter.place(relx=0.45, rely=0.7)

    def validate(self):
        organisation = self.nameVal.get()
        password = self.passwordVal.get()
        if (len(organisation) == 0 or len(password) == 0):
            messagebox.showerror("Error", "Please provide valid inputs for organisation and password!")
        else:
            fs = FileSystem(self.keydirpath)
            try:
                fs.getOrganisationKey(organisation, password)
                # change the currently logged in organisation
                Application.organisation, Application.password = organisation, password
                messagebox.showinfo(title="Success",
                message="Successfully logged in to "+organisation)
                self.editor.configure(state=NORMAL)
                self.master.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", "Organisation not found!")
            except ValueError:
                messagebox.showerror("Error", "Invalid Password!")


    def on_closing(self):
        self.editor.configure(state=NORMAL)
        self.master.destroy()



class Application(object):

    organisation = None
    password = None

    def __init__(self, master):
        self.master = master
        self.master.title("Molecule")

        self.init_menu()
        self.editor = Text(self.master,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        highlightthickness=0,
        padx=20,
        pady=20,
        fg="white",
        background="#292C33")
        self.editor.pack()

        self.master.bind('<KeyRelease>', self.text_changed)

        # represents whether the current text in the editor is saved or not
        self.saved = False

        self.localkeys_dir = self.get_localkeys_dir()

        self.fs = FileSystem(self.localkeys_dir)

        Application.organisation = None
        Application.password = None

        self.currentFile = None

    def get_words(self, text):
        return get_words

    def text_changed(self, event):
        if((event.keycode >= 97 and event.keycode <= 122) or
        (event.keycode >= 65 and event.keycode <= 90)):
            editor_text = self.editor.get("1.0", END)
            #self.editor.tag_add("import", "1.0", "1.6")
            #self.editor.tag_config("import", foreground="blue")
            #lines = editor_text.split('\n')[:-1]
            #print(lines)
            line = self.editor.get('end - 1 lines linestart', 'end - 1 lines lineend')
            line_num = self.editor.index(INSERT)
            line_num_start = float(line_num.split('.')[0]+".0")

            print(line_num, line)
            line_data = getColours(line)
            print(line_data)
            for datapoint in line_data:
                if datapoint[1] != '':
                    word_start_index = line_num_start + float('0.'+(str(datapoint[0])))
                    word_end_index = line_num_start + float('0.'+(str(datapoint[0])))
                    colour = datapoint[2]
                    print('(',word_start_index,', ',word_end_index,'): '+colour)
                    self.editor.tag_add(str(datapoint[3]), str(word_start_index), str(word_end_index))
                    self.editor.tag_config(str(datapoint[3]), background=colour)
                    print()
                    print()
                    print()
            '''for (index, line) in enumerate(lines):
                print(index, line, 'here')
                line_start = self.editor.get(str(index+1)+".0")
                line_end = str(index+1)+"."+str(len(line))
                line_data = getColours(line)
                for datapoint in line_data:
                    startindex = str(index+1)+"."+str(datapoint[0])
                    endindex = str(index+1)+"."+str(datapoint[1])
                    self.editor.tag_add(str(datapoint[3]), startindex, endindex)
                    colour = datapoint[2]
                    print('('+startindex+', '+endindex+'): '+colour)
                    self.editor.tag_config(str(datapoint[3]), background=colour)'''

    def get_localkeys_dir(self):
        localkeys_dir = filedialog.askdirectory(initialdir="./localkeys")
        return localkeys_dir if localkeys_dir != None else "localkeys"

    def init_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="New File", command=self.new_file)
        file.add_command(label="Load File", command=self.load_file)
        file.add_command(label="Import File", command=self.load_file)
        file.add_command(label="Save File")
        file.add_command(label="Save As...")
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
        organisation.add_command(label="Login", command=self.login)
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
        print(Application.organisation, Application.password)
        if(Application.organisation == None or Application.password == None):
            # the user needs to be prompted to login first
            self.login()
        else:
            selected_file = filedialog.askopenfile(mode='r',
            initialdir='./',
            filetypes=[("encrypted files", "*.enc")])
            if(selected_file != None):
                # need to save the current file before proceeding
                if((not self.saved) and self.currentFile != None):
                    # prompt the user asking them if they would like to save their changes
                    resp = messagebox.askquestion("Save current file",
                    "You have some unsaved changes in your current file. Would you like to save it?",
                    icon='warning')
                    if resp == 'yes':
                        # save the current contents of the file
                        pass
                # show the decrypted contents to the user
                print(selected_file.name)
                try:
                    decrypted_contents = self.fs.readFile(selected_file.name,
                    Application.organisation,
                    Application.password)
                    print(decrypted_contents)
                    self.currentFile = selected_file.name
                    self.editor.delete(1.0, END)
                    self.editor.insert(END, decrypted_contents)
                except ValueError:
                    messagebox.showerror('Error',
                    'Credentials Invalid for the selected file')


    def login(self):
        # prompt the user for an organisation name and password
        self.editor.configure(state=DISABLED)
        popup = LoginOrganisationCredentials(self.master, self.localkeys_dir, self.editor)

    def create_organisation(self):
        # prompt the user for an organisation name and password
        self.editor.configure(state=DISABLED)
        popup = CreateOrganisationCredentials(self.master, self.localkeys_dir, self.editor)


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
