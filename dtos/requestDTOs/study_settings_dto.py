from dataclasses import dataclass


@dataclass(frozen=True)
class StudySettingsDTO:
    """
    Data Transfer Object (DTO) für die allgemeinen Studieneinstellungen.
    Kapselt die nutzerspezifischen Basisdaten und übergeordneten Studienziele.
    Durch frozen=True ist dieses Objekt nach der Erstellung unveränderlich (Read-Only).
    """
    name: str                   # Der vollständige Name des Studierenden
    degree: str                 # Der angestrebte Abschluss (z. B. "B.Sc." oder "M.Sc.")
    target_gpa: float      # Die individuell gesetzte Wunsch-Abschlussnote
    total_ects_goal: int        # Die für den gesamten Studiengang zu erreichenden Gesamt-ECTS (z. B. 180)