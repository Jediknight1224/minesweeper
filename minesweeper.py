import os, configpy, time, mysqldb
import tkinter as tk
import fieldinit as finit
from tkinter import messagebox, simpledialog

window = tk.Tk()

window.title("Minesweeper")

rows, cols, mines, start_time = 10, 10, 10, 0
field, buttons, mine_counter, custom_sizes = [], [], [], []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
gameover = False
mine_c = mines
name = ""


def create_menu():
    menubar = tk.Menu(window)
    menusize = tk.Menu(window, tearoff=0)
    menusize.add_command(label = "small (10x10 with 10 mines)", command = lambda: set_size(10, 10, 10))
    menusize.add_command(label = "medium (20x20 with 40 mines)", command = lambda: set_size(20, 20, 40))
    menusize.add_command(label = "big (35x35 with 120 mines)", command = lambda: set_size(35, 35, 120))
    menusize.add_command(label = "custom", command = set_custom_size)
    menusize.add_separator()
    for x in range(0, len(custom_sizes)):
        menusize.add_command(label = str(custom_sizes[x][0]) + "x" + str(custom_sizes[x][1]) + " with " + str(custom_sizes[x][2]) + " mines", command = lambda x = x, custom_sizes = custom_sizes: set_size(custom_sizes[x][0], custom_sizes[x][1], custom_sizes[x][2]))
    menubar.add_cascade(label = "Size", menu = menusize)
    menubar.add_command(label = "Exit", command = lambda: window.destroy())
    window.config(menu = menubar)


def set_custom_size():
    global custom_sizes
    r, c, m = 0, 0, 0
    while r < 5 or r > 50:
        r = tk.simpledialog.askinteger("Custom size", "Enter number of rows(min: 5, max: 50)")
    while c < 5 or c > 50:
        c = tk.simpledialog.askinteger("Custom size", "Enter number of columns(min: 5, max: 50")
    while m < 1 or m > r*c:
        m = tk.simpledialog.askinteger("Custom size", f"Enter number of mines(min: 1, max:{r*c})")
    custom_sizes.insert(0, (r,c,m))
    custom_sizes = custom_sizes[0:5]
    set_size(r,c,m)
    create_menu()

def set_size(r,c,m):
    global rows, cols, mines
    rows, cols, mines = r, c, m
    configpy.saveConfig(rows, cols, mines, custom_sizes)
    restart_game()

def prepare_window():
    global rows, cols, buttons, mine_c, mines, mine_counter, start_time, name
    name = tk.simpledialog.askstring("User", "Enter your username")
    start_time = time.time()
    mine_c = mines
    mine_counter.clear()
    tk.Button(window, text = "Highscore", activebackground = "green", command = lambda: mysqldb.disp_highscores(rows, cols, mines)).grid(row = 0, column = 0, columnspan = cols - cols//2, sticky = tk.N+tk.W+tk.S+tk.E)
    tk.Button(window, text = "Restart", activebackground = "red", command = restart_game).grid(row = 0, column = cols - cols//2, columnspan = cols//2, sticky = tk.N+tk.W+tk.S+tk.E)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tk.Button(window, text = " ", width = 2, command = lambda x = x, y = y: on_left_click(x, y))
            b.bind("<Button-3>", lambda e, x = x, y = y: on_right_click(x, y))
            b.config(background = "black", activebackground = "green")
            b.grid(row = x+1, column = y, sticky = tk.N+tk.W+tk.S+tk.E)
            buttons[x].append(b)
    m = tk.Label(window, text = "Mines: " + str(mine_c))
    m.grid(row = rows + 2, column = 0, columnspan = cols//2, sticky = tk.W)
    mine_counter.append(m)

def restart_game():
    global gameover, rows, cols, mines, field, mine_c
    gameover = False
    for x in window.winfo_children():
        if type(x) != tk.Menu:
            x.destroy()
    prepare_window()
    field = finit.prepare_game(rows, cols, mines)

def show_mines():
    global rows, cols
    for _x in range(0, rows):
        for _y in range(cols):
            if field[_x][_y] == -1:
                buttons[_x][_y]["text"] = u"\U0001F4A3"
                buttons[_x][_y]["fg"] = "white"

def on_left_click(x,y):
    global field, buttons, colors, gameover, rows, cols
    if gameover:
        return
    buttons[x][y]["text"] = str(field[x][y])
    if field[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background = 'red', disabledforeground = 'black')
        gameover = True
        show_mines()
        tk.messagebox.showinfo("Game Over", "You have lost.")        
    else:
        buttons[x][y].config(disabledforeground = colors[field[x][y]])
    if field[x][y] == 0:
        buttons[x][y]["text"] = " "
        empty_cell_click(x,y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief = tk.SUNKEN)
    check_for_win()

def empty_cell_click(x,y):
    global field, buttons, colors, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return
    if field[x][y] != 0:
        buttons[x][y]["text"] = str(field[x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground = colors[field[x][y]])
    buttons[x][y].config(relief = tk.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if field[x][y] == 0:
        if x != 0 and y != 0:
            empty_cell_click(x-1,y-1)
        if x != 0:
            empty_cell_click(x-1,y)
        if x != 0 and y != cols-1:
            empty_cell_click(x-1,y+1)
        if y != 0:
            empty_cell_click(x,y-1)
        if y != cols-1:
            empty_cell_click(x,y+1)
        if x != rows-1 and y != 0:
            empty_cell_click(x+1,y-1)
        if x != rows-1:
            empty_cell_click(x+1,y)
        if x != rows-1 and y != cols-1:
            empty_cell_click(x+1,y+1)

def on_right_click(x,y):
    global buttons, mine_counter, mine_c
    if gameover:
        return
    if buttons[x][y]["text"] == "?":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
        mine_c += 1
        mine_counter[0]["text"] = "Mines: " + str(mine_c)
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "?"
        buttons[x][y]["state"] = "disabled"
        mine_c -= 1
        mine_counter[0]["text"] = "Mines: " + str(mine_c)
    
def check_for_win():
    global buttons, field, rows, cols, start_time, name, mines
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        show_mines()
        final_time = int(time.time() - start_time)
        mysqldb.insert_score(name, final_time, rows, cols, mines)
        tk.messagebox.showinfo("Gave Over", f"You have won.\nYour final time is {final_time//60} minutes {final_time%60} seconds")

if os.path.exists("config.ini"):
    rows, cols, mines = configpy.loadConfig(custom_sizes)
else:
    configpy.saveConfig()

create_menu()
prepare_window()
field = finit.prepare_game(rows, cols, mines)
window.mainloop()