from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests

# Create root window
root = Tk()
root.title('Currency Conversion App')
root.geometry("500x500")

# Create tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=5)

# Create Frames 
currency_frame = Frame(my_notebook, width=480, height=480)
conversion_frame = Frame(my_notebook, width=480, height=480)

currency_frame.pack(fill="both", expand=1)
conversion_frame.pack(fill="both", expand=1)

# Add Tabs
my_notebook.add(currency_frame, text="Currencies")
my_notebook.add(conversion_frame, text="Convert")

# Disable the 2nd Tab
my_notebook.tab(1, state='disabled')

######################################################
# Currency Stuff
######################################################
def lock():
    if not home_entry.get() or not conversion_entry.get():
        messagebox.showwarning("WARNING!", "You did not fill out all the fields...")
    else:
        # Disable Entry Boxes
        home_entry.config(state='disabled')
        conversion_entry.config(state='disabled')
        # Enable Tab
        my_notebook.tab(1, state='normal')
        # Changing Tab Field for Conversion Tab
        amount_label.config(text=f'Amount of {home_entry.get()} to convert to {conversion_entry.get()}')
        converted_label.config(text=f'Equals this many {conversion_entry.get()}')
        convert_button.config(text=f'Convert from {home_entry.get()}')

def unlock():
    # Enable Entry Boxes
    home_entry.config(state='normal')
    conversion_entry.config(state='normal')
    # Disable Tab
    my_notebook.tab(1, state='disabled')

home = LabelFrame(currency_frame, text="Your Home Currency (3 Letter Code)")
home.pack(pady=20)

# Home Currency Entry Box
home_entry = Entry(home, font=("Calibri", 24))
home_entry.pack(pady=10, padx=10)

# Conversion Currency Frame
conversion = LabelFrame(currency_frame, text="Conversion Currency")
conversion.pack(pady=20)

# 'Convert To' Label
conversion_label = Label(conversion, text = "Currency to Convert to... (3 Letter Code)")
conversion_label.pack(pady=10)

# 'Convert To' Entry Box
conversion_entry = Entry(conversion, font=("Calibri", 24))
conversion_entry.pack(pady=10, padx=10)

# Option to manually input the rate over here, but that functionality has been removed

# Button Frame 
button_frame = Frame(currency_frame)
button_frame.pack(pady=20)

# Create Buttons
lock_button = Button(button_frame, text="Lock", command=lock)
lock_button.grid(row=0, column=0, padx=10)

unlock_button = Button(button_frame, text="Unlock", command=unlock)
unlock_button.grid(row=0, column=1, padx=10)

######################################################
# Conversion Stuff
######################################################
def convert():
    # Clear Converted Entry Box
    converted_entry.delete(0, END)
    
    # Convert
    api = requests.get(f"https://api.frankfurter.app/latest?amount={float(amount_entry.get())}&from={home_entry.get()}&to={conversion_entry.get()}")
    api_conversion_rate = api.json()['rates'][conversion_entry.get()]
    conversion = float(api_conversion_rate)
    # Convert 'conversion' to just 2 decimal places
    conversion = round(conversion, 2)
    # Add commas to the produced value
    conversion = '{:,}'.format(conversion)

    # Update Converted Entry Box
    converted_entry.insert(0, f'{conversion} {conversion_entry.get()}')

def clear():
    amount_entry.delete(0, END)
    converted_entry.delete(0, END)

amount_label = LabelFrame(conversion_frame, text="Amount to Convert")
amount_label.pack(pady=20)

# Entry Box for Amount to Convert
amount_entry = Entry(amount_label, font=("Calibri", 24))
amount_entry.pack(pady=10, padx=10)

# Convert Button
convert_button = Button(amount_label, text="Convert", command=convert)
convert_button.pack(pady=20)

# 'Equivalent to this amount' Frame
converted_label = LabelFrame(conversion_frame, text="Converted Currency")
converted_label.pack(pady=20)

# 'Converted' Entry Box
converted_entry = Entry(converted_label, font=("Calibri", 24), bd=0)
converted_entry.pack(pady=10, padx=10)
# There was meant to be a bg="systembuttonface" command over here but it was not running

# Clear Button
clear_button = Button(conversion_frame, text="Clear", command=clear)
clear_button.pack(pady=20)

# Face Label to make spacing better
spacer = Label(conversion_frame, text="", width=68)
spacer.pack()




root.mainloop()