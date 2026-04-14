# Sovellus talouden seurantaan

Tähän tulee **ohjelmistotekniikan** harjoitustyö, aiheena *talouden seuranta*.

## Dokumentaatio

[Changelog](https://github.com/Jaqt/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)

[Vaatimusmäärittely](https://github.com/Jaqt/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Tuntikirjanpito](https://github.com/Jaqt/ot-harjoitustyo/blob/main/dokumentaatio/tuntikirjanpito.md)

[Arkkitehtuurikuvaus](https://github.com/Jaqt/ot-harjoitustyo/blob/main/dokumentaatio/arkkitehtuuri.md)


## Asennus

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Luo tarvittavat ympäristömuuttujat (valinnainen):

Luo .env tiedosto
```bash
DATABASE_FILENAME = "tähän sqlite3 tietokannan nimi"
```

3. Suorita vaadittavat alustustoimenpiteet komennolla:

```bash
poetry run python src/init_db.py
```

4. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```
## Testaus

Voit suorittaa testit komennolla:

```bash
poetry run invoke test
```

## Testikattavuus

Voit generoida testikattavuusraportin komennolla:

```bash
poetry run invoke coverage-report
```

## Pylint

Voit suorittaa linttauksen komennolla:

```bash
poetry run invoke lint
```
