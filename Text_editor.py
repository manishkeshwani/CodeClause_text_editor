from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('TextPad')
root.geometry("600x340")

# set variable for open file name
global open_status_name
open_status_name = False

global selected
selected=False

# Create new file function
def new_file():
    # Delete Previous text
    my_text.delete("1.0",END)
    # Update status bar
    root.title("New File")
    status_bar.config(text="New File......")

    global open_status_name
    open_status_name = False


# Open file function
def open_file():
    # Delete Previous File 
    my_text.delete("1.0",END)
    # Grab Filename
    text_file = filedialog.askopenfilename(title="Open File",
                                           initialdir="D:/Internships/CodeClause/Task 2 Text Editor/",
                                           filetypes=(("Text Files","*.txt"),
                                                      ("HTML Files","*.html"),
                                                      ("Python Files","*.py"),
                                                      ("All Files","*.*")))
    
    # Check to see if there is a file name
    if text_file:
        #make file name global so we can access it later
        global open_status_name
        open_status_name = text_file
    # Update Status bars
    name = text_file
    status_bar.config(text=name)
    name = name.replace("D:/Internships/CodeClause/Task 2 Text Editor/","")
    root.title(f"{name} - TextPad!")
    # Open the file
    text_file=open(text_file,'r')
    stuff = text_file.read()
    # Add file to textbox
    my_text.insert(END,stuff)
    # Close the opend file
    text_file.close()



# Save a file
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension='.*', 
                                             initialdir="D:/Internships/CodeClause/Task 2 Text Editor/",
                                             title="Save File",filetypes=(("Text Files","*.txt"),
                                                                          ("HTML Files","*.html"),
                                                                          ("Python Files","*.py"),
                                                                          ("All Files",'*.*')))
    if text_file:
        name = text_file
        status_bar.config(text=f"Saved : {name}......")
        name = name.replace("D:/Internships/CodeClause/Task 2 Text Editor/","")
        root.title(f"{name} - TextPad")
        
    #save the file
    text_file = open(text_file,'w')
    text_file.write(my_text.get(1.0,END))
    # Close the file
    text_file.close()

# save file
def save_file():
    global open_status_name
    if open_status_name:
        #save the file
        text_file = open(open_status_name,'w')
        text_file.write(my_text.get(1.0,END))
        # Close the file
        text_file.close()
        # Put status update or popup code
        status_bar.config(text=f"Saved : {open_status_name}......")
    else:
        save_as_file()


# Cut Text
def cut_text(e):
    global selected
    #check to see if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # grab selected text from text box
            selected = my_text.selection_get()
            # delete selected text from text box
            my_text.delete("sel.first","sel.last")
            # Clear the clipboard then append
            root.clipboard_clear()
            root.clipboard_append(selected)

# Copy Text
def copy_text(e):
    global selected
    # check to see if wee used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # grab selected text from text box
        selected = my_text.selection_get()
        # Clear the clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)

# Paste Text
def paste_text(e):
    global selected
    #check to see if keyboard shortcut is used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position,selected)


# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create our scrollbar for the text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT,fill=Y)

#Horizontal Scrollbar
hor_scroll = Scrollbar(my_frame,orient="horizontal")
hor_scroll.pack(side=BOTTOM,fill=X)

# Create Text Box
my_text = Text(my_frame,
               width=97,
               height=25,
               font=('Helvetical',16),
               selectbackground='#333333',
               selectforeground="white",
               undo=True,
               yscrollcommand=text_scroll.set,
               wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()


# Configure our Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add file to Menu
file_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_command(label="Save As",command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label="Cut     ",command=lambda: cut_text(False),accelerator="ctrl+x")
edit_menu.add_command(label="Copy     ",command=lambda: copy_text(False),accelerator="ctrl+c")
edit_menu.add_command(label="Paste     ",command=lambda: paste_text(False),accelerator="ctrl+v")
edit_menu.add_separator()
edit_menu.add_command(label="Undo     ",command=my_text.edit_undo,accelerator="ctrl+z")
edit_menu.add_command(label="Redo     ",command=my_text.edit_redo,accelerator="ctrl+y")


# Add Status Bar To Bottom of App
status_bar = Label(root,text='Ready    ',anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=15)

#Edit Bindings
root.bind('<Control-Key-x>',cut_text)
root.bind('<Control-Key-c>',copy_text)
root.bind('<Control-Key-v>',paste_text)


root.mainloop()

