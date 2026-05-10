# Arkkitehtuuri

## Pakkausrakenne

Ohjelman rakenne noudattelee kolmitasoista kerrosarkkitehtuuria, ja koodin pakkausrakenne on seuraava:

![Pakkausrakenne](./kuvat/pakkauskaavio.png)

Pakkaus `ui` sisältää sovelluksen käyttöliittymän, `services` sovelluslogiikan, `repositories` tietokantaoperaatiot ja `entities` sovelluksen käyttämät tietokohteet.

## Käyttöliittymä

Käyttöliittymä sisältää tällä hetkellä erilliset näkymät seuraaville toiminnoille:

- Aloitusnäkymä sovelluksen käynnistyessä
- Kirjautuminen
- Rekisteröityminen
- Päänäkymä
- Uuden tapahtuman luominen/Luodun tapahtuman muokkaaminen

Jokainen näkymä on toteutettu omaan luokkaansa ja niiden näyttämisestä vastaa [UI](../src/ui/ui.py)-luokka. 

Kun käyttäjä kirjautuu sisään tai lisää uuden tapahtuman, päivittää käyttöliittymä päänäkymän näyttämään valitun kuukauden tapahtumat uudelleen. Päänäkymässä käyttäjä voi valita tarkasteltavan kuukauden pudotusvalikosta, minkä perusteella näkymä hakee ja renderöi kyseiseen kuukauteen kuuluvat tapahtumat.

## Sovelluslogiikka

Sovelluksen tietokohteet muodostavat luokat `User` ja `Transaction`, jotka kuvaavat sovelluksen käyttäjiä ja käyttäjien tallentamia tapahtumia:

```mermaid
classDiagram
    Transaction "*" --> "1" User
    class User{
        id
        username
        password
    }
    class Transaction{
        id
        user_id
        year
        month
        transaction_type
        category
        amount
        description
    }
```

Sovelluslogiikasta vastaavat luokat `UserService` ja `TransactionService`.

## Tietokanta

Tietojen tallennuksesta SQLite-tietokantaan vastaa pakkauksen `repositories` luokat `UserRepository` ja `TransactionRepository`. Luokkien toteutusta on mahdollista muuttaa, jos tallennustapaa halutaan myöhemmin muuttaa. 

Sovellus käyttää tietokantatiedoston sijainnin määrittelyyn juureen sijoitettua konfiguraatiota. Tietokantatiedosto luetaan `.env` tiedostosta ympäristömuuttujien asettamiseksi, tai sen puuttuessa käytetään oletusarvoista tietokannan nimeä. Testeissä käytetään erillistä testitietokantaa. 

Tietokanta alustetaan tiedostossa `init_db.py`. Tietokanta sisältää taulut `users` ja `transactions`.

## Päätoiminnallisuudet

Käyttäjän kirjautuessa tai rekisteröityessä sovellukseen, päätyy hän ohjelman pääsivulle, jossa tapahtumat näytetään seuraavasti:

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant TransactionService
    participant UserService
    participant TransactionRepository
    participant Database

    User->>UI: Login/Register
    UI->>TransactionService: get_transaction_months()
    TransactionService->>UserService: get_current_user()
    UserService-->>TransactionService: current_user
    TransactionService->>TransactionRepository: find_months_by_user_id(user_id)
    TransactionRepository->>Database: SELECT ...
    Database-->>TransactionRepository: months
    TransactionRepository-->>TransactionService: months
    TransactionService-->>UI: months

    UI->>UI: set_default_month()

    UI->>TransactionService: get_transactions_for_month(year, month)
    TransactionService->>UserService: get_current_user()
    UserService-->>TransactionService: current_user
    TransactionService->>TransactionRepository: find_by_user_and_time(user_id, year, month)
    TransactionRepository->>Database: SELECT ...
    Database-->>TransactionRepository: transactions
    TransactionRepository-->>TransactionService: transactions
    TransactionService-->>UI: transactions

    UI->>TransactionService: get_summary_for_month(year, month)
    TransactionService-->>UI: income_total, expense_total

    UI->>TransactionService: get_category_distribution_for_month(year, month, transaction_type)
    TransactionService-->>UI: labels, values

    UI->>UI: show_transactions()
    UI->>UI: show_summary()
    UI->>UI: show_category_chart()
```

Sovellukseen käyttöliittymä siirtyy päänäkymään, jossa näytetään käyttäjän tapahtumat valitulta kuukaudelta. Ensin käyttöliittymä pyytää sovelluslogiikalta kaikki ne `(vuosi, kuukausi)`-parit, joilta käyttäjällä on tallennettuja tapahtumia. `TransactionService` hakee kirjautuneen käyttäjän `UserService`:n avulla ja pyytää tämän jälkeen `TransactionRepository`:a hakemaan käyttäjän tapahtumakuukaudet tietokannasta. Kun käyttöliittymä on saanut saatavilla olevat kuukaudet, se valitsee oletuksena näytettävän kuukauden. Tämän jälkeen käyttöliittymä pyytää sovelluslogiikalta valitun kuukauden tapahtumat. Kaikki käyttäjälle ja valitulle kuukaudelle kuuluvat tapahtumat haetaan `TransactionService`:stä, joka pyytää `TransactionRepository`:a hakemaan tiedot tietokannasta.

Kun tapahtumat on palautettu käyttöliittymään, päänäkymä renderöi ne käyttäjälle näkyviin. Tapahtumien näyttämisen lisäksi päänäkymä muodostaa samalle kuukaudelle myös yhteenvedon tuloista ja menoista sekä kategoriakohtaisen kaavion valitun tapahtumatyypin perusteella.
