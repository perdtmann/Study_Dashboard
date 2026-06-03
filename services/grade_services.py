import math
from typing import TYPE_CHECKING

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from models.study_program import StudyProgram


class GradeService:
    """
    Service für die mathematische Analyse, Validierung und Prognose von Noten.
    Bietet Hilfsfunktionen, um Notendurchschnitte zu berechnen und Zielprognosen zu erstellen.
    """

    @staticmethod
    def calculate_semester_gpa(program: 'StudyProgram', semester_index: int) -> float:
        """
        Berechnet den Notendurchschnitt (GPA) für ein ganz bestimmtes Semester.
        Nutzt den Index, um das Semester aus der Liste des Studienprogramms auszuwählen.
        """
        # Kontrolle: Befindet sich der angeforderte Index im gültigen Listenbereich?
        if 0 <= semester_index < len(program.semesters):
            target_semester = program.semesters[semester_index]
            return target_semester.get_semester_gpa()

        return 0.0

    @staticmethod
    def predict_needed_grade(program: 'StudyProgram', target_gpa: float) -> float:
        """
        Berechnet, welche Note im nächsten Modul erzielt werden muss,
        um den gewünschten Ziel-Gesamtschnitt exakt zu erreichen.
        """
        all_grades = []

        # Alle bisherigen Noten aus allen Semestern auslesen
        for semester in program.semesters:
            for module in semester.modules:
                if module.is_finished() and module.exam.grade is not None:
                    all_grades.append(module.exam.grade)

        count = len(all_grades)

        # Wenn noch keine Noten vorhanden sind, ist die benötigte Note das Ziel selbst
        if count == 0:
            return target_gpa

        current_sum = sum(all_grades)

        # Mathematische Formel zur Berechnung der nächsten benötigten Note
        needed = ((count + 1) * target_gpa) - current_sum
        return round(needed, 2)

    @staticmethod
    def is_target_reachable(program: 'StudyProgram', target_gpa: float) -> bool:
        """
        Prüft, ob der Ziel-Schnitt mit der nächsten Prüfung theoretisch machbar ist.
        Gibt True zurück, wenn die benötigte Note nicht besser als eine 1.0 sein müsste.
        """
        return GradeService.predict_needed_grade(program, target_gpa) >= 1.0

    @staticmethod
    def get_required_top_grades(program: 'StudyProgram', target_gpa: float) -> int:
        """
        Berechnet, wie viele aufeinanderfolgende 1.0-Noten benötigt werden,
        um einen verfehlten Ziel-Schnitt wieder auszugeben.
        """
        all_grades = []
        for semester in program.semesters:
            for module in semester.modules:
                if module.is_finished() and module.exam.grade is not None:
                    all_grades.append(module.exam.grade)

        count = len(all_grades)
        current_sum = sum(all_grades)

        if count == 0:
            return 0

        # Wenn das Ziel 1.0 ist, kann man es nach einer schlechteren Note nie wieder erreichen
        if target_gpa <= 1.0:
            return 99

        # Berechnung der Anzahl benötigter Top-Noten mittels Aufrundung
        n = (current_sum - count * target_gpa) / (target_gpa - 1.0)
        required_count = math.ceil(n)

        # Falls das Ziel bereits erreicht ist, werden 0 weitere Top-Noten benötigt
        return max(0, required_count)

    @staticmethod
    def validate_grade(grade: float) -> bool:
        """Prüft, ob ein eingegebener Notenwert im zulässigen Bereich von 1.0 bis 5.0 liegt."""
        return 1.0 <= grade <= 5.0