# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus tuottaa aikataulun opinnoille annettujen vaatimusten (opintopisteraja/periodi, opintojen kesto) perusteella.

## Käyttöliittymäluonnos

![Sovelluksen käyttöliittymäluonnos](kuvat/kayttoliittymahahmotelma.svg)
Sovellus aukeaa kurssien lisäysnäkymään ja oikealta yläkulmalta pääsee vaihtamaan näkymää.
Jos tällainen aikataulunäkymä osoittautuu liian vaativaksi, niin teen näkymästä puurakenteen esim.

```txt
2023 (30 op)
    1. periodi (15 op)
        Kurssi 1
        Kurssi 2
        ...
    2. periodi (15 op)
        ...
2024 (60 op)
    ...
...
```

## Toiminnallisuudet

### Perustoiminnallisuudet

- [x] Kurssien lisäys, muokkaus ja poisto
- [x] Syötettyjen kurssitietojen tyhjentäminen
- [x] Kurssitietojen säilyttäminen tietokannassa
- [x] Aikataulun tuottaminen
  - [x] Esitiedot huomioitu
  - [x] Mahdollisimman vähän tyhjää
  - [x] Periodikohtainen opintopisteraja
  - [x] Periodien ja lukuvuosien kokonaisopintopistemäärä
- [x] Konfiguroitava periodimäärä
- [x] Kurssitietojen lukeminen `json`-tiedostosta
- [x] Kurssitietojen kirjoittaminen `json`-tiedostoon

### Jatkokehitysideoita

- [ ] Aikataulun vieminen `json`-tiedostona
- [ ] Kurssien haku verkosta (jos löytyy API, todennäköisesti ei toteudu)
