"""Mini projekat 1: refaktoring obrade rezervacija (principi S, O i D)."""

import csv
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    def __post_init__(self) -> None:
        if self.noci <= 0:
            raise ValueError(f"Broj noćenja mora biti pozitivan: {self.noci}")
        if self.cijena_noci < 0:
            raise ValueError(f"Cijena ne može biti negativna: {self.cijena_noci}")

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci


# Izvori podataka
class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class CsvIzvor:
    """CSV sa zaglavljem: gost,noci,cijena_noci."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(newline="", encoding="utf-8") as f:
            return [
                Rezervacija(red["gost"], int(red["noci"]), float(red["cijena_noci"]))
                for red in csv.DictReader(f)
            ]


class JsonIzvor:
    """JSON lista objekata sa ključevima gost, noci, cijena_noci."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8") as f:
            return [Rezervacija(**r) for r in json.load(f)]


# Izvještavanje
class Izvjestaj(Protocol):
    def posalji(self, iznosi: list[float]) -> None: ...


class DatotecniIzvjestaj:
    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def posalji(self, iznosi: list[float]) -> None:
        self.putanja.write_text(str(iznosi), encoding="utf-8")


class MailIzvjestaj:
    """Zamjena za slanje maila - ispisuje ukupan iznos."""

    def posalji(self, iznosi: list[float]) -> None:
        print("Poslato:", sum(iznosi))


# Servis
class ServisRezervacija:
    """Obračunava rezervacije; zavisi samo od apstrakcija, ne od konkretnih klasa."""

    def __init__(self, izvor: IzvorRezervacija, izvjestaji: Sequence[Izvjestaj] = ()) -> None:
        self.izvor = izvor
        self.izvjestaji = izvjestaji

    def iznosi(self) -> list[float]:
        return [r.iznos for r in self.izvor.ucitaj()]

    def obradi(self) -> list[float]:
        iznosi = self.iznosi()
        for izvjestaj in self.izvjestaji:
            izvjestaj.posalji(iznosi)
        return iznosi


if __name__ == "__main__":
    folder = Path(__file__).parent
    servis = ServisRezervacija(
        CsvIzvor(folder / "rezervacije.csv"),
        [DatotecniIzvjestaj(folder / "izvjestaj.txt"), MailIzvjestaj()],
    )
    servis.obradi()
