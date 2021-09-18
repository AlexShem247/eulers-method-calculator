import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from math import *


def drawTable():
    """Performs calculations and draws table"""
    global x, y, h, r, dydxr, tableWin, canvas, table_data, equation, dp, xValues, yValues
    # Define values
    equation = equationEntry.get()
    x = xEntry.get()
    y = yEntry.get()
    xI = xIEntry.get()
    yI = yIEntry.get()
    iterations = iterationsEntry.get()
    h = hEntry.get()
    dp = dpEntry.get()
    
    # Error Checking
    try:
        # Converts data to correct type
        if equation == "": equation = None
        if x == "": x = None
        else: x = float(x)
        if y == "": y = None
        else: y = float(y)
        if xI == "": xI = None
        else: xI = float(xI)
        if yI == "": yI = None
        else: yI = float(yI)
        if iterations == "": iterations = None
        else: iterations = int(iterations)
        if h == "":h = None
        else: h = float(h)
        if dp == "": dp = None
        else: dp = int(dp)
        eval(equation)
        
    except Exception:
        tk.messagebox.showerror("Error", "Incorrectly formated input")
        
    else:
        if equation == None or x == None  or y == None  or ((xI == None and yI == None) and (iterations == None or h == None)) :
            tk.messagebox.showwarning("Warning", "Missing Fields")
        else:      
            # If the iteration is not specified
            if not iterations and h:
                if xI: # If xI was give
                    iterations = int((xI-x)/h)
                elif yI: # If xY was given
                    iterations = int((yI-y)/h)
            
            # If h is not specified
            elif not h and iterations:
                if xI: # If xI was given
                    h = round((xI-x)/iterations, dp)
                elif yI: # If xY was given
                    h = round((yI-y)/iterations, dp)

            # If iteration and h is given, but not final x/y value given
            elif h and iterations and not xI and not yI:
                h = h
                iterations = iterations
            
            # If iteration and h not specifed, but final x/y value given
            elif not h and not iterations:
                if xI: # If xI was given
                    h = round((xI-x)/eval(equation), dp)
                    iterations = int((xI-x)/h)
                elif yI: # If xY was given
                    h = round((yI-y)/eval(equation), dp)
                    iterations = int((yI-y)/h)
            else:
                tk.messagebox.showwarning("Warning", "Too many inputs!\n\nIgnoring xᵢ and/or yᵢ")
                
            table_data = [["h", "r", "xᵣ", "yᵣ", "(dy/dx)ᵣ"]]
            xValues = []
            yValues = []
            
            for r in range(iterations+1):
                dydxr = eval(equation) # Inserts x and y into equation
                table_data.append([h, r, round(x, dp), round(y, dp), round(dydxr, dp)]) # Adds to table
                xValues.append(x) # Add to graph
                yValues.append(y)
                
                # Calculates xr and yr for next iteration
                x += h
                y = y + h*dydxr 
            
            # Creates table
            tableWin = tk.Toplevel()
            tableWin.geometry("400x400")
            
            tk.Button(tableWin, text="Add another iteration",
                      font="Arial 14", fg="white", bg="gray40", command=newIteration).pack(padx=20, pady=10)
            
            fig = plt.figure(dpi=200)
            ax = fig.add_axes((0,0,1,1)) 
            table = ax.table(cellText=table_data, loc="center")
            table.set_fontsize(14)
            table.scale(1,2)
            ax.axis("off")
            canvas = FigureCanvasTkAgg(fig, master=tableWin)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
            drawGraph(xValues, yValues)


def newIteration():
    """Performs another iteration"""
    global x, y, h, r, dydxr, tableWin, canvas, table_data, dp, xValues, yValues
    r += 1
    dydxr = eval(equation) # Inserts x and y into equation
    table_data.append([h, r, round(x, dp), round(y, dp), round(dydxr, dp)]) # Adds to table
    xValues.append(x) # Add to graph
    yValues.append(y)
    
    # Calculates xr and yr for next iteration
    x += h
    y = y + h*dydxr
    
    for i, widget in enumerate(tableWin.winfo_children()):
        if i == 1:
            widget.destroy()
    
    # Redraws table   
    fig = plt.figure(dpi=200)
    ax = fig.add_axes((0,0,1,1)) 
    table = ax.table(cellText=table_data, loc="center")
    table.set_fontsize(14)
    table.scale(1,2)
    ax.axis("off")
    canvas = FigureCanvasTkAgg(fig, master=tableWin)
    canvas.draw()
    canvas.get_tk_widget().pack()
    drawGraph(xValues, yValues)
    

def drawGraph(x, y):
    """Generates graph"""
    global graphWin
    plt.style.use("tableau-colorblind10") 
    
    try:
        for widget in graphWin.winfo_children():
            widget.destroy()
    except Exception:
        graphWin = tk.Toplevel()
        graphWin.geometry("600x400+600+10")
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=3)
    plt.xlabel("X axis") 
    plt.ylabel("Y axis") 
    canvas = FigureCanvasTkAgg(fig, master=graphWin)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    
def showHelp():
    """Shows help window"""
    tk.messagebox.showinfo("Help", "Enter an equation, x and y values and either the final x value (xᵢ) or final "
                           "y value (yᵢ).\n\nIf you have a specific h value or iteration number, then you can also "
                           "add it in the corresponding field.\n\nSPECIAL OPERATIONS FOR EQUATION\n** - To the "
                           "power of\nsqrt() - Square root\nexp() - Exponent\ne - e constant\nlog() - natural log "
                           "ln()\n sin(), cos(), tan() - trigonometric functions (in radians)")
            

### Draw Graphical User Interface ###

# Create window
root = tk.Tk()
root.title("Eulers Method")
root.geometry("600x550")

# Create labels
for i, label in enumerate(["(dy/dx) =", "x₀:", "y₀:", "xᵢ:", "yᵢ:", "h:", "Iterations:", "Decimal Points:"]):
    tk.Label(root, text=label, font="Arial 20").grid(row=i, column=0, padx=20, pady=5, sticky="e")

# Create entry boxes
equationEntry = tk.Entry(root, font="Arial 20")
equationEntry.grid(row=0, column=1, padx=20, pady=5)
equationEntry.insert(0, "(y-x)/(y*x-x**3)")

xEntry = tk.Entry(root, font="Arial 20")
xEntry.grid(row=1, column=1, padx=20, pady=5)
xEntry.insert(0, "2")

yEntry = tk.Entry(root, font="Arial 20")
yEntry.grid(row=2, column=1, padx=20, pady=5)
yEntry.insert(0, "10")

xIEntry = tk.Entry(root, font="Arial 20")
xIEntry.grid(row=3, column=1, padx=20, pady=5)
xIEntry.insert(0, "5")

yIEntry = tk.Entry(root, font="Arial 20")
yIEntry.grid(row=4, column=1, padx=20, pady=5)
yIEntry.insert(0, "")

hEntry = tk.Entry(root, font="Arial 20")
hEntry.grid(row=5, column=1, padx=20, pady=5)
hEntry.insert(0, "")

iterationsEntry = tk.Entry(root, font="Arial 20")
iterationsEntry.grid(row=6, column=1, padx=20, pady=5)
iterationsEntry.insert(0, "2")

dpEntry = tk.Entry(root, font="Arial 20")
dpEntry.grid(row=7, column=1, padx=20, pady=5)
dpEntry.insert(0, "3")

# Create buttons
tk.Button(root, text="Help", font="Arial 20 bold",
          fg="white", bg="gray40", command=showHelp).grid(row=8, column=0, padx=20, pady=20, ipadx=20)

tk.Button(root, text="Calculate", font="Arial 20 bold",
          fg="white", bg="gray40", command=drawTable).grid(row=8, column=1, padx=20, pady=20, sticky="we")

tk.Label(root, text="Program made by Alexander Shemaly",
         font="Arial 16").grid(row=9, column=0, padx=20, pady=10, columnspan=2)

root.mainloop()
