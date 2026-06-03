import logging
from models.enums import DegreeType
from models.semester import Semester

# Logger für diese Datei initialisieren (schreibt in data/app.log)
logger = logging.getLogger(__name__)


class StudyProgram:
    """
    Repräsentiert das gesamte Studienprogramm eines Benutzers.
    Verwaltet globale Ziele, berechnet die Gesamt-Leistung
    und hält eine Liste aller zugehörigen Semester.
    """

    def __init__(self, name: str, degree: DegreeType, target_gpa: float, total_ects_goal: int,
                 current_semester_index: int, user_name: str = "Student"):
        # Speicherung der Kern- und Zieldaten des Studiums
        self.name = name
        self.degree = degree
        self.target_gpa = target_gpa
        self.total_ects_goal = total_ects_goal

        # Laufende Parameter des Dashboards
        self.current_semester = current_semester_index
        self.user_name = user_name

        # Liste zur Verwaltung aller Studiensemester
        self.semesters: list = []

    def calculate_total_gpa(self) -> float:
        """Berechnet den aktuellen Gesamt-Notendurchschnitt (GPA) über das gesamte Studium."""
        total_grade_sum = 0.0
        total_modules_count = 0

        for semester in self.semesters:
            for module in semester.modules:
                # Nur abgeschlossene Module mit gültiger Note fließen in die Berechnung ein
                if module.is_finished() and module.exam.grade is not None:
                    total_grade_sum += module.exam.grade
                    total_modules_count += 1

        if total_modules_count == 0:
            return 0.0

        return total_grade_sum / total_modules_count

    def calculate_total_ects(self) -> int:
        """Berechnet die Summe aller bereits erreichten ECTS-Punkte über alle Semester hinweg."""
        total_ects = 0
        for semester in self.semesters:
            total_ects += semester.calculate_current_ects()
        return total_ects

    def get_performance_status(self) -> str:
        """
        Ermittelt den Status für das Ampelsystem des Dashboards.
        Vergleicht den aktuellen Schnitt mit dem gesetzten Ziel-Schnitt.
        """
        current_gpa = self.calculate_total_gpa()

        # Noch keine Noten vorhanden -> Neutraler Zustand
        if current_gpa == 0.0:
            return "NEUTRAL"

        # Ampelsystem-Logik basierend auf dem Ziel-Schnitt (target_gpa)
        if current_gpa <= self.target_gpa - 0.1:
            return "GREEN"
        elif current_gpa == self.target_gpa:
            return "YELLOW"
        else:
            return "RED"

    def add_semester(self, semester: Semester) -> None:
        """Fügt ein neues Semester zum Studienprogramm hinzu, sofern es vom Typ Semester ist."""
        if isinstance(semester, Semester):
            self.semesters.append(semester)
            logger.info(f"Semester {semester.number} wurde zum Studienprogramm hinzugefügt.")
        else:
            logger.error("Fehler: Es können nur Objekte vom Typ 'Semester' hinzugefügt werden.")

    def to_dict(self) -> dict:
        """Konvertiert das Studienprogramm in ein Dictionary für die JSON-Speicherung."""
        return {
            "name": self.name,
            "degree": self.degree.value if hasattr(self.degree, 'value') else self.degree,
            "target_gpa": self.target_gpa,
            "total_ects_goal": self.total_ects_goal,
            "current_semester_index": self.current_semester,
            "user_name": self.user_name,
            "semesters": [s.to_dict() for s in self.semesters]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StudyProgram':
        """Erstellt ein Studienprogramm mitsamt allen Semestern aus einem Dictionary."""
        name = data.get("name", "Unbekanntes Studium")
        degree = DegreeType(data.get("degree", "B.Sc."))
        target_gpa = data.get("target_gpa", 2.0)
        total_ects_goal = data.get("total_ects_goal", 180)
        user_name = data.get("user_name", "Student")
        current_idx = data.get("current_semester_index", 1)

        # Neues Studienprogramm-Objekt instanziieren
        program = cls(
            name=name,
            degree=degree,
            target_gpa=target_gpa,
            total_ects_goal=total_ects_goal,
            current_semester_index=current_idx,
            user_name=user_name
        )

        # Semester-Liste rekursiv aus den JSON-Daten wiederaufbauen
        if "semesters" in data:
            for s_data in data["semesters"]:
                program.add_semester(Semester.from_dict(s_data))

        return program