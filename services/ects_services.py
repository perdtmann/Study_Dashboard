from typing import TYPE_CHECKING

# Schutz vor zyklischen Importen 
if TYPE_CHECKING:
    from models.semester import Semester
    from models.study_program import StudyProgram


class ECTSService:
    """
    Service für die Berechnung von ECTS-Fortschrittswerten.
    Bietet Hilfsfunktionen, um den Studienfortschritt pro Semester 
    oder für das gesamte Studienprogramm mathematisch auszuwerten.
    """

    @staticmethod
    def calculate_semester_progress_percent(semester: 'Semester') -> int:
        """Berechnet den ECTS-Fortschritt eines einzelnen Semesters in Prozent."""
        actual = semester.calculate_current_ects()
        target = semester.target_ects

        # Kontrolle: Wenn das Semesterziel auf 0 steht, ist der Fortschritt 0
        if target == 0:
            return 0

        # Berechnung: (Erreichte ECTS / Ziel-ECTS) * 100
        percent = (actual / target) * 100
        return int(round(percent))

    @staticmethod
    def get_total_study_summary(program: 'StudyProgram') -> str:
        """Liefert eine strukturierte Text-Zusammenfassung der Gesamt-ECTS (z. B. '65 von 180')."""
        actual = program.calculate_total_ects()
        goal = program.total_ects_goal
        return f"{actual} von {goal}"

    @staticmethod
    def calculate_total_progress_ratio(model: 'StudyProgram') -> float:
        """Berechnet das prozentuale Verhältnis des gesamten Studienfortschritts."""
        # Kontrolle: Wenn das Gesamtziel 0 ist, ist der Fortschritt 0,0 %
        if not model or model.total_ects_goal == 0:
            return 0.0

        total_achieved = model.calculate_total_ects()
        return (total_achieved / model.total_ects_goal) * 100