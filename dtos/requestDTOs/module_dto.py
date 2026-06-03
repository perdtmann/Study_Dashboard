from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleDTO:
    """
    Data Transfer Object (DTO) für die Eingabemaske eines Studienmoduls.
    Transportiert die eingegebenen Modulinformationen von der UI-Schicht zur Logikschicht.
    Durch frozen=True ist das Objekt nach der Erstellung schreibgeschützt.
    """
    module_code: str            # Eindeutiges Kürzel des Moduls (z. B. "DLBDSOOFPP01")
    module_name: str            # Vollständiger Name des Moduls (z. B. "Programmierung mit Python")
    ects: int                   # Anzahl der ECTS-Punkte für dieses Modul
    status: str                 # Aktueller Status des Moduls ("Geplant", "Begonnen", "Abgeschlossen")
    exam_grade: float      # Erzielte Note (wird im Service ignoriert, falls Status nicht "Abgeschlossen" ist)