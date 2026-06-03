import json
import os
import logging
from typing import TYPE_CHECKING
from persistence.i_persistence import IPersistence

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from models.study_program import StudyProgram

# Logger für diese Datei initialisieren (schreibt in data/app.log)
logger = logging.getLogger(__name__)


class JSONHandler(IPersistence):
    """
    Konkrete Implementierung der Persistence-Schnittstelle.
    Speichert und lädt die Daten des Studienprogramms in einer lokalen JSON-Datei.
    """

    def __init__(self, file_path: str = "data/data.json"):
        self._file_path = file_path

        # Erstellt den Datenordner automatisch, falls er im System noch fehlt
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)

    def save(self, program: 'StudyProgram') -> None:
        """
        Konvertiert das übergebene Studienprogramm in ein Dictionary
        und schreibt es als formatierten Text in die JSON-Datei.
        """
        data = program.to_dict()
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info("Daten erfolgreich in JSON-Datei gesichert.")

    def load(self) -> 'StudyProgram':
        """
        Lädt die JSON-Datei und baut das Studienprogramm-Objekt wieder auf.
        Gibt ein leeres Standard-Studienprogramm zurück, falls die Datei fehlt oder fehlerhaft ist.
        """
        from models.study_program import StudyProgram
        from models.enums import DegreeType

        # Fallback: Wenn die Datei nicht existiert oder komplett leer ist
        if not os.path.exists(self._file_path) or os.path.getsize(self._file_path) == 0:
            logger.info("Keine bestehende Datendatei gefunden. Erstelle neues Studienprogramm.")
            return StudyProgram(
                name="",
                degree=DegreeType.BSC,
                target_gpa=0.0,
                total_ects_goal=0,
                current_semester_index=1,
                user_name="Student"
            )

        try:
            # Versuche, die Datei regulär einzulesen
            with open(self._file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return StudyProgram.from_dict(data)
        except Exception as e:
            # Falls die Datei beschädigt ist, wird der Fehler abgefangen und neu gestartet
            logger.warning(f"Fehler beim Laden der JSON-Datei: {str(e)}. Erstelle leeres Programm.")

            return StudyProgram(
                name="",
                degree=DegreeType.BSC,
                target_gpa=0.0,
                total_ects_goal=0,
                current_semester_index=1,
                user_name="Student"
            )