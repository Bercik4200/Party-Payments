import tkinter as tk
from tkinter import messagebox

def rozlicz_platnosci(platnosci):
    liczba_osob = len(platnosci)
    suma_wydatkow = sum(platnosci.values())
    srednia_kwota = suma_wydatkow / liczba_osob
    
    # Obliczamy, ile każda osoba powinna otrzymać/zapłacić
    saldo = {osoba: platnosci[osoba] - srednia_kwota for osoba in platnosci}
    
    # Tworzymy dwie listy: osoby, które muszą oddać pieniądze i te, które muszą otrzymać
    do_zaplaty = [(osoba, round(-kwota, 2)) for osoba, kwota in saldo.items() if kwota < 0]
    do_otrzymania = [(osoba, round(kwota, 2)) for osoba, kwota in saldo.items() if kwota > 0]
    
    # Rozliczamy, kto komu ma zapłacić
    transakcje = []
    
    while do_zaplaty and do_otrzymania:
        dlużnik, kwota_do_zaplaty = do_zaplaty.pop(0)
        wierzyciel, kwota_do_otrzymania = do_otrzymania.pop(0)
        
        # Minimalna kwota, jaką można przelać
        kwota_transakcji = min(kwota_do_zaplaty, kwota_do_otrzymania)
        
        transakcje.append(f"{dlużnik} powinien zapłacić {wierzyciel} {kwota_transakcji} zł")
        
        # Aktualizujemy kwoty po transakcji
        kwota_do_zaplaty -= kwota_transakcji
        kwota_do_otrzymania -= kwota_transakcji
        
        # Jeśli ktoś nadal ma dług lub należność, dodajemy go z powrotem do listy
        if kwota_do_zaplaty > 0:
            do_zaplaty.insert(0, (dlużnik, kwota_do_zaplaty))
        if kwota_do_otrzymania > 0:
            do_otrzymania.insert(0, (wierzyciel, kwota_do_otrzymania))
    
    return transakcje

''' Przykład użycia
platnosci = {
    "Jan": 150,
    "Anna": 120,
    "Tomek": 180,
    "Zosia": 100
}

transakcje = rozlicz_platnosci(platnosci)
for transakcja in transakcje:
    print(transakcja)
'''

def oblicz_rozliczenie():
    platnosci = {}
    for i in range(len(lista_osob)):
        osoba = lista_osob[i].get()
        kwota = lista_kwot[i].get()
        if osoba and kwota:
            try:
                platnosci[osoba] = float(kwota)
            except ValueError:
                messagebox.showerror("Błąd", f"Niewłaściwa kwota dla osoby: {osoba}")
                return
    
    transakcje = rozlicz_platnosci(platnosci)
    wynik.config(state="normal")
    wynik.delete(1.0, tk.END)  # Czyści pole wyników
    for transakcja in transakcje:
        wynik.insert(tk.END, transakcja + "\n")
    wynik.config(state="disabled")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Rozliczanie płatności")

# Listy do przechowywania pól tekstowych
lista_osob = []
lista_kwot = []

# Funkcja do dodania nowego pola dla osoby
def dodaj_pole():
    osoba_entry = tk.Entry(root)
    kwota_entry = tk.Entry(root)
    osoba_entry.grid(row=len(lista_osob) + 1, column=0, padx=5, pady=5)
    kwota_entry.grid(row=len(lista_osob) + 1, column=1, padx=5, pady=5)
    lista_osob.append(osoba_entry)
    lista_kwot.append(kwota_entry)

# Etykiety nagłówkowe
tk.Label(root, text="Imię").grid(row=0, column=0)
tk.Label(root, text="Kwota zapłacona").grid(row=0, column=1)

# Dodanie pierwszych dwóch pól tekstowych na starcie
dodaj_pole()
dodaj_pole()

# Przycisk do dodania nowej osoby
tk.Button(root, text="Dodaj osobę", command=dodaj_pole).grid(row=0, column=2, padx=5, pady=5)

# Przycisk do obliczenia rozliczenia
tk.Button(root, text="Oblicz rozliczenie", command=oblicz_rozliczenie).grid(row=len(lista_osob) + 2, column=0, columnspan=3, pady=10)

# Pole tekstowe do wyświetlania wyniku
wynik = tk.Text(root, height=10, width=50, state="disabled")
wynik.grid(row=len(lista_osob) + 3, column=0, columnspan=3, padx=5, pady=5)

# Uruchomienie aplikacji
root.mainloop()