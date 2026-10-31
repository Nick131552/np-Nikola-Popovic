# Nedelja 1

## Predmetne stvari

Bodovanje:
- Mini projekti - 30 bodova
- Kolokvijum - 30 bodova
- Završni projekat - 40 bodova

Može da se koristi AI alati, ali jedino ako može da objasni to što generiše.
Pored toga može za sve standardne svrhe da se koristi:
- testiranje, debugging, documenting prompts,
- ne davati privatne informacije, ne plagijarizam, etc.

## Osnovne podatke

Tipovi podataka:
- `int`, `float` - numerički tipovi
- `str` - nepromijenljiv niz
- `bool` - logički vrijednost
- `list` - uređena, promjenljiva kolecija
- `tuple` - uređena, nepromjenljiva kolekcija
- `dict` - preslikavanje, ključ vrijednosti
- `set` - neuređen skup

Iteracija:
- for petlja - ekplicitna iteracija i akumulacija
- list comprehension - sažet zapis transformacije i filtriranja

## Funckije: parametri, tipovi i izuzeci

- Type honts:
- Podrazumijevani parametar: opcioni argument koji ograničava koje su moguće ulazi
- Valdacija: neispravan ulaz izaziva izuzetak
- Docstring: kratak opis namjene

## Rad sa datotekama i obrada grešaka

- Context manager: osigurava zatvaranje datoteke
- `csv.DictReader`: redovi se čitaju kao rječnici
- try/except: obrada očekivanih grešaka
- Princip: hvatati konkretne izuzetke, ne sve

## Struktura efikasnog upita (prompta)

- Kontekst: smanjuje nejednoznačnost
- Ograničenja: usmjerava na prihvatljivo rješenje
- Testovi u zahtjevu: omogućava neposrednu verifikaciju
- Obrazloženje: podržava razumijevanje riješenja

## Objektno orijentisano programiranje

- Održivost koda odrežuje trošak sofvera

## Osnovni pojmovi

- Klasa : Opis strukture i ponašanja skupa srodnih objekata
- Objekat: Konkretan primjerak klase sa vlastitim stanjem
- Atribut: Podatak koji čine stanje objekta
- Metoda: Funkcija koja definiše poanašanje objekta
- Enkapsulacija: Zaštita unutrašnjeg stanja i kontrolisan pristup
- Apstrakcija: Izdvajanje bitnog, skrivanje informacije
- Polimorfizam: Različite klase iza istog interfejsa
