import tkinter as tk
import psutil

root = tk.Tk()
root.title("OS current stats")

def update_stats():

    mem_avail = psutil.virtual_memory().available / 1024 / 1024
    mem_label.config(text=f"{mem_avail:.2f} MB")

    disk_usage = psutil.disk_usage('/').percent
    disk_label.config(text=f"{disk_usage:.2f} %")
    
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_label.config(text=f"{cpu_percent:.2f} %")
    
    root.after(1000, update_stats)  # update every 1 sec

mem_text = tk.Label(root, text='Memory available (MB): ',padx=5, pady=5, font=("Arial", 10, "bold"))
mem_text.grid(row=1,column=0, sticky='W')
mem_label = tk.Label(root, text='',padx=5, pady=5)
mem_label.grid(row=2,column=0, sticky='W')

# show cpu stats
cpu_text = tk.Label(root, text='Cpu usage (%): ',padx=5, pady=5, font=("Arial", 10, "bold"))
cpu_text.grid(row=3,column=0, sticky='W')
cpu_label = tk.Label(root, text='',padx=5, pady=5)
cpu_label.grid(row=4,column=0, sticky='W')

# show disk stats
disk_text = tk.Label(root, text='Disk usage (%): ',padx=5, pady=5, font=("Arial", 10, "bold"))
disk_text.grid(row=5,column=0, sticky='W')
disk_label = tk.Label(root, text='',padx=5, pady=5)
disk_label.grid(row=6,column=0, sticky='W')

# introduce close windows
def close_app():
    root.destroy()

close = tk.Button(root, text='Exit', padx=40, pady=5, command=close_app)
close.grid(row=7,column=0, padx=4, pady=6)

update_stats()

root.mainloop()
