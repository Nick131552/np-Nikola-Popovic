# np-Nikola-Popovic

Repozitorijum za predmet **Napredno programiranje** (UDG, semestar 7) - vježbe, mini projekti i završni projekat.

## Struktura

| Folder | Sadržaj |
|---|---|
| `Nedelja1/` | Osnove Pythona, `prosjecna_cijena` (zadatak: priprema okruženja), vježbe sa časa |
| `Nedelja2/` | Mini projekat 1: refaktoring obrade rezervacija (OOP i SOLID) |

## Pokretanje

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

ruff check . && ruff format --check .   # linter i formater
pytest                                  # svi testovi
python Nedelja2/rezervacije.py          # pokretanje mini projekta 1
```

---

## Zadatak: priprema radnog okruženja (Nedjelja 1)

- Python 3.12, VS Code, Git/GitHub
- `ruff` i `pytest` su dodati u `requirements-dev.txt`, a podešeni u `pyproject.toml`
- Funkcija `prosjecna_cijena` i testovi: [`Nedelja1/nedelja1.py`](Nedelja1/nedelja1.py)

### Upotrijebljeni upit

Alat: Claude Code (agent u VS Code-u).

> finish the function prosjecna_cijena in nedelja1.py

Polazni kod je bio skelet sa časa (potpis funkcije, `ukupno, noci = 0.0, 0` i `with` blok).

### Uočeni nedostaci generisanog koda i testa

1. **Test ne provjerava ponderisanje.** U testu sa časa oba gosta imaju isti broj noćenja
   (`Ana,2,100` i `Marko,2,50`), pa su ponderisani i običan prosjek isti (75.0). Pogrešna
   implementacija bi prošla test. Dodat je test sa različitim brojem noćenja.
2. **Prazna datoteka** dovodi do dijeljenja nulom. Funkcija sada baca `ValueError`, uz poseban test.
3. **Nedostajuća kolona** izaziva `KeyError` bez jasne poruke o tome šta nije u redu sa datotekom.
4. **Neispravan tip** (npr. `noci = "tri"`) izaziva generičku poruku iz `int()`.
5. **Negativan broj noćenja** se ne odbija i tiho kvari prosjek.
6. **Greška u testu:** pri prepisivanju sa slajda podaci su prepisani pogrešno, pa očekivana
   vrijednost 75.0 nije odgovarala podacima (stvarni rezultat 85.0). Greška je otkrivena tek
   pokretanjem testa, što pokazuje zašto se kod mora izvršiti, a ne samo pročitati.

Na vježbi kritičkog pregleda koda AI je predložio test za kodiranje datoteke koji je **prolazio
i na neispravnom kodu**, pa nije ništa provjeravao. Greška je otkrivena pokretanjem testova na
originalnom kodu i test je ispravljen. Zaključak: test treba provjeriti i tako što se pokrene na
kodu koji sadrži grešku.

---

## Mini projekat 1: refaktoring obrade rezervacija (Nedjelja 2)

Kod: [`Nedelja2/rezervacije.py`](Nedelja2/rezervacije.py), testovi: [`Nedelja2/test_rezervacije.py`](Nedelja2/test_rezervacije.py)

### Polazni kod

Klasa `UpravljanjeRezervacijama` sa slajda 17. Ona učitava CSV, računa iznos, čuva izvještaj i
šalje mail, što su četiri razloga za promjenu u jednoj klasi.

### Dizajn

| Element | Odgovornost | Princip |
|---|---|---|
| `Rezervacija` (dataclass) | podaci i obračun iznosa, validacija | S |
| `IzvorRezervacija` (Protocol) | ugovor za učitavanje podataka | D |
| `CsvIzvor`, `JsonIzvor` | konkretni izvori; JSON je dodat bez izmjene servisa | O |
| `Izvjestaj` (Protocol) | ugovor za izvještavanje | D |
| `DatotecniIzvjestaj`, `MailIzvjestaj` | konkretni izvještaji | S, O |
| `ServisRezervacija` | povezuje izvor i izvještaje; zavisi samo od Protocol-a | D |

Zavisnosti se prosljeđuju kroz konstruktor (injekcija zavisnosti), pa se u testovima lako
zamjenjuju lažnim objektima.

### Testovi

- 3 testa servisa sa zamjenskim izvorom (`LazniIzvor`) i zamjenskim izvještajem (`LazniIzvjestaj`)
- testovi za `CsvIzvor`, `JsonIzvor` i `DatotecniIzvjestaj` (preko `tmp_path`)
- validacija neispravne rezervacije (0 ili negativno noćenja, negativna cijena)



### Ispravke generisanog koda

1. Prva verzija je imala Protocol samo za izvor podataka. Zadatak traži i Protocol za
   izvještavanje, pa je dodat `Izvjestaj` sa dvije implementacije.
2. Prva verzija je imala samo jedan test sa zamjenskim izvorom (traže se najmanje tri), pa su
   dodati testovi za slanje izvještaja i za prazan izvor.
3. Dodata je validacija u `Rezervacija.__post_init__`, jer original prihvata 0 ili negativan
   broj noćenja.
4. Datoteke se otvaraju kroz `with` i uz `encoding="utf-8"`. Original ih nije zatvarao i zavisio
   je od kodiranja sistema.
5. CSV se čita preko `csv.DictReader` (kolone po imenu), umjesto `split(",")` i indeksa `r[1]`,
   `r[2]`, koji se tiho pokvare kada se promijeni redosljed kolona.
6. `ruff` je pronašao importe usred datoteke i pogrešan redosljed importa. Ispravljeno.
