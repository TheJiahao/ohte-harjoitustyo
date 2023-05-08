# Käyttöohje

## Konfigurointi

Sovelluksen konfiguraatiot ovat `.env`-tiedostossa.
Tällä hetkellä sovelluksella on seuraavat konfiguraatiot:

- `DATABASE_FILENAME`, tietokantatiedoston nimi
- `PERIODS_PER_YEAR`, periodien määrä lukuvuodessa, voidaan esimerkiksi asettaa 6 vastaamaan 4 tavallista periodia + 2 kesäperiodia.
- `COURSE_NAME_WIDTH`, kurssin nimikentän pituus, voidaan säätää tarpeen mukaan pidemmäksi

## Asennus

1. Asenna Python `3.10.x` ja [Poetry](https://python-poetry.org/).
2. Klonaa repositorio.
3. Asenna riippuvuudet:

    ```shell
    poetry install
    ```

## Käynnistys

Sovellus käynnistyy komennolla:

```shell
poetry run invoke start
```

Jos sovellus valittaa, että ei ole oikeuksia tietokantaan, niin säädä tiedoston `data/database.db` (oletusnimi) oikeudet tai poista se ja käynnistä sovellus uudelleen.

## Kurssin luominen

Täytä tiedot ja paina "Tallenna"-nappia.

![Kurssin luomisnäkymä](kuvat/kurssin_luomisnakyma.png)

### Kurssien vienti

Kurssitiedot voidaan tallentaa JSON-tiedostoksi painamalla "Vie"-nappia ja antamalla haluttu tiedostonimi.

### Kurssien tuonti

Kurssitiedot voidaan lukea JSON-tiedostosta painamalla "Tuo"-nappia ja valitsemalla tiedosto.

## Laskuri

Painamalla laskurivälilehteä pääsee laskurinäkymään.
Kun halutut parametrit on syötetty, niin "Laske"-nappia painamalla pääsee aikataulunäkymään.

![Laskurinäkymä](kuvat/laskurinakyma.png)

## Aikataulu

Aikataulunäkymässä on kurssit jaettu sopiviin vuosiin ja periodeihin laskurinäkymässä annettujen ehtojen perusteella.

![Aikataulunäkymä](kuvat/aikataulunakyma.png)
