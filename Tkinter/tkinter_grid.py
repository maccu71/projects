import tkinter as tk

class App:
    def __init__(self, window):
        self.window = window
        #self.window.title("OKNO")

        self.frame = tk.Frame(self.window)
        self.frame.grid(padx=30, pady=30)

        self.b9 = tk.Button(self.frame, text="1")
        self.b9.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.b2 = tk.Button(self.frame, text="2")
        self.b2.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.b3 = tk.Button(self.frame, text="3", command=self.exit)
        self.b3.grid(row=2, column=0, sticky="e", padx=5, pady=5)

    def exit(self):
        self.window.destroy()


window = tk.Tk()
app = App(window)

window.mainloop()
