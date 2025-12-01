from tkinter import Tk, Button, Listbox, SINGLE
from tkinter import ttk
from ScrollingFrame import ScrollingFrame
from OptionBox import option_box
from macro import follow_command, everything
from tkinter import simpledialog
from tkinter import messagebox
from pynput import keyboard

# -- WINDOW SETUP -- #
window = Tk()
window.title("Super Macro 3000")
#window.geometry('500x500-25+25')
window.resizable(True,True)

left = ttk.Frame(window,width=25,height=500)
left.grid(column=0,row=0, rowspan=5) # Change this if grid Y size changes

right = ttk.Frame(window,width=25,height=500)
right.grid(column=3,row=0, rowspan=5)

options = [(everything[command]['OptionText'] if 'OptionText' in everything[command] else command) for command in everything.keys()]
values = [(everything[command]['DefaultValue'] if 'DefaultValue' in everything[command] else command) for command in everything.keys()]

# -- INPUT FUNCTIONS -- #
loop = 'OFF'
def toggle_loop():
    global loop, loop_button
    loop = 'ON' if loop == 'OFF' else 'OFF'
    loop_button.config(text='Loop: ' + loop)

def add_command():
    answer = option_box("What command are you adding?", options, values)
    scrolling_frame.new_element(answer)

playing = False
def play_macro():
    global scrolling_frame
    global play, playing

    playing = True
    play.config(text='F1: Stop')
    play.update()

    items = scrolling_frame.get_items()
    while True:
        for item in items:
            follow_command(item)
            if not playing:
                break
        if loop == 'OFF' or not playing:
            break
    playing = False
    play.config(text='Play')
    play.update()

def stop_macro(key, injected):
    if not injected:
        if key == keyboard.Key.f1:
            global playing
            playing = False

listener = keyboard.Listener(on_release=stop_macro)
listener.start()

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
loop_button = ttk.Button(window, text="Loop: OFF", command=toggle_loop)
loop_button.grid(column=2,row=1)

# F1 to Stop instruction
label = ttk.Label(window, text='F1 to stop the macro', font=('Arial', 10))
label.grid(column=1, row=3, columnspan=2)

# Play Button
play = Button(window, text="Play", command=play_macro)
play.grid(column=1,row=4,columnspan=2)

window.mainloop()