from tkinter import *
from tkinter import ttk
from ScrollingFrame import ScrollingFrame
from OptionBox import option_box
from macro import follow_command, everything
from tkinter import simpledialog
from tkinter import messagebox

# -- WINDOW SETUP -- #
window = Tk()
window.title("Super Macro 3000")
window.geometry('500x500-25+25')
window.resizable(True,True)

left = ttk.Frame(window,width=25,height=500)
left.grid(column=0,row=0, rowspan=4) # Change this if grid Y size changes

options = [(everything[command]['OptionText'] if 'OptionText' in everything[command] else command) for command in everything.keys()]
values = [(everything[command]['DefaultValue'] if 'DefaultValue' in everything[command] else command) for command in everything.keys()]

# -- INPUT FUNCTIONS -- #
def add_command():
    answer = option_box("What command are you adding?", options, values)
    scrolling_frame.new_element(answer)

def play_macro():
    global scrolling_frame
    items = scrolling_frame.get_items()
    for item in items:
        follow_command(item)

def edit_element(index, element: str):
    global scrolling_frame
    start = element.split('(')[0]
    command = everything[start]

    if not 'Settings' in command:
        return
    element_settings = command['Settings'](element)

    if 'Values' in element_settings:
        answer = option_box(element_settings['Prompt'], element_settings['Values'],  element_settings['Values'], element_settings['Wrap'], element_settings['Direction'])
        success = command['Edit'](answer)
        scrolling_frame.edit_element(index, success)
        return


    answer = simpledialog.askstring(title="Edit Command", prompt=element_settings['Prompt'], initialvalue=element_settings['InitialValue'])
    success = command['Edit'](answer)
    if success is False:
        messagebox.showerror("Value Error", element_settings['Error'])
        return
    scrolling_frame.edit_element(index, success)

# -- UI SETUP -- #
title = ttk.Label(window, text="Super Macro 3000", font=('Arial', 25))
title.grid(column=1,row=0, columnspan=2)

# Scrolling Frame
outer_box = ttk.Frame(window, width=500-25*2,height=300)
outer_box.grid(column=1,row=2,columnspan=2)

list_box = Listbox(outer_box, font=('Arial',10), selectmode=SINGLE)
list_box.place(x=0,y=0,width=500-25*2, height=outer_box.cget('height'))
scrolling_frame = ScrollingFrame(list_box, window, command=edit_element)

# Buttons
add = ttk.Button(window, text="Add Command", command=add_command)
add.grid(column=1,row=1)
record = ttk.Button(window, text="Cool Button")
record.grid(column=2,row=1)

# Play Button
play = Button(window, text="Play", command=play_macro)
play.grid(column=1,row=3,columnspan=2)

window.mainloop()