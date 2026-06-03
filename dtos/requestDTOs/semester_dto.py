from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SemesterDTO:
    """
    Data Transfer Object (DTO) für die Einstellungen eines Studiensemesters.
    Transportiert die eingegebenen Planungsdaten von der UI-Schicht zur Logikschicht.
    Durch frozen=True ist das Objekt nach der Erstellung unveränderlich.
    """
    semester_number: int  # Die laufende Nummer des Semesters (z. B. 1, 2, 3)
    target_ects: int      # Das angestrebte ECTS-Ziel für dieses Semester (z. B. 30)
    start_date: date      # Das offizielle Beginndatum des Semesters
    end_date: date        # Das offizielle Enddatum des Semesters (wichtig für die Restzeit)