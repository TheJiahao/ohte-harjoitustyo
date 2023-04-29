# Arkkitehtuuri

## Sovelluslogiikka

Sovelluksen ainoa oma tietorakenne on `Course`-luokka, joka kuvaa kurssia.
Lisäksi sovelluksessa on aikataulutuksesta vastaava `Scheduler`-luokka ja sovelluslogiikasta vastaava `PlannerService`-luokka.
Luokkien riippuvuudet on esitetty seuraavassa luokkakaaviossa.

```mermaid
classDiagram
    PlannerService ..> Course
    PlannerService ..> Scheduler
    Scheduler -- "*" Course

    class Course {
        -name
        -credits
        -timing
        -requirements
        -id
    }

    class Scheduler {
        +get_schedule()
    }
```

## Algoritmi

Sovelluksen toiminta perustuu suunnatun verkon topologiseen järjestykseen  ja Kahnin algoritmiin [^tirakirja] [^kahn].

(Tähän tulee algoritmin selitys)

## Toiminnallisuudet

### Uuden kurssin tallentaminen

Oletetaan, että käyttäjä syöttää uuden kurssin "Ohte" tiedot ja painaa Tallenna-nappia.
Tällöin sovelluksen kontrolli etenee seuraavasti:

```mermaid
sequenceDiagram
actor User

User ->> UI: click "save" button
UI ->> ohte: Course("Ohte", 5, {4})
ohte -->> UI: ohte
UI ->> PlannerService: create_course(ohte)
PlannerService ->> CourseRepository: create(ohte)
CourseRepository ->> CourseRepository: write(ohte)
CourseRepository -->> UI: 
```

### Olemassaolevan kurssin muokkaaminen

Oletetaan, että käyttäjä valitsee valikosta olemassaolevan kurssin "Ohte" (id=1), päivittää tietoja sekä painaa Tallenna-nappia.
Tällöin sovelluksen kontrolli etenee seuraavasti:

```mermaid
sequenceDiagram
actor User

User ->> UI: click "save" button
UI ->> ohte: Course("Ohte", 5, {4}, id=1)
ohte -->> UI: ohte
UI ->> PlannerService: create_course(ohte)
PlannerService ->> CourseRepository: create(ohte)
CourseRepository ->> ohte: id()
ohte -->> CourseRepository: 1
CourseRepository ->> CourseRepository: delete(1)
CourseRepository ->> CourseRepository: write(ohte)
CourseRepository -->> UI: 
UI -->> User: clear fields
```

### Olemassaolevan kurssin poistaminen

Oletetaan, että käyttäjä valitsee valikosta olemassaolevan kurssin "Ohte" (id=1) ja painaa Poista-nappia.
Tällöin sovelluksen kontrolli etenee seuraavasti:

```mermaid
sequenceDiagram
actor User

User ->> UI: click "delete" button
UI -->> User: confirm delete
User ->> UI: "yes"
UI ->> PlannerService: delete_course(1)
PlannerService ->> CourseRepository: delete(1)
CourseRepository -->> UI: 
UI -->> User: clear fields
```

### Aikataulun laskeminen

Oletetaan, että käyttäjä on syöttänyt kurssit ja parametrit aikataulua varten sekä painaa Laske-nappia.
Tällöin sovelluksen kontrolli etenee seuraavasti:

```mermaid
sequenceDiagram
actor User

User ->> UI: click "calculate" button
UI ->> PlannerService: set(year, period, max_credits)
PlannerService -->> UI: 
UI ->> UI: handle_show_schedule_view()
UI ->> PlannerService: get_schedule()
PlannerService ->> PlannerService: get_all_courses()
PlannerService ->> scheduler: Scheduler(courses, starting_period, periods_per_year, max_credits)
scheduler -->> PlannerService: scheduler
PlannerService ->> scheduler: get_schedule()
scheduler -->> PlannerService: schedule

PlannerService -->> UI: schedule
UI -->> User: show schedule
```

[^tirakirja]: Antti Laaksonen, *Tietorakenteet ja algoritmit*, 2022. https://www.cs.helsinki.fi/u/ahslaaks/tirakirja/
[^kahn]: Geeksforgeeks, *Kahn’s algorithm for Topological Sorting*. https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/, luettu 28.4.2023.
