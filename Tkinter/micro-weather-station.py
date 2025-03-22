

import tkinter as tk
import requests

class App:
    def __init__(self, window):
        '''
        Simple GUI to get the actual weather stats
        '''
        self.window = window
        self.window.title("MICRO WEATHER STATION")

        self.label1 = tk.Label(self.window, text='Enter the City',padx=5, pady=5)
        self.label1.grid(row=0,column=0 ,sticky='W')

        self.entry1 = tk.Entry(self.window)
        self.entry1.grid(row=0,column=1)

        self.label2 = tk.Label(self.window, text='',padx=5, pady=5)
        self.label2.grid(row=1,column=1 ,sticky='W')

        self.label3 = tk.Label(self.window, text='',padx=5, pady=5)
        self.label3.grid(row=2,column=1 ,sticky='W')

        self.wynik = tk.Label(self.window,text='Sky:',font=('Arial', 10, 'bold'))
        self.wynik.grid(row=1,column=0,padx=2, pady=5, sticky='W')

        self.wynik1 = tk.Label(self.window,text='Temperature:',font=('Arial', 10, 'bold'))
        self.wynik1.grid(row=2,column=0,padx=2, pady=5, sticky='W')

        self.close = tk.Button(self.window, text='Exit here', padx=40, pady=5, command=self.close_app)
        self.close.grid(row=3,column=0, padx=4, pady=6)

        self.oblicz = tk.Button(self.window,text='Get weather',padx=40, pady=5, command=self.get_weather)
        self.oblicz.grid(row=3,column=1, padx=4, pady=6)

    def close_app(self) -> None:
        '''
        this close the app
        '''
        self.window.destroy()

    def get_weather(self):

        city = self.entry1.get()
        url = f"https://wttr.in/{city}?format=j1"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError if response is not 200
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

        data = response.json()

        current = data.get('current_condition')
        if not current:
            print("Unexpected response format: Missing 'current_condition'")
            return None

        weather_desc = current[0].get('weatherDesc', [{}])  # Default empty list
        sky = weather_desc[0].get('value', "Unknown")
        temp_c = current[0].get('temp_C', "N/A")  # Default "N/A" if missing

        self.label2.config(text=sky)
        self.label3.config(text=temp_c)

window = tk.Tk()
app = App(window)

window.mainloop()
