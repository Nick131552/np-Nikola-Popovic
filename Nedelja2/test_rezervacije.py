import pytest

from rezervacije import (
    CsvIzvor,
    DatotecniIzvjestaj,
    JsonIzvor,
    Rezervacija,
    ServisRezervacija,
)


class LazniIzvor:
    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class LazniIzvjestaj:
    def __init__(self) -> None:
        self.primljeno: list[list[float]] = []

    def posalji(self, iznosi: list[float]) -> None:
        self.primljeno.append(iznosi)


REZERVACIJE = [Rezervacija("Ana", 3, 80), Rezervacija("Marko", 5, 65)]


# Testovi servisa sa zamjenskim izvorom podataka
def test_iznosi_sa_laznim_izvorom():
    assert ServisRezervacija(LazniIzvor(REZERVACIJE)).iznosi() == [240, 325]


def test_obradi_salje_iznose_svim_izvjestajima():
    prvi, drugi = LazniIzvjestaj(), LazniIzvjestaj()
    ServisRezervacija(LazniIzvor(REZERVACIJE), [prvi, drugi]).obradi()
    assert prvi.primljeno == drugi.primljeno == [[240, 325]]


def test_prazan_izvor():
    izvjestaj = LazniIzvjestaj()
    assert ServisRezervacija(LazniIzvor([]), [izvjestaj]).obradi() == []
    assert izvjestaj.primljeno == [[]]


# Testovi konkretnih implementacija
def test_csv_izvor(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\nAna,3,80\n", encoding="utf-8")
    assert CsvIzvor(p).ucitaj() == [Rezervacija("Ana", 3, 80.0)]


def test_json_izvor(tmp_path):
    p = tmp_path / "r.json"
    p.write_text('[{"gost": "Ana", "noci": 3, "cijena_noci": 80}]', encoding="utf-8")
    assert JsonIzvor(p).ucitaj() == [Rezervacija("Ana", 3, 80)]


def test_datotecni_izvjestaj(tmp_path):
    p = tmp_path / "izvjestaj.txt"
    DatotecniIzvjestaj(p).posalji([240.0, 325.0])
    assert p.read_text(encoding="utf-8") == "[240.0, 325.0]"


@pytest.mark.parametrize("noci, cijena", [(0, 80), (-1, 80), (3, -10)])
def test_neispravna_rezervacija(noci, cijena):
    with pytest.raises(ValueError):
        Rezervacija("Ana", noci, cijena)
