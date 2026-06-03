from dataclasses import dataclass


@dataclass
class AreaB1QuantGoalsDTO:
    """
    Datencontainer (DTO) für die quantitativen Ziele (Area B1).
    Überträgt ECTS-Fortschritte und Fristen gebündelt vom Service zur Benutzeroberfläche.
    """
    current_semester_ects: int      # Erreichte ECTS-Punkte im aktuellen Semester
    semester_target_ects: int       # Angestrebtes ECTS-Ziel für das aktuelle Semester
    total_study_ects: str           # KORREKTUR: Jetzt 'str' für Text-Zusammenfassungen wie "15 von 180"
    total_progress_percent: int     # Prozentualer Fortschritt des aktuellen Semesters
    days_until_semester_end: int    # Verbleibende Tage bis zum offiziellen Semesterende