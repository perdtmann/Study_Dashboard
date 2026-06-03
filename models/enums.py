from enum import Enum


class DegreeType(str, Enum):
    """
    Repräsentiert die akademischen Abschlussarten für das Studienprogramm.
    Wird genutzt, um den angestrebten Abschluss im Dashboard anzuzeigen.
    """
    BSC = "B.Sc."
    MSC = "M.Sc."


class ModulStatus(str, Enum):
    """
    Definiert die verschiedenen Zustände, die ein Modul annehmen kann.
    Steuert die Logik: Nur Module im Status 'Abgeschlossen' (COMPLETED)
    werden für die Berechnung des Notenschnitts berücksichtigt.
    """
    PLANNED = "Geplant"
    IN_PROGRESS = "Begonnen"
    COMPLETED = "Abgeschlossen"