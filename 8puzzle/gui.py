from tkinter import *
import winsound
import time
import re
from tkinter import messagebox

from solver import *

root = Tk()
root.title("8 puzzle")
root.resizable(False, False)
root.geometry("450x700+500+10")

# setting variables
w = 5
h = 3
f = ("Courier", 36)

# creating puzzle labels
color = ["#50394c", "#ffef96", "#b2b2b2", "#f4e1d2", "#c94c4c", "#92a8d1", "#b2ad7f", "#6b5b95"]
labels = []
labels.append(Label(root, text=" ", width=w, height=h))
for i in range(1, 9):
    labels.append(Label(root, text=i, font=f, width=w, height=h, bg=color[i - 1]))

# label to show execution time in miliseconds
exec_time = Label(root, text=" ", width=20, height=2)
exec_time.grid(row=8, column=1)

# label to show current step
steps = Label(root, text=" ", width=20)
steps.grid(row=9, column=1)

# indicate clicking on stop button
flag = False


# handle clicking on stop button
def terminate(f):
    global flag
    flag = True


# make sure the input has unique characters between 0-8
def validate_input(t):
    if re.search("[0-8]{9}", t) and len(set(t)) == len(t):
        return True
    return False


# display solution steps
def run(step, labels, method, heuristic_fn=None):
    global flag, e, exec_time
    flag = False
    initial_state = e.get()  # e : user input state
    if not validate_input(initial_state):
        messagebox.showerror('Python Error', 'Error: This is invalid input !')
        return

    start_time = time.time()
    if heuristic_fn:
        path = method(initial_state, heuristic_fn)
    else:
        path = method(initial_state)

    total_time = str(int((time.time() - start_time) * 1000))
    exec_time.config(text="Executed in " + total_time + " ms")

    # if the puzzle isn't solvable show info message
    if not len(path):
        messagebox.showinfo("Message", "The Puzzle Is UnSolvable")

    i = 1
    for state in path:
        for index in range(9):
            (r, c) = (int(index) // 3, int(index) % 3)
            labels[int(state[index])].grid(row=r, column=c)
        winsound.PlaySound('mixkit-small-hit-in-a-game-2072.wav', winsound.SND_ASYNC)
        step_number = "Step no " + str(i) + " out of " + str(len(path))
        i += 1
        step.config(text=step_number)
        root.update()
        if flag:
            break
        time.sleep(0.75)


state = "012345678"  # initial_state

# show initial state when the app begin
for index in range(9):
    (r, c) = (int(index) // 3, int(index) % 3)
    labels[int(state[index])].grid(row=r, column=c, padx=1, pady=1)

# entry : inter initial state as string
e = Entry(root)
e.grid(row=5, column=1)

# running buttons
BFS = Button(root, text="BFS", bg='#567', fg='White', command=lambda: run(steps, labels, bfs))
BFS.grid(row=4, column=0, padx=15, pady=15)
DFS = Button(root, text="DFS", bg='#567', fg='White', command=lambda: run(steps, labels, dfs))
DFS.grid(row=4, column=2)
A1 = Button(root, text="A* heuristic1", bg='#567', fg='White', command=lambda: run(steps, labels, a_star, h1))
A1.grid(row=6, column=0)
A2 = Button(root, text="A* heuristic2", bg='#567', fg='White', command=lambda: run(steps, labels, a_star, h2))
A2.grid(row=6, column=2)

# stop button
Stop = Button(root, text="STOP", fg='red', command=lambda: terminate(flag))
Stop.grid(row=7, column=1)


# handle closing the window
def on_closing():
    global flag
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        flag = True
        root.quit()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
