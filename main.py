from tkinter import *
from tkinter import ttk
from pynput import mouse
import ctypes

color = "#000000"
width = 10

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
sf = int(user32.GetDpiForSystem()/96)

root = Tk()
root.geometry("1920x1080")
root.title("YTC Paint")
# root.config(cursor="dot")
canvas = Canvas(root, bg="white", width="1920", height="1080")
canvas.pack()

# кнопка ввода цвета
ent = ttk.Entry()
canvas.create_window(10, 20, anchor=NW, window=ent, width=100, height=40)

# кнопка ввода размера кисти
entw = ttk.Entry()
canvas.create_window(130, 20, anchor=NW, window=entw, width=100, height=40)

s = False
mx = my = 0
px = py = 0

def on_enter1(event):
    global width
    alf = "1234567890"
    wd = entw.get()
    for i in range(len(wd)):
        if wd[i] not in alf:
            break
        else:
            width = int(wd)

# логика кнопки ввода цвета
def on_enter(event):
    global color
    alf = "0123456789abcdefABCDEF"
    cl = ent.get()
    for i in range(len(cl)):
        if cl[i] not in alf or len(cl) > 6:
            break
        else:
            color = "#" + cl + "0"*(6-len(cl))

# получение координат курсора
def on_mouse_click(x, y, button, pressed):
    global mx, my, s, px, py
    if button == mouse.Button.left and pressed:
        s = True
        mx, my = x, y
        px, py = mx, my
    else:
        s = False
        px, py = None, None
def on_move(x, y):
    global mx, my
    mx, my = x, y
listener = mouse.Listener(on_click=on_mouse_click, on_move=on_move)
listener.start()

# рисовалка
def gu():
    global px, py
    ent.bind("<Return>", on_enter)
    entw.bind("<Return>", on_enter1)
    print(root.winfo_x(), root.winfo_y())
    # print(ent.get())
    if s and px is not None and py is not None:
        cx = (mx - 9 - root.winfo_x())*sf
        cy = (my - 39 - root.winfo_y())*sf
        pcx = (px - 9 - root.winfo_x())*sf
        pcy = (py - 39 - root.winfo_y())*sf
        try:
            canvas.create_line(pcx, pcy, cx, cy, fill=color, width=width, capstyle=ROUND, smooth=True)
        except:
            pass
        px, py = mx, my
    root.after(10, gu)

# старая система
# def gu():
#     if s:
#         cx = (mx - 9 - root.winfo_x())*sf
#         cy = (my - 39 - root.winfo_y())*sf
#         ent.bind("<Return>", on_enter)
#         entw.bind("<Return>", on_enter1)
#         try:
#             canvas.create_oval(cx-width, cy-width, cx+width, cy+width,fill=color,  outline=color, width=width)
#         except:
#             pass
#     root.after(1, gu)

root.after(10, gu)
root.mainloop()
