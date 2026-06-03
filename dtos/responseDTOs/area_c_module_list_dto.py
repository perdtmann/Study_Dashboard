from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModuleItemDTO:
    """
    Repräsentiert die Daten eines einzelnen Moduls für die Anzeige in der UI-Liste.
    Dient als kompakter Datencontainer für Namen, ECTS, Status und die Note.
    """
    name: str
    ects: int
    status: str
    grade: Optional[float] = None
    module_code: Optional[str] = None


@dataclass
class AreaCModuleListDTO:
    """
    Datencontainer (DTO) für die gesamte Modulübersicht (Area C).
    Hält die Liste aller Semestergruppen, damit das Dashboard die Module
    strukturiert nach Semestern sortiert ausgeben kann.
    """
    # field(default_factory=list) verhindert Python-Fehler bei leeren Listenstarts
    semester_groups: List[dict] = field(default_factory=list)