import tkinter as tk
from tkinter import ttk

field_text = ""

def add_to_field(sth):
    global field_text
    field_text = field_text + str(sth)
    # delete previous content
    field.config(state="normal")
    field.delete("1.0", "end")
    field.insert("1.0", field_text)
    field.config(state="disabled")

def calculate():
    global field_text
    result=str(eval(field_text))
    field.config(state="normal")
    field.delete("1.0", "end")
    field.insert("1.0", result)
    field_text = result
    field.config(state="disabled")

def clear():
    global field_text
    field_text = ""
    field.config(state="normal")
    field.delete("1.0", "end")
    field.config(state="disabled")

window = tk.Tk()
window.title("Python Calculator")
window.geometry("500x500")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1) # frame expands
frame = ttk.Frame(window,padding=10)
frame.grid(row=0, column=0, sticky="nsew")
for i in range(5):
    frame.rowconfigure(i, weight=1)

for j in range(4):
    frame.columnconfigure(j, weight=1)

# in here height is the count of rows
field = tk.Text(frame, height=1, font=("Times New Roman", 22))
field.grid(column=0, row=0, columnspan=5, sticky="nsew", pady=10,padx=10)
field.config(
    insertwidth=0,
    state = "disabled"
)

#########################################################
# Number Buttons
#########################################################
btn_1 = tk.Button(frame,text="1", command=lambda : add_to_field(1),font=("Times New Roman",14))
btn_1.grid(column=0, row=3,sticky="nsew", padx=5, pady=5)

btn_2 = tk.Button(frame,text="2", command=lambda : add_to_field(2),font=("Times New Roman",14))
btn_2.grid(column=1, row=3,sticky="nsew", padx=5, pady=5)

btn_3 = tk.Button(frame,text="3", command=lambda : add_to_field(3),font=("Times New Roman",14))
btn_3.grid(column=2, row=3,sticky="nsew", padx=5, pady=5)

btn_4 = tk.Button(frame,text="4", command=lambda : add_to_field(4),font=("Times New Roman",14))
btn_4.grid(column=0, row=2,sticky="nsew", padx=5, pady=5)

btn_5 = tk.Button(frame,text="5", command=lambda : add_to_field(5),font=("Times New Roman",14))
btn_5.grid(column=1, row=2,sticky="nsew", padx=5, pady=5)

btn_6 = tk.Button(frame,text="6", command=lambda : add_to_field(6),font=("Times New Roman",14))
btn_6.grid(column=2, row=2,sticky="nsew", padx=5, pady=5)

btn_7 = tk.Button(frame,text="7", command=lambda : add_to_field(7),font=("Times New Roman",14))
btn_7.grid(column=0, row=1,sticky="nsew", padx=5, pady=5)

btn_8 = tk.Button(frame,text="8", command=lambda : add_to_field(8),font=("Times New Roman",14))
btn_8.grid(column=1, row=1,sticky="nsew", padx=5, pady=5)

btn_9 = tk.Button(frame,text="9", command=lambda : add_to_field(9),font=("Times New Roman",14))
btn_9.grid(column=2, row=1,sticky="nsew", padx=5, pady=5)

btn_0 = tk.Button(frame,text="0", command=lambda : add_to_field(0),font=("Times New Roman",14))
btn_0.grid(column=1, row=4,sticky="nsew", padx=5, pady=5)

#########################################
# Operations Buttons
#########################################
btn_plus = tk.Button(frame,text="+", command=lambda : add_to_field("+"),font=("Times New Roman",14))
btn_plus.grid(column=3, row=1,sticky="nsew", padx=5, pady=5)

btn_minus = tk.Button(frame,text="-", command=lambda : add_to_field("-"),font=("Times New Roman",14))
btn_minus.grid(column=3, row=2,sticky="nsew", padx=5, pady=5)

btn_times = tk.Button(frame,text="*", command=lambda : add_to_field("*"),font=("Times New Roman",14))
btn_times.grid(column=3, row=3,sticky="nsew", padx=5, pady=5)

btn_division = tk.Button(frame,text="/", command=lambda : add_to_field("/"),font=("Times New Roman",14))
btn_division.grid(column=3, row=4,sticky="nsew", padx=5, pady=5)

btn_clear = tk.Button(frame,text="c", command=clear,font=("Times New Roman",14))
btn_clear.grid(column=0, row=4,sticky="nsew", padx=5, pady=5)

btn_equal = tk.Button(frame,text="=", command=calculate,font=("Times New Roman",14))
btn_equal.grid(column=2, row=4,sticky="nsew", padx=5, pady=5)

window.mainloop()


