# Kod za nedelju 1 - teorija je u nedelja1_teorija.md
import csv
from pathlib import Path

# Osnovne podatke
rezervacije = [
    {"gost": "Ana", "noci": 3, "cijena_noci": 80},
    {"gost": "Marko", "noci": 5, "cijena_noci": 65},
    {"gost": "Ivana", "noci": 2, "cijena_noci": 120},
]

# Eksplicitna petlja
ukupno = 0
for r in rezervacije:
    ukupno += r["noci"] * r["cijena_noci"]

# Ekvivalent pomocu izraza
# iznos = r["noci"] * r["cijena_noci"] for r in rezervacije


# Funckije: parametri, tipovi i izuzeci
def iznos(noci: int, cijena_noci: float, popust: float = 0.0) -> float:
    if not 0.0 <= popust <= 1.0:
        raise ValueError("Popoust mora biti u intervalu [0,1]")
    return noci * cijena_noci * (1 - popust)


"""
print(iznos(3, 80))
print(iznos(3, 80, 0.1))

try:
    iznos(3, 80, 1.5)
except ValueError as e:
    print("Greška: ", e)
"""


print("Path")

def prosjecna_cijena(putanja: Path) -> float:
    ukupno, noci = 0.0, 0
    with putanja.open(newline="", encoding="utf-8") as f:
        for red in csv.DictReader(f):
            n = int(red["noci"])
            ukupno += n * float(red["cijena_noci"])
            noci += n
    if noci == 0:
        raise ValueError("Datoteka ne sadrži nijednu noć")
    return ukupno / noci


# test_cijene.py
def test_prosjek(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\nAna,2,100\nMarko,5,65\nIvana,2,120")
    
    rezultat = prosjecna_cijena(p)
    
    assert prosjecna_cijena(p) == 75.0
    print("Test uspješan! Prosječna cijea: ", rezultat)




#Zadaci
#1. Identifikovati nedostatke u kodu (najmanje 4)
#2. Formulisati test koji otkriva svaki nedostatak
#3. Amalizirati isti kod uz AI asistenta i uporediti nalaze
#4. Ispraviti fukcije i potvrditi ispravke testovima
#5. Obrazložiti zašto je svaki nedostatak rizičan u praksi

# Originalni kod (sa nedostacima)
"""
def prosjek(vrijednosti, rezultat = []):
    rezultat.append(sum(vrijednosti) / len(vrijednosti))
    return rezultat

def ucitaj(putanja):
    try:
        return open(putanja).read()
    except:
        pass

def punoljetan(godine):
    return godine > 18
"""

# 1. Nedostaci i 5. Zašto su rizični u praksi
"""
N1. prosjek: promjenljiv podrazumijevani argument (rezultat = []).
    Lista se kreira samo jednom, pri definiciji funkcije, pa se rezultati
    gomilaju između poziva. Rizik: drugi poziv vraća i stare rezultate -
    tihe, teško uočljive greške koje zavise od redosljeda poziva.

N2. prosjek: prazna lista izaziva ZeroDivisionError.
    Rizik: nejasna poruka koja ne govori šta je pogrešno u ulazu; program
    pada na podacima koji su u praksi česti (npr. nema ocjena/rezervacija).

N3. ucitaj: goli except: pass guta SVE izuzetke i vraća None.
    Hvata i KeyboardInterrupt, PermissionError, UnicodeDecodeError...
    Rizik: greška se ne vidi na mjestu nastanka, već kasnije kao
    "NoneType has no attribute ..." - debugging postaje vrlo težak.

N4. ucitaj: datoteka se ne zatvara (nema context managera).
    Rizik: curenje file deskriptora; u dugo-živućim programima (serveri)
    sistem ostaje bez deskriptora, a na Windowsu datoteka ostaje zaključana.

N5. ucitaj: nije zadat encoding.
    Koristi se podrazumijevani encoding sistema (na Windowsu često cp1250),
    pa se "č, ć, ž, š, đ" čitaju pogrešno ili izazivaju UnicodeDecodeError.
    Rizik: kod radi na jednom računaru, a pada na drugom.

N6. punoljetan: granični slučaj - osoba sa tačno 18 godina nije punoljetna
    (> umjesto >=). Rizik: off-by-one greška u poslovnom pravilu; pogrešno
    odbijanje korisnika, pravne posljedice.

N7. punoljetan: nema validacije - negativne godine prolaze bez greške.
    Rizik: neispravni podaci se tiho prihvataju i šire kroz sistem.

Dodatno: nijedna funkcija nema type hints ni docstring.
"""

