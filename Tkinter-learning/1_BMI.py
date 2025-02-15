def oblicz_bmi(wzrost: int, waga: int) -> float:
    """
    Prosty program napisany w języku Python3
    do obliczania BMI (współczynnika BMI - Body Mass Index)
    wskazującego stosunek masy ciała do jego wzrostu.
    Dodatkowe tabele pozwalaja ocenić jego stan.
    Parametrami są tutaj:
    waga - masa ciała w kilogramach
    wzrost - wzrost w centymetrach
    Zwracanym wynikiem jest:
    bmi - współczynnik BMI z dokładnością do jednej liczby po przecinku
    """
    bmi = waga / wzrost   # silnik obliczanie BMI
    return bmi

if __name__ == "__main__":
    while True:
        try:
            waga = input("wprowadź swoją wagę w kg: ")
            waga = int(waga)
            wzrost = input("wprowadź swoją wagę w cm: ")
            wzrost = int(wzrost)
            break
        except ValueError:
            print("wprowadź jeszcze raz poprawne wartości..")
            continue
    obliczony_bmi = oblicz_bmi(waga, wzrost)
    print(f'Twój index BMI wynosi: {obliczony_bmi:.1f}')





