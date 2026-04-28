# Käyttöohje

Lataa projektin viimeisin [release](https://github.com/Jaqt/ot-harjoitustyo/releases).

## Ohjelman käynnistäminen

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

## Aloitusnäkymä

Sovellus käynnistyy aloitusnäkymään:

(./kuvat/aloitusnakyma.png)

Sovelluksen käyttäjät ohjataan joko kirjautumaan tai rekistöimään uusi käyttäjä.

## Kirjautuminen

Rekisteröityneet käyttäjät voivat kirjautua sisään kirjautumisnäkymästä syöttämällä käyttäjätunnus ja salasana.

(./kuvat/kirjautuminen.png)

## Päänäkymä

Kirjautuneet käyttäjät ohjataan päänäkymään, josta näkyy viimeisimmän lisätyn kuukauden tapahtumat. 

(./kuvat/paanakyma.png)

Käyttäjän on tästä näkymästä mahdollista lisätä uusia tapahtumia tai poistaa vanhoja. Dropdown valikosta käyttäjä pystyy valitsemaan menneiden kuukausien tapahtumia näkyviin. Käyttäjät voivat myös kirjautua ulos `kirjaudu ulos` nappia painamalla.