'''
This is an app to visualize my running results as well as store them.
print(f'\033[91m hallo \x1b[0m')  - colored console - not applied here
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
Wynik = .152671756 * (3055 - czas)  # 100% /655 calculate the perf. as a %

# some additional informative stuff:
# best run                            - 2400 sec ( 40 min )
# worst run                           - 3055 sec ( 50 min 55 sec )
# difference in seconds               - 655 sec  ( 10 min 55 sec )

print(f'Your result: {Wynik:.1f} % \n')

# load databese of results
with open("cwicz.dump", "r") as json_file:
    data = json.load(json_file)

# add today's result
a = input("show the new result? y/n ")
if a == "y" or a == "Y":
    data[str(Days)] = round(Wynik)

b = input("save to % database? y/n ")
if b == "y" or b == "Y":
    with open("cwicz.dump", "w") as f:
        json.dump(data, f)

with open("cwicz_SECONDS.dump", "r") as fs:
    druga = json.load(fs)

x = input("czy zapisać ilość sekund? y/n ")
print()
if x == "y" or x == "Y":
    druga[str(Days)] = czas
    with open("cwicz_SECONDS.dump", "w") as ff:
        json.dump(druga, ff)

print(f'lista z sekundami: {druga}')
print(f'lista z wynikiem w %: {data}')

# plotting results
x = list(data.keys())
y = list(data.values())

# plotting the points 
plt.plot(x, y, color='green', linewidth=2, marker='o',
    markerfacecolor='red', markersize=4)

plt.ylim([-10, 110])
plt.xlabel('days from the first one')   # naming the x axis
plt.ylabel('progress in %')         # naming the y axis
plt.title('progress in exercising')  # giving a title to my graph
plt.show()                          # function to show the plot