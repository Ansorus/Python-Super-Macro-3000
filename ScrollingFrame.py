import tkinter
from tkinter import *
from tkinter import font

chars_fitted = 1+10+10+10+1

def contentize_string(text, width, text_font: font.Font):
    left_text = f" :: {text}"

    left_size = text_font.measure(left_text)
    right_size = text_font.measure('X')

    pixels_to_fill = width - right_size - left_size
    unit = text_font.measure(" ")
    space = [' '] * int(pixels_to_fill / unit - 1)

    full_text = [left_text] + space + ['X']
    return ''.join(full_text)

def decontentize_string(string):
    size = len(string)
    stop = 0
    for i in range(size - 2, 0, -1):
        if string[i] != ' ':
            stop = i + 1
            break
    return string[4:stop]

class ScrollingFrame:
    def __init__(self, list_box: Listbox, root: Tk, command = lambda x:x):
        self.root = root
        self.box = list_box
        self.font = font.Font(font=self.box.cget("font"))
        self.box.update()
        self.width: int = self.box.winfo_width()

        self.box.bind('<Double-1>', lambda event: self.double_clicked(command))
        self.box.bind("<Button-1>", self.select_element)
        self.box.bind("<B1-Motion>", self.shift_element)
        self.box.bind("<ButtonRelease-1>", self.mouse_released)
        self.box.bind("<Motion>", self.mouse_move)
        self.box.bind("<Leave>",self.mouse_leave)

        self.selected = None
        self.dragging = False
    def mouse_move(self, event):
        if 30 > event.x > 0:
            self.root.config(cursor="fleur")
        elif event.x > 450-18*2:
            self.root.config(cursor="right_ptr")
        else:
            self.root.config(cursor="arrow")
    def mouse_leave(self,event):
        self.root.config(cursor="arrow")
    def mouse_released(self, event):
        self.dragging = False
        self.selected = None
    def new_element(self, text):
        full_text = contentize_string(text, self.width, self.font)
        self.box.insert(self.box.size(), ''.join(full_text))
    def select_element(self, event:Event):
        if event.x<30:
            self.selected = self.box.nearest(event.y)
        if event.x > 450-18*2:
            self.box.delete(self.box.nearest(event.y))
    def shift_element(self, event):
        selected = self.selected
        if selected is None:
            return
        i = self.box.nearest(event.y)
        if i < selected:
            contents = self.box.get(i)
            self.box.delete(i)
            self.box.insert(i+1,contents)
        if i > selected:
            contents = self.box.get(i)
            self.box.delete(i)
            self.box.insert(i-1, contents)
        self.selected = i
    def get_items(self):
        items = self.box.get(0,tkinter.END)
        sliced_items = []
        for item in items:
            sliced_items.append(decontentize_string(item))
        return sliced_items
    def double_clicked(self, command):
        index = self.box.curselection()[0]
        contents = self.box.get(index)
        command(index, decontentize_string(contents))
    def edit_element(self, index, new_string):
        self.box.delete(index)
        full_text = contentize_string(new_string, self.width, self.font)
        self.box.insert(index, full_text)