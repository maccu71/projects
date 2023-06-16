'''
This is an app to visualize my running results as well as store them.
print(f'\033[91m hallo \x1b[0m')  - colored console - not applied here $$
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

with open("cwicz_SECONDS.dump", "r") as fs:
    druga = json.load(fs)

lista = []
for values in druga.values():
    lista.append(values)

lista_max = max(lista)
lista_min = min(lista)

wspolczynnik = 100 / (lista_max - lista_min)
Wynik = round(wspolczynnik * (lista_max - czas))

print(f'Your result: {Wynik:.1f} % \n')

data = {}  # dict with % results (as comparison to max)

for i in druga:
    x = wspolczynnik * (lista_max - druga.get(i))
    x = round(x)
    data.update({i:x})
data.update({Days:Wynik})  # add last result

odp = input("save to seconds db? y/n ")
print()
if odp.lower() == "y":
    druga[str(Days)] = czas
    with open("cwicz_SECONDS.dump", "w") as file:
        json.dump(druga, file)

# show results in a list form
print(f'list that shows days/seconds: {druga}')
print(f'list that shows days/percents: {data}')

# plotting results
x = list(data.keys())
y = list(data.values())

# plotting the points 
plt.plot(x, y, color='green', linewidth=2, marker='o',
    markerfacecolor='red', markersize=4)

# plt.ylim([-10, 110])
plt.xlabel('days from the first one')   # naming the x axis
plt.ylabel('progress in %')         # naming the y axis
plt.title('progress in exercising')  # giving a title to my graph
plt.show()                          # function to show the plot
