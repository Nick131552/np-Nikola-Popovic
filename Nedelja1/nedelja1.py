# Kod za nedelju 1 - teorija je u nedelja1_teorija.md
import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pytest

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
    p.write_text("gost,noci,cijena_noci\nAna,2,100\nMarko,2,50\n", encoding="utf-8")
    assert prosjecna_cijena(p) == 75.0


def test_prosjek_ponderisan_brojem_noci(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\nAna,1,100\nMarko,3,60\n", encoding="utf-8")
    assert prosjecna_cijena(p) == 70.0  # (1*100 + 3*60) / 4


def test_prosjek_prazna_datoteka(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\n", encoding="utf-8")
    with pytest.raises(ValueError):
        prosjecna_cijena(p)


# Zadaci
# 1. Identifikovati nedostatke u kodu (najmanje 4)
# 2. Formulisati test koji otkriva svaki nedostatak
# 3. Amalizirati isti kod uz AI asistenta i uporediti nalaze
# 4. Ispraviti fukcije i potvrditi ispravke testovima
# 5. Obrazložiti zašto je svaki nedostatak rizičan u praksi

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


class Tarifa(ABC):
    @abstractmethod
    def cijena(self, osnova: float) -> float: ...


class Standradna(Tarifa):
    def cijena(self, osnova: float) -> float:
        return osnova


class Sezonska(Tarifa):
    def cijena(self, osnova: float) -> float: ...


# Zadaci
# 1. Identifikovati odgovornost klase (princip S)
# 2. Razdvojiti na zasebne klase ili funkcije
# 3. Apstrahovati izvor podataka kroz Protocol (princip D)
# 4. Prosiriti - dodati drugi izvor bez izmjene servisa (princip O)
# 5. Testirati servis sa zamjenskim izvorom podataka
# 6. Uporediti rjesenje sa prijedlogom AI asistenta

# Originalni kod
"""
class UpravljanjeRezervacijama:
    def __init__(self, putanja):
        self.putanja = putanja

    def ucitaj(self):
        return [l.strip().split(",") for l in open(self.putanja)]

    def izracunaj_iznos(self, r):
        return int(r[1]) * float(r[2])

    def sacuvaj_izvjestaj(self, iznosi):
        open("izvjestaj.txt", "w").write(str(iznosi))

    def posalji_mail(self, iznosi):
        print("Poslato: ", sum(iznosi))
"""

# 1. Odgovornosti klase UpravljanjeRezervacijama
"""
Klasa ima četiri razloga za promjenu, a po principu S treba da ima jedan:
    - ucitaj:             čitanje podataka (format datoteke, izvor)
    - izracunaj_iznos:    poslovno pravilo (obračun cijene)
    - sacuvaj_izvjestaj:  format i lokacija izvještaja
    - posalji_mail:       način obavještavanja
Promjena formata CSV-a ili načina slanja maila mijenja istu klasu kao i
promjena obračuna, a obračun se ne može testirati bez prave datoteke.
"""


# 2. Razdvajanje odgovornosti
@dataclass
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci


# 3. Apstrakcija izvora podataka (princip D)
class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class CsvIzvor:
    def __init__(self, putanja: Path):
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(newline="", encoding="utf-8") as f:
            return [
                Rezervacija(red["gost"], int(red["noci"]), float(red["cijena_noci"]))
                for red in csv.DictReader(f)
            ]


# 4. Novi izvor - servis se ne mijenja (princip O)
class JsonIzvor:
    def __init__(self, putanja: Path):
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8") as f:
            return [Rezervacija(**r) for r in json.load(f)]


class ServisRezervacija:
    """Obračun rezervacija; zavisi samo od apstrakcije IzvorRezervacija."""

    def __init__(self, izvor: IzvorRezervacija):
        self.izvor = izvor

    def iznosi(self) -> list[float]:
        return [r.iznos for r in self.izvor.ucitaj()]


def sacuvaj_izvjestaj(iznosi: list[float], putanja: Path) -> None:
    putanja.write_text(str(iznosi), encoding="utf-8")


def posalji_obavjestenje(iznosi: list[float]) -> None:
    print("Poslato: ", sum(iznosi))


# 5. Testovi sa zamjenskim izvorom podataka
class LazniIzvor:
    def __init__(self, rezervacije: list[Rezervacija]):
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


def test_servis_sa_laznim_izvorom():
    izvor = LazniIzvor([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 5, 65)])
    assert ServisRezervacija(izvor).iznosi() == [240, 325]


def test_csv_izvor(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\nAna,3,80\n", encoding="utf-8")
    assert ServisRezervacija(CsvIzvor(p)).iznosi() == [240.0]


def test_json_izvor(tmp_path):
    p = tmp_path / "r.json"
    p.write_text('[{"gost": "Ana", "noci": 3, "cijena_noci": 80}]', encoding="utf-8")
    assert ServisRezervacija(JsonIzvor(p)).iznosi() == [240.0]
