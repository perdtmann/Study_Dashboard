import logging
from datetime import date
from models.module import Module

logger = logging.getLogger(__name__)


class Semester:
    """
    Repräsentiert ein Studiensemester.
    Verwaltet den Zeitraum, das ECTS-Ziel und die zugeordneten Module.
    """

    def __init__(self, number: int, target_ects: int, start_date: date, end_date: date):
        self.number = number
        self.target_ects = target_ects
        self.start_date = start_date
        self.end_date = end_date

        # Liste zur Speicherung der zugehörigen Module
        self.modules = []

    def calculate_current_ects(self) -> int:
        """Berechnet die Summe aller bereits erfolgreich erarbeiteten ECTS-Punkte."""
        total = 0
        for module in self.modules:
            total += module.get_effective_ects()
        return total

    def get_days_left(self) -> int:
        """Berechnet die Gesamtdauer des Semesters in Tagen basierend auf Start- und Enddatum."""
        return (self.end_date - self.start_date).days

    def add_module(self, module: Module) -> None:
        """Fügt ein neues Modul zur Liste des Semesters hinzu, sofern es vom Typ Module ist."""
        if isinstance(module, Module):
            self.modules.append(module)
            logger.info(f"Modul '{module.name}' wurde zu Semester {self.number} hinzugefügt.")
        else:
            logger.error("Fehler: Es können nur Objekte vom Typ 'Module' hinzugefügt werden.")

    def get_semester_gpa(self) -> float:
        """Berechnet den aktuellen Notendurchschnitt (GPA) für dieses Semester."""
        total_grades = 0.0
        count = 0

        for module in self.modules:
            # Nur abgeschlossene Module fließen in die Note ein
            if module.is_finished():
                total_grades += module.exam.grade
                count += 1

        if count == 0:
            return 0.0

        return total_grades / count

    def to_dict(self) -> dict:
        """Konvertiert das Semester-Objekt mitsamt Modulen in ein Dictionary für die JSON."""
        return {
            "number": self.number,
            "target_ects": self.target_ects,
            "start_date": self.start_date.isoformat(),  # Datum formatiert als ISO-String YYYY-MM-DD
            "end_date": self.end_date.isoformat(),
            "modules": [m.to_dict() for m in self.modules]  # Ruft to_dict() der Module auf
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Semester':
        """Erstellt ein Semester-Objekt inklusive aller enthaltenen Module aus einem Dictionary."""
        sem = cls(
            number=data["number"],
            target_ects=data["target_ects"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"])
        )

        # Module rekursiv wieder aufbauen und hinzufügen
        for m_data in data["modules"]:
            sem.add_module(Module.from_dict(m_data))

        return sem