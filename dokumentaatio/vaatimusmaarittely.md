
# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla käyttäjien on mahdollista seurata henkilökohtaista talouttaan. Käyttäjät voivat kirjata tulojaan ja menojaan, muokata ja poistaa tekemiään kirjauksia sekä tarkastella taloutensa historiallista kehitystä. Sovellukseen on mahdollista rekisteröidä käyttäjiä, jotka näkevät kirjautuessaan omat taloustietonsa.

## Käyttäjät

Alkuvaiheessa sovelluksella on ainoastaan yksi käyttäjärooli eli _normaali käyttäjä_. Myöhemmin sovellukseen saatetaan lisätä _perhetili_, jonka taloustietoja voivat tarkastella kaikki tiliin liitetyt käyttäjät.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- Käyttäjä voi luoda uuden käyttäjätunnuksen
  - Käyttäjätunnuksen täytyy olla uniikki ja pituudeltaan vähintään 3 merkkiä
- Käyttäjä voi kirjautua järjestelmään
  - Kirjautuminen onnistuu syötettäessä olemassa oleva käyttäjätunnus ja salasana kirjautumislomakkeelle
  - Jos käyttäjää ei ole olemassa, tai salasana ei täsmää, ilmoittaa järjestelmä tästä

### Kirjautumisen jälkeen

- Käyttäjä näkee vain omat taloustietonsa
- Käyttäjä voi luoda uuden tulojen ja menojen kuukausitapahtuman
- Käyttäjä voi muokata luotuja kuukausitapahtumia
- Käyttäjä voi poistaa luotuja kuukausitapahtumia
- Käyttäjä voi kirjautua ulos järjestelmästä

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- usean käyttäjän yhteinen _perhetili_
- tietojen vienti esim. CSV-tiedostoon
- taloustietojen koonti kvartaali ja/tai vuositasolla
- analytiikkaa esim. keskikulutuksesta kategorioittain
- ohjelman laajentaminen muilla henkilökohtaisen talouden työkaluilla
