# Käyttöohje

## Asennus

1. Asenna Python `3.10.x` ja [Poetry](https://python-poetry.org/).
2. Klonaa repositorio.
3. Asenna riippuvuudet:

    ```shell
    poetry install
    ```

## Käynnistys

Ennen ensimmäistä käynnistystä, suorita seuraavat toimenpiteet.

1. Asenna riippuvuudet:

    ```shell
    poetry install
    ```

2. Alusta tietokanta

    ```shell
    poetry run invoke build
    ```

Kun edelliset toimenpiteet on suoritettu ainakin kerran, sovellus käynnistyy komennolla:

```shell
poetry run invoke start
```

## Kurssin luominen

Täytä tiedot ja paina "Tallenna"-nappia.

![Kurssin luomisnäkymä](kuvat/kurssin_luomisnakyma.png)

## Laskuri

Kun kurssit on lisätty, niin painamalla laskurivälilehteä pääsee laskurinäkymään.
Kun halutut parametrit on syötetty, niin "Laske"-nappia painamalla pääsee aikataulunäkymään.

![Laskurinäkymä](kuvat/laskurinakyma.png)

## Aikataulu

Aikataulunäkymässä on kurssit jaettu sopiviin vuosiin ja periodeihin laskurinäkymässä annettujen tietojen perusteella.

![Aikataulunäkymä](kuvat/aikataulunakyma.png)
