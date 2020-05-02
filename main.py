from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pygments import lex
from pygments.lexers import PythonLexer
import pyperclip
from filesystem import FileSystem
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



class Application(Frame):

    organisation = None
    password = None
    localkeys_dir = None
    windows = []
    root = None

    def __init__(self, master):
        self.master = master
        self.master.title("Molecule")
        Application.root = self.master

        Application.localkeys_dir = self.get_localkeys_dir()

        window = Application.open_new_editor_window(
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        highlightthickness=0,
        padx=20,
        pady=10,
        fg='white',
        background='#292C33')
        Application.windows.append(window)

    def open_new_editor_window(*args, **kwargs):
        master = Toplevel(Application.root) if len(Application.windows) > 0 else Application.root
        editor = CustomText(master, *args, **kwargs)
        editor.linenumbers.pack(side='left', fill='y')
        editor.pack(side='right', fill=BOTH, expand=True)
        return editor

    def get_localkeys_dir(self):
        localkeys_dir = filedialog.askdirectory(initialdir="./localkeys")
        return localkeys_dir if localkeys_dir != None else "localkeys"


class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum, fill='#435D61')
            i = self.textwidget.index("%s+1line" % i)

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self.master = args[0]

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.init_menu()

        self.linenumbers = TextLineNumbers(self.master,
        width=30,
        highlightthickness=0,
        background='#292C33')
        self.linenumbers.attach(self)

        self.bind("<<Change>>", self._on_change)
        self.bind("<Configure>", self._on_change)
        self.bind("<Key>", self._on_change)

        self.stack = []
        self.queue = []

        self.saved = False
        self.fs = FileSystem()
        self.currentFile = None

    def _on_change(self, event):
        self.linenumbers.redraw()
        if str(event.type) == "KeyPress":
            if len(self.stack) == 0 or self.get(1.0, END) != self.stack[-1]:
                if len(self.stack) > 20:
                    self.stack = self.stack[1:]
                self.queue = []
                self.stack.append(self.get("1.0", END))
            print(self.stack)

    def check_if_saved(self):
        return self.saved == self.get(1.0, END)

    def init_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="New File", command=self.new_file)
        file.add_command(label="Load File", command=self.load_file)
        file.add_command(label="Import File", command=self.import_file)
        file.add_command(label="Save File", command=self.save_file)
        file.add_command(label="Save As...", command=self.save_file_as)
        file.add_command(label="Decrypt File")
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Select All", command=self.select_all)
        edit.add_command(label="Cut", command=self.cut)
        edit.add_command(label="Copy", command=self.copy)
        edit.add_command(label="Paste", command=self.paste)
        edit.add_command(label="Copy Path", command=self.copy_file_path)
        edit.add_command(label="Toggle Comments", command=self.toggle_comments)
        edit.add_command(label="Undo", command=self.undo)
        edit.add_command(label="Redo", command=self.redo)
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
        print(self.master)
        window = Application.open_new_editor_window(width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        highlightthickness=0,
        padx=20,
        pady=10,
        fg='white',
        background='#292C33')
        Application.windows.append(window)

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
                    self.delete(1.0, END)
                    self.insert(END, decrypted_contents)
                except ValueError:
                    messagebox.showerror('Error',
                    'Credentials Invalid for the selected file')

    def import_file(self):
        if(Application.organisation == None or Application.password == None):
            # the user needs to be prompted to login first
            self.login()
        else:
            selected_file = filedialog.askopenfile(mode='r',
            initialdir='./',
            filetypes=[("python files", "*.py")])
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
                decrypted_file = open(selected_file.name, 'r')
                decrypted_contents = decrypted_file.read()
                decrypted_file.close()
                self.fs.createFile(selected_file.name, Application.organisation,
                Application.password, decrypted_contents)
                self.currentFile = selected_file.name + '.enc'
                self.delete(1.0, END)
                self.insert(END, decrypted_contents)

    def save_file(self, filename=None):
        # if filename not provided, save contents to currentFile
        if(Application.organisation == None or Application.password == None):
            self.login()
        else:
            # ask the user for a filepath
            # has to be saved as an enc file
            if (not self.saved):
                editor_text = self.get("1.0", END)
                self.saved = editor_text
                if (self.currentFile == None and filename == None):
                    self.save_file_as()
                else:
                    selected_file = self.currentFile if filename == None else filename
                    if (selected_file != None):
                        self.queue = []
                        self.fs.updateFile(selected_file,
                        editor_text,
                        Application.organisation,
                        Application.password)

    def save_file_as(self):
        selected_file = filedialog.asksaveasfilename(
        initialdir='../',
        filetypes=[("encrypted files", "*.enc")])
        if (selected_file != ''):
            self.save_file(selected_file)

    def select_all(self):
        self.event_generate("<<SelectAll>>")

    def cut(self):
        self.event_generate("<<Cut>>")

    def copy(self):
        self.event_generate("<<Copy>>")

    def paste(self):
        self.event_generate("<<Paste>>")

    def copy_file_path(self):
        if self.currentFile != None:
            pyperclip.copy(self.currentFile)

    def toggle_comments(self):
        start_line, last_line = self.get_selected_lines_indices()
        lines = self.get(start_line, last_line).split('\n')
        lines = lines[1:] if len(lines) > 1 else lines
        # if there is a single uncommented line, comment every line
        # otherwise uncomment every line
        contains_normal = False
        for line in lines:
            first_char = line[len(line) - len(line.lstrip())]
            if first_char != '#':
                contains_normal = True
                break
        output = self.add_comments(lines) if contains_normal else self.remove_comments(lines)
        self.delete(start_line, last_line)
        out_lines = '\n'.join(output)+'\n' if len(output) > 1 else output[0]
        self.insert(start_line, out_lines)

    def get_selected_lines_indices(self):
        try:
            start_line = self.index(SEL_FIRST).split('.')[0]+".0"
            last_line = str(int(self.index(SEL_LAST).split('.')[0])+1)+".0"
            return start_line, last_line
        except:
            start_line = self.index('insert linestart')
            last_line = self.index('insert lineend')
            return start_line, last_line

    def add_comments(self, lines):
        # append a '# ' at the start of each line
        return list(map(lambda line: '# '+line, lines))

    def remove_comments(self, lines):
        return list(map(lambda line: line[2:] if line[:2] == '# ' else line, lines))

    def undo(self):
        if len(self.stack) > 0:
            self.queue = [self.get("1.0", END)] + self.queue
            self.delete("1.0", END)
            state = self.stack.pop()
            self.insert("1.0", state)

    def redo(self):
        if len(self.queue) > 0:
            self.delete("1.0", END)
            state = self.queue[0]
            self.queue = self.queue[1:]
            self.insert("1.0", state)
            self.stack.append(state)

    def login(self):
        # prompt the user for an organisation name and password
        self.configure(state=DISABLED)
        popup = LoginOrganisationCredentials(self.master, Application.localkeys_dir, self)

    def create_organisation(self):
        # prompt the user for an organisation name and password
        self.configure(state=DISABLED)
        popup = CreateOrganisationCredentials(self.master, Application.localkeys_dir, self)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = None
        try:
            result = self.tk.call(cmd)
        except Exception:
            print("Some Exception")

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

# class Example(Frame):
#     def __init__(self, *args, **kwargs):
#         Frame.__init__(self, *args, **kwargs)
#         self.text = CustomText(self)
#         self.vsb = Scrollbar(orient="vertical", command=self.text.yview)
#         #self.text.configure(yscrollcommand=self.vsb.set)
#         #self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
#         self.linenumbers = TextLineNumbers(self, width=30)
#         self.linenumbers.attach(self.text)
#
#         self.vsb.pack(side="right", fill="y")
#         self.linenumbers.pack(side="left", fill="y")
#         self.text.pack(side="right", fill="both", expand=True)
#
#         self.text.bind("<<Change>>", self._on_change)
#         self.text.bind("<Configure>", self._on_change)
#
#         #self.text.insert("end", "one\ntwo\nthree\n")
#         #self.text.insert("end", "four\n",("bigfont",))
#         #self.text.insert("end", "five\n")
#
#     def _on_change(self, event):
#         self.linenumbers.redraw()


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
    #Example(root).pack(side="top", fill="both", expand=True)
    #root.mainloop()
