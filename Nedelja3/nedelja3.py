# Kod za nedelju 3 - teorija je u nedelja3_teorija.md
from dataclasses import dataclass, field
from functools import lru_cache

import pytest

# from config import postavke


# ============================== Factory ==============================
TARIFE: dict[str, type] = {}


def registruj(naziv: str):
    def dekorator(klasa):
        TARIFE[naziv] = klasa
        return klasa

    return dekorator


@registruj("standardna")
class Standardna:
    def cijena(self, osnovna: float) -> float:
        return osnovna


@registruj("sezonska")
class Sezonska:
    def cijena(self, osnovna: float) -> float:
        return osnovna * 1.3


def kreiraj_tarifu(naziv: str):
    if naziv not in TARIFE:
        raise ValueError(f"Nepoznata tarifa: {naziv}")
    return TARIFE[naziv]()


print(kreiraj_tarifu("sezonska").cijena(100))  # 130.0


# ============================== Builder ==============================
@dataclass
class Rezervacija:
    gost: str
    noci: int
    dodaci: list[str] = field(default_factory=list)


class RezervacijaBuilder:
    def __init__(self, gost: str):
        self._gost, self._noci, self._dodaci = gost, 1, []

    def noci(self, n: int):
        self._noci = n
        return self

    def dodatak(self, naziv: str):
        self._dodaci.append(naziv)
        return self

    def build(self) -> Rezervacija:
        if self._noci < 1:
            raise ValueError("Najmanje jedno noćenje")
        return Rezervacija(self._gost, self._noci, self._dodaci)


r = RezervacijaBuilder("Ana").noci(3).dodatak("doručak").build()
print(r)


# ============================== Singleton ==============================
# 1) Modul je singleton
# config.py
postavke = {"okruzenje": "razvoj", "debug": True}

# drugi modul
# from config import postavke  # uvijek isti objekat (import je na vrhu datoteke)


# 2) Keširana funkcija
@lru_cache(maxsize=1)
def klijent_baze():
    print("Uspostavljanje veze...")
    return object()


a = klijent_baze()
b = klijent_baze()
assert a is b  # ista instanca

# Za testove: pozvati klijent_baze.cache_clear() ili proslijediti zavisnost
# kroz konstruktor (princip D).


# ============================== Adapter ==============================
class StariSistemCijena:
    def cijena_u_centima(self, soba: str) -> int:
        return 8500


class CjenovnikAdapter:
    def __init__(self, sistem: StariSistemCijena):
        self.sistem = sistem

    def cijena(self, soba: str) -> float:
        return self.sistem.cijena_u_centima(soba) / 100


def prikazi(cjenovnik, soba: str) -> None:
    print(f"{soba}: {cjenovnik.cijena(soba):.2f} EUR")


prikazi(CjenovnikAdapter(StariSistemCijena()), "dvokrevetna")
# dvokrevetna: 85.00 EUR


# ============================== Dekorator ==============================
class Tarifa:
    def cijena(self, osnovna: float) -> float:
        return osnovna


class SaPopustom:
    def __init__(self, tarifa, popust: float):
        self.tarifa, self.popust = tarifa, popust

    def cijena(self, osnovna: float) -> float:
        return self.tarifa.cijena(osnovna) * (1 - self.popust)


class SaTaksom:
    def __init__(self, tarifa, taksa: float = 1.0):
        self.tarifa, self.taksa = tarifa, taksa

    def cijena(self, osnovna: float) -> float:
        return self.tarifa.cijena(osnovna) + self.taksa


t = SaTaksom(SaPopustom(Tarifa(), 0.1))
print(t.cijena(100))  # 91.0


# ============================== Facade ==============================
class Dostupnost:
    def provjeri(self, soba, noci):
        return True


class Cjenovnik:
    def iznos(self, soba, noci):
        return 85.0 * noci


class Placanje:
    def naplati(self, iznos):
        return True


class Potvrda:
    def posalji(self, gost):
        print("Potvrda:", gost)


class RezervacijaFasada:
    def __init__(self):
        self.d, self.c = Dostupnost(), Cjenovnik()
        self.p, self.k = Placanje(), Potvrda()

    def rezervisi(self, gost, soba, noci) -> bool:
        if not self.d.provjeri(soba, noci):
            return False
        if not self.p.naplati(self.c.iznos(soba, noci)):
            return False
        self.k.posalji(gost)
        return True


RezervacijaFasada().rezervisi("Ana", "dvokrevetna", 3)


# ============================== Zadatak ==============================
# Scenarij A: Aplikacija ucitava tarifu prema nazivu iz konfiguracione datoteke
# ("standardna", "sezonska", "Promotivna").
#
# Scenarij B: Sistem rezervacija treba da koristi stari sistem cijena ciji metod
# vraca cijenu u centima, dok ostatak koda ocekuje cijenu u eurima.
#
# Zadaci:
# 1. Imenovati: sablon za svaki scenarij i obrazloziti izbor
# 2. Skicirati: dijagram klasa (papir ili Mermaid)
# 3. Implementovati: dva scenarija uz AI asistenta
# 4. Testirati: nepoznat naziv tarife mora izazvati jasnu gresku
# 5. Procijeniti: da li je sablon zaista potreban u svakom scenariju


# ============================== Rjesenje ==============================
# 1. Imenovanje sablona
"""
Scenarij A -> Factory (sa registrom) - vec implementiran gore (TARIFE, registruj)
    Naziv tarife dolazi iz konfiguracije kao string, a program treba da napravi
    odgovarajuci objekat. Registar (dict naziv -> klasa) zamjenjuje lanac if/elif;
    nova tarifa se dodaje dekoratorom @registruj bez izmjene fabrike (princip O).

Scenarij B -> Adapter - vec implementiran gore (CjenovnikAdapter)
    Stari sistem ima drugaciji interfejs (cijena u centima) od onog koji ostatak koda
    ocekuje (cijena u eurima). Omotac prevodi jedan interfejs u drugi, pa se ni stari
    sistem ni klijentski kod (prikazi) ne mijenjaju.
"""

# 2. Dijagram klasa (Mermaid)
"""
classDiagram
    class Fabrika {
        TARIFE: dict
        +registruj(naziv)
        +kreiraj_tarifu(naziv)
    }
    class Standardna {
        +cijena(osnovna) float
    }
    class Sezonska {
        +cijena(osnovna) float
    }
    class Promotivna {
        +cijena(osnovna) float
    }
    Fabrika ..> Standardna : kreira
    Fabrika ..> Sezonska : kreira
    Fabrika ..> Promotivna : kreira

    class StariSistemCijena {
        +cijena_u_centima(soba) int
    }
    class CjenovnikAdapter {
        +sistem: StariSistemCijena
        +cijena(soba) float
    }
    class prikazi {
        <<klijent>>
    }
    CjenovnikAdapter o-- StariSistemCijena
    prikazi ..> CjenovnikAdapter : cijena(soba)
"""


# 3. Implementacija - Scenarij A: nova tarifa bez izmjene fabrike
@registruj("promotivna")
class Promotivna:
    def cijena(self, osnovna: float) -> float:
        return osnovna * 0.8


def tarifa_iz_konfiguracije(vrijednost: str):
    """Naziv iz konfiguracije moze biti "Promotivna" ili " sezonska " - normalizuje se."""
    return kreiraj_tarifu(vrijednost.strip().lower())


# 3. Implementacija - Scenarij B: CjenovnikAdapter gore je cijelo rjesenje.


# 4. Testovi
def test_kreiraj_poznatu_tarifu():
    assert isinstance(kreiraj_tarifu("sezonska"), Sezonska)


def test_nova_tarifa_bez_izmjene_fabrike():
    assert kreiraj_tarifu("promotivna").cijena(100) == 80.0


def test_naziv_iz_konfiguracije_ne_zavisi_od_velicine_slova():
    assert isinstance(tarifa_iz_konfiguracije("Promotivna"), Promotivna)


def test_nepoznata_tarifa_izaziva_jasnu_gresku():
    with pytest.raises(ValueError, match="Nepoznata tarifa: vikend"):
        kreiraj_tarifu("vikend")


def test_adapter_pretvara_cente_u_eure():
    assert CjenovnikAdapter(StariSistemCijena()).cijena("dvokrevetna") == 85.0


def test_klijent_radi_sa_adapterom(capsys):
    prikazi(CjenovnikAdapter(StariSistemCijena()), "dvokrevetna")
    assert capsys.readouterr().out == "dvokrevetna: 85.00 EUR\n"


def test_builder_odbija_nula_nocenja():
    with pytest.raises(ValueError, match="Najmanje jedno"):
        RezervacijaBuilder("Ana").noci(0).build()


# 5. Procjena - da li je sablon zaista potreban
"""
Scenarij A - Factory: DA, opravdan.
    Naziv stize kao string iz konfiguracije, pa je preslikavanje naziv -> klasa
    neophodno u nekom obliku. Registar je zapravo samo dict, sto je najjednostavniji
    oblik fabrike. Dekorator @registruj se isplati tek kada tarifa ima vise;
    za 3 tarife bi bio dovoljan i obican dict {"standardna": Standardna, ...}.
    Bez konfiguracije (tarifa poznata u kodu) fabrika ne bi bila potrebna.

Scenarij B - Adapter: DA, opravdan.
    Stari sistem se ne smije mijenjati, a bez adaptera bi se "/ 100" ponavljalo
    na svakom mjestu poziva - lako je zaboraviti konverziju i dobiti cijenu 100x
    vecu. Adapter drzi konverziju na jednom mjestu. Ako bi se stari sistem pozivao
    samo na jednom mjestu, obicna funkcija bi bila dovoljna.
    Napomena: za novac je float neprecizan; u produkciji bi se koristio Decimal
    ili bi se iznosi drzali u centima kao int.
"""
