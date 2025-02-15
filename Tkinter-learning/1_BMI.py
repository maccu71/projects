import tkinter as tk

class App:
    def __init__(self, window):
        '''
        program do obliczania BMI wykorzystujący
        tkinter framework
        '''
        self.window = window
        self.window.title("BMI kalkulator")

        self.label1 = tk.Label(self.window, text='Podaj wagę w kg')
        self.label1.pack()

        self.entry1 = tk.Entry(self.window)
        self.entry1.pack()

        self.label2 = tk.Label(self.window, text='Podaj wzrost w cm')
        self.label2.pack()

        self.entry2 = tk.Entry(self.window)
        self.entry2.pack()

        self.wynik = tk.Label(self.window, text="Your BMI will appear here.")
        self.wynik.pack()

        self.close = tk.Button(self.window, text='Tutaj zamknij aplikację', command=self.close_app)
        self.close.pack()

        self.oblicz = tk.Button(self.window,text='Oblicz swoje BMI',command=self.oblicz_bmi)
        self.oblicz.pack()

    def close_app(self) -> None:
        '''
        ma za zadanie zamknąć aplikację 
        po naciśnięciu przycisku'''
        self.window.destroy()

    def oblicz_bmi(self) -> None:
        '''
        ma na celu obliczenie BMI - główne obliczenia
        '''
        try:
            waga = float(self.entry1.get())
            wzrost = float(self.entry2.get())/100
            print(waga, wzrost)
            wynik = waga / (wzrost * wzrost) 
            print(f'{wynik:.2f}')
            self.wynik.config(text=f'Twoje BMI: {wynik:.2f}')
        except:
            self.wynik.config(text='Podaj prawidłowe wartości w cm i kg')

window = tk.Tk()
app = App(window)

window.mainloop()


