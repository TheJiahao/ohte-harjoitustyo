import json

from entities.course import Course


class ExportService:
    """Luokka, joka vastaa kurssien viennistä."""

    def write(self, courses: list[Course], path: str) -> None:
        """Kirjoittaa JSON-tiedostoon kurssit. Ylikirjoittaa tiedoston.

        Args:
            courses (list[Course]): Kirjoitettavat kurssit.
            path (str): Kirjoitettavan tiedoston polku.
        """

        with open(path, mode="w", encoding="utf-8") as file:
            json.dump(
                sorted(courses, key=lambda x: x.id),
                file,
                default=self.__encode_course,
                indent=4,
            )

    def __encode_course(self, course: Course) -> dict:
        """Muuntaa kurssin sanakirjaksi.

        Args:
            course (Course): Muunnettava kurssi.

        Returns:
            dict: Kurssi sanakirjana.
        """

        result = {
            "id": course.id,
            "name": course.name,
            "credits": course.credits,
            "timing": sorted(course.timing),
            "requirements": sorted(course.requirements),
        }

        return result


export_service = ExportService()
