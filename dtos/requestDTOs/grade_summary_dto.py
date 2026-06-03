from dataclasses import dataclass


@dataclass(frozen=True)
class GradeSummaryDTO:
    """
    Data Transfer Object für die zusammengefassten Notenstatistiken.
    Kapselt die berechneten Durchschnittswerte und Prognosen für die
    qualitative Zielüberwachung im Dashboard (Bereich B2).
    Durch frozen=True ist dieses Objekt nach der Erstellung unveränderlich (Read-Only).
    """
    current_semester_gpa: float  # Der Notendurchschnitt des aktuell ausgewählten Semesters
    total_gpa: float             # Der aktuelle Gesamtdurchschnitt über das gesamte Studium
    target_gpa: float            # Die vom Nutzer definierte Wunsch-Zielnote
    required_prognosis: float    # Die rechnerisch notwendige Durchschnittsnote für künftige Module