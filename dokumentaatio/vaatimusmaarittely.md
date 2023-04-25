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

### Perusversio

- [x] Kurssien lisäys tietoineen (nimi, opintopisteet, ajoitus, edeltävät opinnot)
- [x] Lisättyjen kurssien muokkaus ja selaaminen
- [x] Lisättyjen kurssien poistaminen
- [x] Kurssitietojen säilyttäminen tietokannassa
- [x] Aikataulu topologisessa järjestyksessä (esitietovaatimukset täyttyvät ennen kurssia)

### Jatkokehitysideoita

- [ ] Kurssitietojen lukeminen `json`-tiedostosta
- [ ] Aikataulun vieminen `json`-tiedostona
- [ ] Opintopisteyläraja periodille
- [ ] Periodin ja lukuvuoden opintopistemäärän näyttäminen
- [ ] Kurssien haku verkosta (jos löytyy API, todennäköisesti ei toteudu)
- [ ] Periodien työmäärän tasapainottaminen
- [ ] Kesäperiodit
