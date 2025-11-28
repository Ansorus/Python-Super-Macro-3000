from tkinter import *
from tkinter import  ttk

def option_box(question, options, values, wrap=1, direction='vertical'):
    box = Toplevel(width=300, height=300)
    box.grid_columnconfigure(0, weight=1)
    box.grid_rowconfigure(0, weight=1)

    question = ttk.Label(box, text=question, anchor='center', justify='center', font=('Arial', 18))
    question.grid(row=0, column=0, sticky="N")

    answer = StringVar(value=options[0])

    i = 1
    for option in options:
        filling = int((i-1)/wrap)
        wrapping = (i-1)%wrap

        column = wrapping if direction == 'vertical' else filling
        row = (filling if direction == 'vertical' else wrapping)+1

        widget = Radiobutton(box, text=option, variable=answer, value=values[i-1], font=('Arial', 12))
        widget.grid(row=row, column=column)
        if i == 1:
            widget.select()
        i += 1

    confirm_button = Button(box, text='Confirm', font=('Arial', 12), command=box.quit)
    confirm_button.grid(row=i, column=0)
    box.mainloop()
    box.destroy()
    return answer.get()

# class OptionBox:
#     def __init__(self, question, options):
#         box = Toplevel(width=300,height=300)
#         box.grid_columnconfigure(0, weight=1)
#         box.grid_rowconfigure(0, weight=1)
#
#         question = ttk.Label(box, text=question ,anchor='center',justify='center', font=('Arial', 18))
#         question.grid(row=0, column=0, sticky="N")
#
#         answer = StringVar()
#
#         i = 1
#         for option in options:
#             widget = Radiobutton(box, text=option, variable=answer, value=option, font=('Arial', 12))
#             widget.grid(row=i,column=0)
#             if i==1:
#                 widget.select()
#             i += 1
#
#         confirm_button = Button(box,text='Confirm',font=('Arial', 12), command=confirmed)
#         confirm_button.grid(row=i,column=0)
#
#     def confirmed(self):
#         box.destroy()