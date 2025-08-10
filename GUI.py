import tkinter as tk
from tkterminal import Terminal
from PIL import Image, ImageTk
import os
from tkinter import Text

window = tk.Tk()
# window.configure(background='black')
window.title('AI Chatbot with SA')
window.geometry('1200x800')

# Load the image
image=Image.open('bg.png')

# Resize the image in the given (width, height)
img=image.resize((1200, 800))

# Conver the image in TkImage
bg=ImageTk.PhotoImage(img)

label1 = tk.Label(master=window, image=bg)
label1.place(x=0, y=0)

stream = os.popen('echo Returned output')
output = stream.read()

title = tk.Label(master=window, text='AI Chatbot with SA', borderwidth=10, font=('Arial', 25), fg='#003556')
title.place(x=400, y=650)

terminal = Terminal(pady=5, padx=5, height=25, font=1, borderwidth=30, foreground='white', background='black', selectbackground='white')
terminal.pack(expand=False, fill='both')
terminal.shell = True

# Create text widget and specify size.
# T = Text(window, height = 35, width = 137)
# T.place(x=50, y=50)

# stream = os.popen('rasa shell')
# output = stream.read()
# T.insert(tk.END, output)

window.mainloop()