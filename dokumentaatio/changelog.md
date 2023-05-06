# Changelog

## Viikko 2

- Lisätty tietokannan käsittelyyn tarvittavat luokat
- Lisätty `Course`-luokka, joka kuvaa kurssia

## Viikko 3

- Refaktoroitu ja testattu `Course`-luokka
- Toteutettu `CourseRepository`-luokka, joka vastaa kurssien tallennuksesta tietokantaan
- Testattu `CourseRepository`-luokan kaikki metodit

## Viikko 4

- Lisätty alustava käyttöliittymä, jolla voi lisätä, muokata ja poistaa kursseja
- Lisätty sovelluslogiikasta vastaava `PlannerService`-luokka

## Viikko 5

- Lisätty aikataulutusalgoritmi `PlannerService`-luokkaan
- Lisätty alustava laskuri- ja aikataulunäkymä
- Lisätty testejä `PlannerService`-luokalle
- Siirretty tietokantayhteyteen liittyvät koodi `Database`-luokkaan

## Viikko 6

- Refaktoroitu `PlannerService`, eriytetty aikataulutusalgoritmi
- Lisätty uusi Kahnin algoritmiin perustuva aikataulutusalgoritmi `Scheduler`-luokkaan
- Lisätty kurssin luontinäkymään Tyhjennä-nappi, jolla voi tyhjentää syötetyt tiedot

## Loppupalautus

- Lisätty opintopistemäärät aikatauluun
- Lisätty alustava tiedoston käsittelijä
- Refaktoroitu `Course`-luokka, poistettu turhat metodit ja tehty oliomuuttujista julkisia
- Lisätty enemmän syötteiden tarkistusta
