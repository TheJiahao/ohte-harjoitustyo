# Testausdokumentti

Sovellus, poislukien käyttöliittymä, on testattu yksikkötesteillä.
Käyttöliittymä on testattu käsin.

## Yksikkö- ja integraatiotestaus

### Testikattavuus

[![codecov](https://codecov.io/gh/TheJiahao/study-planner/branch/main/graph/badge.svg?token=VSQHAACB32)](https://codecov.io/gh/TheJiahao/study-planner)

Testikattavuus näkyy yllä olevassa kuvakkeessa. Kattavuusraportti löytyy Codecovista painamalla kuvaketta.
`config.py`- ja `build.py`-tiedostoja ei ole testattu yksikkötesteillä.

### Tietokantayhteys

Tietokantayhteydestä vastaava `Database`-luokka on testattu [TestDatabase](https://github.com/TheJiahao/study-planner/blob/main/src/tests/lib/test_database.py)-luokalla.

### Tietorakenteet

Kurssia kuvaava `Course`-luokka on testattu [TestCourse](https://github.com/TheJiahao/study-planner/blob/main/src/tests/entities/test_course.py)-luokalla.

### Sovelluslogiikka

Sovelluslogiikasta vastaava `PlannerService`-luokka on testattu [TestPlannerService](https://github.com/TheJiahao/study-planner/blob/main/src/tests/services/test_planner_service.py)-luokalla.
Testauksessa on käytetty `CourseRepository`-luokan sijaan `FakeCourseRepository`-luokkaa, jotta `CourseRepository`-luokan viat eivät vaikuttaisi tämän luokan testeihin.

Kurssitietojen tuonnista ja viennistä vastaavat `ImportService`- ja `ExportService`-luokat on testattu [TestImportService](https://github.com/TheJiahao/study-planner/blob/main/src/tests/services/test_import_service.py)- ja [TestExportService](https://github.com/TheJiahao/study-planner/blob/main/src/tests/services/test_export_service.py)-luokilla ja [`test/data`](https://github.com/TheJiahao/study-planner/tree/main/src/tests/data)-hakemiston JSON-tiedostoilla.

Aikataulutuksesta vastaava `SchedulerService`-luokka on testattu [TestSchedulerService](https://github.com/TheJiahao/study-planner/blob/main/src/tests/services/test_scheduler_service.py)-luokalla.

### Repository-luokka

Kurssien tallennuksesta vastaava `CourseRepository`-luokka on testattu [TestCourseRepository](https://github.com/TheJiahao/study-planner/blob/main/src/tests/repositories/test_course_repository.py)-luokalla.
Testeissä käytetyn tietokantatiedostin nimi on määritelty `.env.test`-tiedostoon.

## Järjestelmätestaus

### Asennus

Sovelluksen asennusta [käyttöhjeen](dokumentaatio/kaytto-ohje.md) mukaan on testattu Linux-ympäristössä.

### Konfiguraatio

Sovellusta on kokeiltu eri konfiguraatioilla muokkaamalla `.env`-tiedostoa.

### Toiminnallisuudet

Kaikki [vaatimusmäärittelyssä](vaatimusmaarittely.md) esitetyt toiminnallisuudet on testattu käsin.
On yritetty antaa virheellisiä syötteitä, esimerkiksi merkkijonoja numerokenttiin tai tyhjiä syötteitä.
Lisäksi testattu [testisyötteellä](https://github.com/TheJiahao/study-planner/blob/main/src/tests/data/sample_realistic.json), joka sisältää osan TKT- ja MAT-kandiopintojen kurssit.

## Puutteet

Sovellusta ei voida käynnistää, jos tietokantatiedostoon ei ole luku/kirjoitusoikeuksia.
