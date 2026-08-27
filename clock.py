'''
#source: https://handhikayp.medium.com/generate-a-simple-digital-clock-with-python-tkinter-796a5b298872

import tkinter as tk
from time import strftime

# Function to update the digital clock label
def update_time():
    string_time = strftime('%H:%M:%S')
    digital_clock.config(text=string_time)
    digital_clock.after(1000, update_time)

# Main Tkinter window
root = tk.Tk()
root.title("Digital Clock")

# Digital clock label configuration
digital_clock = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
digital_clock.pack(pady=20)

# Initial call to update_time function
update_time()

# Tkinter main loop
root.mainloop()

#source: https://docs.python.org/3/library/time.html#time.localtime
'''



