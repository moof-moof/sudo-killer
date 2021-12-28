#!/usr/bin/python3

########################################################################
## SUDOKiller, a sudoku solver
## Copyright (C) 2021  Loxia labs
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details:
## <http://www.gnu.org/licenses/>.
##
##
## The actual, rather elegant, solving algorithm relied upon in this 
## application -- comprising functions possible() and solve() below --
## was demonstrated by Professor Thorsten Altenkirch in the Computerphile
## episode <https://youtu.be/G_UYXzGuqvM>, and can thus be considered
## to be in the public domain.
## 
########################################################################


import tkinter as tk
from tkinter import ttk
from tkinter import Menu, messagebox as tkmb
import math
import numpy as np
import os


root = tk.Tk()
root.geometry("400x420+1000+300")
root.title('SUDOKiller')
root.resizable(0, 0)
ikon = tk.PhotoImage(file='gif/sol.gif')
root.call('wm', 'iconphoto', root._w, ikon)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

grid_bg =       '#FFF8BF'
tint_bg =       '#EBFAFF'
my_menubg =     '#FFFFFF'
my_active_bg =  '#2589FF'           # menu-item hover Flag-Blue
my_active_fg =  '#FFFFFF'           # menu-item hover contrast (white)
my_fg =         '#222222'           # text default off-black

root.tk_setPalette(
    background = grid_bg,                   # widget base-bg
    foreground = my_fg,                     # widget text 
    activeBackground = my_active_bg,        # hover bg
    activeForeground = my_active_fg         # hover fg
    )

# Define the Entry widget style:
style_ent = ttk.Style()
style_ent.configure('Tint.TEntry', fieldbackground = tint_bg)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


""" Configure the grid 
---------------------------------------------------------------------"""
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1) 
root.columnconfigure(6, weight=1)
root.columnconfigure(7, weight=1)
root.columnconfigure(8, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)


""" Declare global variables and lists 
---------------------------------------------------------------------"""
rcount = tk.IntVar()
kcount = tk.IntVar()
kcount = 0

entries= [] # Create an empty "single-dimension" list (Entry-widget references)
data1D = [] # Create another empty "1D" list (returned solution values)
data2D = [[0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9)] # Create a populated 2D list (solver's i/o data)



""" Generate and save references to 81 Entry-widgets, 
    representing a standard sudoku table: 
---------------------------------------------------------------------"""
for rad in range(9):
    
    rcount = 0
    kcount += 1
    if math.floor((kcount - 1)/3) != 1:             ## Rows 1-3, 7-9
        
        for kol in range(9):
            
            rcount += 1
            if math.floor((rcount - 1)/3) == 1:     ## Columns 4-6
                cell = ttk.Entry(
                    root, 
                    width = 2, 
                    justify = tk.CENTER, 
                    font = ('Monospace', 21), 
                    style = 'Tint.TEntry')
            else:
                cell = ttk.Entry(
                    root, 
                    width = 2, 
                    justify = tk.CENTER, 
                    font = ('Monospace', 21))
                cell.focus_set()
                
            cell.grid(column = kol, row = rad, padx = 2, pady = 5)
            entries.append(cell)
    else:                                           ## Rows 4-6
        
        for kol in range(9):

            rcount += 1
            if math.floor((rcount - 1)/3) == 1:     ## Columns 1-3, 7-9
                cell = ttk.Entry(
                    root, 
                    width = 2, 
                    justify = tk.CENTER, 
                    font = ('Monospace', 21))
            else:
                cell = ttk.Entry(
                    root, 
                    width = 2, 
                    justify = tk.CENTER, 
                    font = ('Monospace', 21), 
                    style = 'Tint.TEntry') 
                
            cell.grid(column = kol, row = rad, padx = 2, pady = 5)
            entries.append(cell)



""" Collect the user entered unsolved pattern of numbers: 
---------------------------------------------------------------------"""
def get_input():

    for line in range(9):                   # Each row 
        for entry in range(9):              # Each cell 
           
            n = ((9 * line) + entry)        # Compute position in 1D number array (0 to 80)  
            val = entries[n].get()          # Collect that position's value
            if val == '':
                val = '0'                   # Fill blanks with naughts
            data2D[line][entry] = int(val)  # Feed the data2D list with all 81 known values
            
    print("Done collecting input\n")



## LLLLLLLLLLLLLLLLLLLLLLL  Solver algorithm  LLLLLLLLLLLLLLLLLLLLLLLLLL

def possible(y,x,n):
    for i in range(0, 9):
        if data2D [y][i] == n: 
            return False
    for i in range(0, 9) :
        if data2D [i][x] == n:
            return False
    x0 = (x//3) * 3
    y0 = (y//3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if data2D[y0+i][x0+j] == n:
                return False
    return True


def solve():
    for y in range(9):
        for x in range(9):
            if data2D[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        data2D[y][x] = n
                        solve()
                        data2D[y][x] = 0
                return
    print("One of possibly many solutions:")
    print('\a')                         # Rings terminal bell (sometimes)
    os.system('spd-say "solved okay"')  # Robotic speech fedback    
    
    for m in range(9):
        for n in range(9):
             v = data2D[m][n] 
             data1D.append(v)
    
    # Finally repopulate table with solution:
    for n in range(81):             
        entries[n].delete(0,"end")
        entries[n].insert(0,data1D[n])
    
    input("Look for more solutions?")   # Stalls program execution

## LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL


""" Kickoff function. Called from File > Solve menu command 
---------------------------------------------------------------------"""
def run_all():
    get_input()
    solve()




def open_file():
    pass            # (Just a dummy command for now)



"""  Menu-bar and menus
---------------------------------------------------------------------"""
menu = tk.Menu(
    root, 
    bg = my_menubg, 
    border = 2, 
    font = 'Virtue 11')
    
root.configure(menu = menu, pady = 0)

# File
file_menu = tk.Menu(menu, tearoff=0, bg=my_menubg, font='Calvin')
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Solve', command=run_all)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=root.destroy)


# Help
help_menu = tk.Menu(menu, tearoff=0, bg=my_menubg, font='Calvin')
menu.add_cascade(label = 'Help', menu = help_menu)
help_menu.add_command(
    label = 'About',
    command = lambda: tkmb.showinfo(
        'About', '    SUDOKiller\na Sneaky S*d*k* Solver'))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

root.mainloop()
