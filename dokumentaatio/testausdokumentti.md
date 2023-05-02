# Testausdokumentti

Sovellus, poislukien käyttöliittymä, on testattu yksikkötesteillä.
Käyttöliittymä on testattu käsin.
Lisäksi yksikkötestit on [asetettu](../.vscode/settings.json) suoritettavaksi myös suoraan VSCode-editorilla.

## Yksikkö- ja integraatiotestaus

### Testikattavuus

[![codecov](https://codecov.io/github/TheJiahao/ohte-harjoitustyo/branch/main/graph/badge.svg?token=VSQHAACB32)](https://codecov.io/github/TheJiahao/ohte-harjoitustyo)

Kattavuusraportti löytyy Codecovista painamalla yllä olevaa kuvaketta.
`config.py`- ja `build.py`-tiedostoja ei ole testattu yksikkötesteillä.

### Tietorakenteet ja algoritmit

Kurssia kuvaava `Course`-, tietokanta yhteydestä vastaava `Database`- sekä aikataulutusalgoritmista vastaava `Scheduler`-luokat on testattu vastaavilla [TestCourse](src/tests/entities/test_course.py)-, [TestDatabase](src/tests/entities/test_database.py)- ja [TestDatabase](src/tests/entities/test_scheduler.py)-luokilla.

## Sovelluslogiikka

Sovelluslogiikasta vastaava `PlannerService`-luokka on testattu [TestPlannerService](src/tests/services/test_planner_service.py)-luokalla.
Testauksessa on käytetty `CourseRepository`-luokan sijaan `FakeCourseRepository`-luokkaa, jotta `CourseRepository`-luokan viat eivät vaikuttaisi tämän luokan testeihin.

## Repository-luokka

Kurssien tallennuksesta vastaava `CourseRepository`-luokka on testattu [TestCourseRepository](src/tests/repositories/test_course_repository.py)-luokalla.
Testeissä käytetyn tietokantatiedostin nimi on määritelty `.env.test`-tiedostoon.
