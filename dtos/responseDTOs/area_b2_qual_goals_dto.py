from dataclasses import dataclass


@dataclass
class AreaB2QualGoalsDTO:
    """
    Datencontainer (DTO) für den qualitativen Zielbereich (Area B2).
    Überträgt die berechneten Notenschnitte und Prognosen transportbereit vom Service zum UI.
    """
    current_gpa: float        # Der Notendurchschnitt des aktuell ausgewählten Semesters
    target_gpa: float         # Der global gesetzte Wunsch-Ziel-Notenschnitt
    total_gpa: float          # Der Gesamt-Notendurchschnitt über das gesamte Studium
    correction_message: str        # Die generierte Prognose-Nachricht (z. B. "Nächste Note benötigt: ...")
    performance_status: str        # Der Status für das Ampelsystem ("GREEN", "YELLOW", "RED", "NEUTRAL")