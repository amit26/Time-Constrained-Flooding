from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk
from subprocess import call

top = Tk()
W = 1000
H = 600
s = "0"
b = "0"
d = "0"


INT = 5
def increment_budget():
    global b
    try:
        curr_budg = int(b)
        curr_budg += INT
        b = curr_budg
        budget_entry.delete(0, END)
        budget_entry.insert(0, str(b))
    except:
        tkMessageBox.showinfo("Error", "Please enter a starting source"\
            + " destination, and budget")

def decrement_budget():
    global b
    try:
        curr_budg = int(b)
        curr_budg -= INT
        b = curr_budg
        budget_entry.delete(0, END)
        budget_entry.insert(0, str(b))
    except:
        tkMessageBox.showinfo("Error", "Please enter a starting source"\
            + " destination, and budget")
def run():
    global b
    global s
    global d
    global graph
    global canvas
    global g
    global fname
    global coords
    global el
    b = budget_entry.get()
    s = source_entry.get()
    d = destination_entry.get()
    fname = graph_file.get()
    p = coord_file.get()
    a = str(el.get())
    call(["./test.sh", s, d, fname, b, "output", p, a])

    canvas.delete(ALL)
    gimage = Image.open("./output/output.png")
    g = ImageTk.PhotoImage(gimage)
    graph = canvas.create_image(W/2 + 150, H/2, image=g)
   
#def main(argv):
canvas = Canvas(top, width = W, height = H)
canvas.grid(row = 1, columnspan = 8)
gimage = Image.open("./output/rabbit.jpg")
g = ImageTk.PhotoImage(gimage)
graph = canvas.create_image(W/2 + 150, H/2, image=g)
el = IntVar()

edge_labels = Checkbutton(top, text="Edge Labels", var = el)
plus = Button(top, text = "+", command = increment_budget)
minus = Button(top, text = "-", command = decrement_budget)
run_button = Button(top, text = "Run", command = run)
budget = Label(top, text = "Budget:")
source = Label(top, text = "Source:")
destination = Label(top, text = "Destination:")
budget_entry = Entry(top, bd = 5)
source_entry = Entry(top, bd = 5)
graph_prompt = Label(top, text = "Graph File:")
coord_prompt = Label(top, text = "Coordinate File:")
graph_file = Entry(top, bd = 5);
coord_file = Entry(top, bd = 5);
destination_entry = Entry(top, bd = 5)

graph_prompt.grid(row = 2, column = 0)
graph_file.grid(row = 2, column = 1)
coord_prompt.grid(row = 2, column = 2)
coord_file.grid(row = 2, column = 3)
source.grid(row = 2, column = 4)
source_entry.grid(row = 2, column = 5)
destination.grid(row = 2, column = 6)
destination_entry.grid(row = 2, column = 7)
budget.grid(row = 2, column = 8)
budget_entry.grid(row = 2, column = 9)
plus.grid(row = 2, column = 11)
minus.grid(row = 2, column = 10)
run_button.grid(row = 2, column = 12)
edge_labels.grid(row = 0, column = 0)
top.mainloop()

#if __name__ == "__main__":
#   main(sys.argv[1:])
