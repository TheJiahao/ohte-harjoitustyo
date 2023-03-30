# Study-planner

Sovellus tuottaa aikataulun opinnoille annettujen vaatimusten (opintopisteraja/periodi, opintojen kesto) perusteella.

## Dokumentaatio

- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](dokumentaatio/tyoaikakirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)

## Asennus

1. Asenna Python `3.11.x`.
2. Asenna riippuvuudet:

    ```shell
    poetry install
    ```

3. Käynnistä sovellus (ei vielä toimi):

    ```shell
    poetry run invoke start
    ```

## Invoke-tehtävät

### Testaus

```shell
poetry run invoke test
```

### Kattavuusraportti

```shell
poetry run invoke coverage-report
```

### Pylint

```shell
poetry run invoke lint
```

### Koodin formatointi

```shell
poetry run invoke format
```
