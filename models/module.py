import logging
from models.enums import ModulStatus
from models.exam_achievement import ExamAchievement

logger = logging.getLogger(__name__)


class Module:
    """
    Repräsentiert ein einzelnes Modul im Studium.
    Verwaltet die Modulinformationen, den aktuellen Status und die zugehörige Prüfung.
    """

    def __init__(self, module_code: str, name: str, ects: int, status: ModulStatus):
        # Basisdaten des Moduls
        self.module_code = module_code
        self.name = name
        self.ects = ects
        self.status = status

        # Jedes Modul besitzt automatisch eine Prüfungsleistung
        self.exam = ExamAchievement()

    def is_finished(self) -> bool:
        """Prüft, ob das Modul erfolgreich beendet und bestanden wurde."""
        return self.status == ModulStatus.COMPLETED and self.exam.is_passed

    def set_completion(self, grade: float) -> None:
        """
        Schließt das Modul mit einer Note ab.
        Leitet die Note an die Prüfung weiter und setzt den Status auf COMPLETED.
        """
        # Reicht die Note an ExamAchievement weiter (wirft bei Fehlern einen ValueError)
        self.exam.is_successful(grade)
        self.status = ModulStatus.COMPLETED
        logger.info(f"Modul '{self.name}' wurde mit der Note {grade} abgeschlossen.")

    def get_effective_ects(self) -> int:
        """Gibt die ECTS-Punkte zurück, wenn die Prüfung bestanden wurde, sonst 0."""
        if self.exam.is_passed:
            return self.ects
        return 0

    def to_dict(self) -> dict:
        """Konvertiert das Modul-Objekt in ein Dictionary für die JSON-Speicherung."""
        return {
            "module_code": self.module_code,
            "module_name": self.name,
            "ects": self.ects,
            "status": self.status.value,  # Speichert den reinen Textwert des Enums
            "exam_grade": self.exam.grade  # Holt die Note aus dem ExamAchievement
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Module':
        """Erstellt ein Modul-Objekt aus einem JSON-Dictionary."""
        module = cls(
            module_code=data["module_code"],
            name=data["module_name"],
            ects=data["ects"],
            status=ModulStatus(data["status"])
        )

        # Falls bereits eine Note existiert, wird das Modul direkt abgeschlossen
        if data["exam_grade"] is not None:
            module.set_completion(data["exam_grade"])

        return module