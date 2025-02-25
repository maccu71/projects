import tkinter as tk

class App:
    def __init__(self, window):
        '''
        prosty GUI program do obliczania BMI 
        wykorzystujący tkinter framework
        '''
        self.window = window
        self.window.title("BMI kalkulator")
        # self.window.overrideredirect(True) 
    
 
        self.label1 = tk.Label(self.window, text='Podaj wagę w kg',padx=5, pady=5)
        self.label1.grid(row=0,column=0 ,sticky='W')

        self.entry1 = tk.Entry(self.window)
        self.entry1.grid(row=0,column=1)

        self.label2 = tk.Label(self.window, text='Podaj wzrost w cm',padx=5, pady=5)
        self.label2.grid(row=1,column=0, sticky='W')

        self.entry2 = tk.Entry(self.window)
        self.entry2.grid(row=1,column=1, padx=8, pady=10)

        self.wynik = tk.Label(self.window, 
            text="Twoje BMI",
            font=('Arial', 10, 'bold'))
        self.wynik.grid(row=2,column=0,padx=2, pady=5, sticky='W')

        self.close = tk.Button(self.window, text='Tutaj zamknij', padx=40, pady=5, command=self.close_app)
        self.close.grid(row=3,column=0, padx=4, pady=6)

        self.oblicz = tk.Button(self.window,text='Oblicz BMI',padx=40, pady=5, command=self.oblicz_bmi)
        self.oblicz.grid(row=3,column=1, padx=4, pady=6)

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