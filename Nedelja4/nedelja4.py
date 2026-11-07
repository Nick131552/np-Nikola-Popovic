# Kod za nedelju 4 - teorija je u nedelja4_teorija.md
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

import pytest

# ============================== Strategy ==============================
Metrika = Callable[[list[float], list[float]], float]


def mae(y, p):
    return sum(abs(a - b) for a, b in zip(y, p, strict=True)) / len(y)


def mse(y, p):
    return sum((a - b) ** 2 for a, b in zip(y, p, strict=True)) / len(y)


METRIKE: dict[str, Metrika] = {"mae": mae, "mse": mse}


def evaluiraj(y, p, metrika: str = "mae") -> float:
    return METRIKE[metrika](y, p)


y_tacno, y_pred = [3.0, 5.0], [2.0, 7.0]
print(evaluiraj(y_tacno, y_pred))  # 1.5
print(evaluiraj(y_tacno, y_pred, "mse"))  # 2.5


# ============================== Observer ==============================
class Trener:
    def __init__(self):
        self.pretplatnici = []

    def pretplati(self, fn):
        self.pretplatnici.append(fn)

    def _objavi(self, dogadjaj, **podaci):
        for fn in self.pretplatnici:
            fn(dogadjaj, **podaci)

    def treniraj(self, gubici):
        for epoha, gubitak in enumerate(gubici):
            self._objavi("kraj_epohe", epoha=epoha, gubitak=gubitak)


def log(dogadjaj, **d):
    print(dogadjaj, d)


def alarm(dogadjaj, **d):
    if d["gubitak"] > 1.0:
        print("UPOZORENJE: gubitak je previsok")


t = Trener()
t.pretplati(log)
t.pretplati(alarm)
t.treniraj([0.9, 1.2])


# ============================== Template Method ==============================
class Eksperiment(ABC):
    def pokreni(self):  # okvir je fiksan
        podaci = self.ucitaj()
        podaci = self.pripremi(podaci)
        model = self.treniraj(podaci)
        return self.evaluiraj(model, podaci)

    def pripremi(self, podaci):  # podrazumijevano
        return podaci

    @abstractmethod
    def ucitaj(self): ...

    @abstractmethod
    def treniraj(self, podaci): ...

    @abstractmethod
    def evaluiraj(self, model, podaci): ...


class ProsjecniEksperiment(Eksperiment):
    def ucitaj(self):
        return [1, 2, 3, 4]

    def treniraj(self, podaci):
        return sum(podaci) / len(podaci)

    def evaluiraj(self, model, podaci):
        return abs(model - podaci[-1])


print(ProsjecniEksperiment().pokreni())  # 1.5


# ============================== Chain of Responsibility ==============================
def nije_prazan(tekst):
    if not tekst.strip():
        raise ValueError("Prazan unos")
    return tekst


def max_duzina(tekst):
    if len(tekst) > 500:
        raise ValueError("Predugačak unos")
    return tekst


def bez_tajni(tekst):
    if "lozinka" in tekst.lower():
        raise ValueError("Unos sadrži osjetljive podatke")
    return tekst


def provedi(tekst, provjere):
    for provjera in provjere:
        tekst = provjera(tekst)
    return tekst


LANAC = [nije_prazan, max_duzina, bez_tajni]
provedi("Objasni dekoratore", LANAC)  # prolazi
try:
    provedi("moja lozinka je 123", LANAC)  # ValueError
except ValueError as e:
    print("Greška:", e)


# ============================== Command ==============================


# ============================== State ==============================


# ============================== Iterator ==============================


# ============================== Zadatak ==============================
# Scenarij A: Sistem salje obavjestenje na e-postu, Slack i SMS kada tacnost
# modela padne ispod praga.
#
# Scenarij B: Zahtjev prolazi autentikaciju, ogranicenje broja zahtjeva i
# validaciju prije nego stigne do modela.
#
# Scenarij C: Postoje cetiri nacina obracuna cijene (standardna, studentska,
# akcijska, VIP) koji se biraju u toku rada.
#
# Scenarij D: Svaki model prolazi iste korake (ucitavanje, priprema, treniranje,
# evaluacija), a razlikuje se samo treniranje.
#
# Zadaci:
# 1. Imenovati: sablon za svaki scenarij
# 2. Skicirati: dijagram klasa u Mermaid-u ili na papiru
# 3. Implementovati: dva scenarija uz AI asistenta
# 4. Kritikovati: zatraziti od asistenta procjenu sta je u rjesenju suvisno
# 5. Predstaviti: rjesenje u dva minuta


# ============================== Rjesenje ==============================
# 1. Imenovanje sablona
"""
Scenarij A -> Observer
    Jedan dogadjaj (pad tacnosti) treba da obavijesti vise strana. Monitor drzi listu
    pretplatnika i ne zna da li salje e-postu, Slack ili SMS; novi kanal = nova pretplata.

Scenarij B -> Chain of Responsibility (pipeline)
    Zahtjev prolazi kroz niz provjera; svaka moze da ga odbije i prekine obradu.
    Provjere se dodaju, uklanjaju i premjestaju nezavisno.

Scenarij C -> Strategy
    Cetiri zamjenjiva algoritma obracuna iza istog interfejsa, birana u toku rada.
    Umjesto lanca if/elif - dict naziv -> funkcija.

Scenarij D -> Template Method
    Okvir (ucitaj -> pripremi -> treniraj -> evaluiraj) je fiksan u baznoj klasi,
    a podklase mijenjaju samo korak treniraj().
"""

# 2. Dijagram klasa: Mermaid blok u nedelja4_teorija.md (pod "Zadatak")


# 3. Implementacija - Scenarij A (Observer)
Pretplatnik = Callable[[str], None]


class MonitorTacnosti:
    """Obavjestava sve pretplatnike kada tacnost modela padne ispod praga."""

    def __init__(self, prag: float) -> None:
        self.prag = prag
        self._pretplatnici: list[Pretplatnik] = []

    def pretplati(self, pretplatnik: Pretplatnik) -> None:
        self._pretplatnici.append(pretplatnik)

    def prijavi_tacnost(self, tacnost: float) -> None:
        if tacnost < self.prag:
            poruka = f"Tacnost modela pala na {tacnost:.2f} (prag {self.prag:.2f})"
            for pretplatnik in self._pretplatnici:
                pretplatnik(poruka)


def posalji_email(poruka: str) -> None:
    print("E-posta:", poruka)


def posalji_slack(poruka: str) -> None:
    print("Slack:", poruka)


def posalji_sms(poruka: str) -> None:
    print("SMS:", poruka)


# 3. Implementacija - Scenarij B (Chain of Responsibility)
@dataclass
class Zahtjev:
    korisnik: str
    token: str
    tekst: str


class OdbijenZahtjev(Exception):
    """Neka provjera u lancu je odbila zahtjev."""


Provjera = Callable[[Zahtjev], None]

VALIDNI_TOKENI = {"abc123"}


def autentikacija(zahtjev: Zahtjev) -> None:
    if zahtjev.token not in VALIDNI_TOKENI:
        raise OdbijenZahtjev("Neispravan token")


class OgranicenjeZahtjeva:
    """Najvise `limit` zahtjeva po korisniku (klasa jer mora da pamti brojac)."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self._broj: dict[str, int] = {}

    def __call__(self, zahtjev: Zahtjev) -> None:
        broj = self._broj.get(zahtjev.korisnik, 0)
        if broj >= self.limit:
            raise OdbijenZahtjev(f"Prekoracen limit od {self.limit} zahtjeva")
        self._broj[zahtjev.korisnik] = broj + 1


def validacija(zahtjev: Zahtjev) -> None:
    if not zahtjev.tekst.strip():
        raise OdbijenZahtjev("Prazan zahtjev")


def obradi(zahtjev: Zahtjev, provjere: list[Provjera], model: Callable[[str], str]) -> str:
    """Pusta zahtjev kroz sve provjere redom; tek onda poziva model."""
    for provjera in provjere:
        provjera(zahtjev)
    return model(zahtjev.tekst)


# Testovi - Scenarij A
def test_pad_tacnosti_obavjestava_sve_pretplatnike():
    primljeno: list[str] = []
    monitor = MonitorTacnosti(prag=0.9)
    for _ in range(3):  # e-posta, Slack, SMS
        monitor.pretplati(primljeno.append)
    monitor.prijavi_tacnost(0.85)
    assert len(primljeno) == 3
    assert "0.85" in primljeno[0]


def test_tacnost_iznad_praga_ne_salje_nista():
    primljeno: list[str] = []
    monitor = MonitorTacnosti(prag=0.9)
    monitor.pretplati(primljeno.append)
    monitor.prijavi_tacnost(0.9)  # granica: nije ispod praga
    monitor.prijavi_tacnost(0.95)
    assert primljeno == []


# Testovi - Scenarij B
def lazni_model(tekst: str) -> str:
    return f"odgovor na: {tekst}"


def lanac() -> list[Provjera]:
    return [autentikacija, OgranicenjeZahtjeva(limit=2), validacija]


def test_ispravan_zahtjev_stize_do_modela():
    z = Zahtjev("ana", "abc123", "zdravo")
    assert obradi(z, lanac(), lazni_model) == "odgovor na: zdravo"


def test_neispravan_token_prekida_lanac():
    pozvan = []
    with pytest.raises(OdbijenZahtjev, match="token"):
        obradi(Zahtjev("ana", "pogresan", "zdravo"), lanac(), pozvan.append)
    assert pozvan == []  # model nije pozvan


def test_prekoracen_limit():
    provjere = lanac()
    z = Zahtjev("ana", "abc123", "zdravo")
    obradi(z, provjere, lazni_model)
    obradi(z, provjere, lazni_model)
    with pytest.raises(OdbijenZahtjev, match="limit"):
        obradi(z, provjere, lazni_model)


def test_prazan_zahtjev_odbijen():
    with pytest.raises(OdbijenZahtjev, match="Prazan"):
        obradi(Zahtjev("ana", "abc123", "   "), lanac(), lazni_model)


# 4. Kritika - sta je suvisno
"""
Scenarij A:
    - MonitorTacnosti je mogao biti samo funkcija koja prima listu pretplatnika;
      klasa ima smisla jer drzi prag i listu na jednom mjestu.
    - Klase EmailObavjestenje, SlackObavjestenje... (cesti AI prijedlog) su suvisne -
      pretplatnik je obicna funkcija, nema potrebe za ABC-om i nasljedjivanjem.
    - Nema odjave pretplate (odjavi) jer je zadatak ne trazi.

Scenarij B:
    - Za tri fiksne provjere bi i jedna funkcija sa tri if-a bila dovoljna. Lanac se
      isplati jer se provjere cesto mijenjaju (npr. dodavanje guardraila).
    - Klasicna implementacija gdje svaki obradjivac cuva referencu na sljedeceg
      (set_next) je suvisna u Pythonu - lista funkcija i petlja rade isto.
    - Klasa je potrebna samo za OgranicenjeZahtjeva, jer pamti stanje (brojac).

Scenariji C i D (nisu implementirani):
    - C: dict {"standardna": f1, "studentska": f2, ...} - Strategy bez ijedne klase.
    - D: funkcija koja prima korak treniraj kao argument je jednostavnija od
      bazne klase; Template Method sa klasom se isplati tek kada ima vise koraka
      koji se mogu mijenjati.
"""
