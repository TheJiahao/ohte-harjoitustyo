import json

from entities.course import Course


class ImportService:
    """Luokka, joka vastaa kurssien tuonnista"""

    def read(self, path: str) -> list[Course]:
        """Lukee JSON-tiedostosta kurssit.

        Args:
            path (str): Tiedoston polku.

        Returns:
            list[Course]: Tiedoston sisältämät kurssit.
        """

        data = ""

        with open(path, mode="r", encoding="utf-8") as file:
            data = json.load(file)

        courses = [self.__decode_course(course_dict) for course_dict in data]

        return sorted(courses, key=lambda x: x.id)

    def __decode_course(self, course_dict: dict) -> Course:
        """Muuntaa sanakirjan kurssiksi.

        Args:
            course_dict (dict):
                Sanakirja, joka sisältää Course-olion oliomuuttujia vastaavat avain-arvo-parit.

        Returns:
            Course: Sanakirjasto muunnettu kurssi.
        """

        course_id = course_dict["id"]
        name = course_dict["name"]
        course_credits = course_dict["credits"]
        timing = set(course_dict["timing"])
        requirements = set(course_dict["requirements"])

        return Course(name, course_credits, timing, requirements, course_id)


import_service = ImportService()
