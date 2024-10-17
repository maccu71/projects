'''
This is an app to visualize my running results as well as store them.
'''
from datetime import date
import json
import matplotlib.pyplot as plt

First_Day = date(2023, 1, 11)   # day when you started makeing exercises
Today = date.today()            # obvious, today
Days = (Today - First_Day).days   # days after you started

minuty = int(input('How many minutes? '))   # dzisiejszy wynik, minuty
sekundy = int(input('How many seconds? '))  # dzisiejszy wynik, sekundy

print(f'\nDays after you started: {Days}')

czas = 60 * minuty + sekundy  # conversion minutes and sesonds to total seconds

with open("cwicz.dump", "r", encoding='utf-8') as fs:
    druga = json.load(fs)

lista = []
for values in druga.values():
    lista.append(values)

lista_max = max(lista)
lista_min = min(lista)

wspolczynnik = 100 / (lista_max - lista_min)
Wynik = round(wspolczynnik * (lista_max - czas))

print(f'Your result: {Wynik:.1f} % \n')

better, worst = 0, 0
for i in druga.values():
    if czas < i:
        worst += 1
    if czas > i:
        better += 1
if better == 0:
    print('YOUR BEST RUN!!')
else:
    print(f'Number of better runs:({better}) ',end='')
    print('\u25A0'*better)
    print(f'Number of worst  runs:({worst}) ',end='')
    print('\u25A0'*worst)

data = {}  # dict with % results (as comparison to max)

for i in druga:
    x = wspolczynnik * (lista_max - druga.get(i))
    x = round(x)
    data.update({i:x})
data.update({Days:Wynik})  # add last result

odp = input("save the output? y/n ")
print()
if odp.lower() == "y":
    druga[str(Days)] = czas
    with open("cwicz.dump", "w", encoding='utf-8') as file:
        json.dump(druga, file)

# show results in a list form
print(f'days/seconds: {druga}')
print(f'days/percents: {data}')

# plotting results
x = list(data.keys())
y = list(data.values())

plt.plot(x, y, color='green', linewidth=2, marker='o',
    markerfacecolor='red', markersize=4)

plt.xlabel('days from the first one')   # naming the x axis
plt.ylabel('progress in %')         # naming the y axis

plt.title('progress in exercising')  # giving a title to my graph
plt.show()                          # function to show the plot
