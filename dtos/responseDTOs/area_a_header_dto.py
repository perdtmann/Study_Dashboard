from dataclasses import dataclass


@dataclass
class AreaAHeaderDTO:
    """
    Datencontainer (DTO) für den oberen Header-Bereich (Area A).
    Überträgt grundlegende Benutzer- und Studiengangsdaten gesammelt an die Benutzeroberfläche.
    """
    user_name: str               # Der Name des Studierenden (z. B. "Student")
    study_program_name: str      # Der Name des Studiengangs (z. B. "Informatik")
    current_semester_count: int  # Die Gesamtzahl der aktuell im Programm registrierten Semester