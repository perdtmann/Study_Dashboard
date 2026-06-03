from typing import TYPE_CHECKING
import customtkinter as ctk

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from dtos.responseDTOs.area_b2_qual_goals_dto import AreaB2QualGoalsDTO


class AreaB2QualGoals(ctk.CTkFrame):
    """
    Repräsentiert den qualitativen Zielbereich (Area B2) des Dashboards.
    Visualisiert den Notendurchschnitt des aktuellen Semesters, den Gesamtschnitt
    des gesamten Studiums sowie eine dynamische Prognose-Ampel.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        # Raster-Konfiguration: Beide Spalten teilen sich den Platz gleichwertig
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Zeile 2 (Statusbalken) dehnt sich vertikal aus und drückt Zeile 3 nach unten
        self.grid_rowconfigure(2, weight=1)

        # --- 1. Header ---
        self._header_frame = ctk.CTkFrame(self, fg_color="lightgrey", corner_radius=0)
        self._header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self._title_label = ctk.CTkLabel(
            self._header_frame,
            text="Qualitative Ziele (Notendurchschnitt)",
            font=ctk.CTkFont(family="Arial", size=15),
            text_color="black",
        )
        self._title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # --- 2. Große aktuelle Notenanzeige (Semester) ---
        self._label_current_gpa = ctk.CTkLabel(
            self,
            text=">> --,--- <<",
            font=ctk.CTkFont(family="Arial", size=30, weight="bold")
        )
        self._label_current_gpa.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # --- 3. Statusbalken (Ampelsystem) ---
        self._status_bar = ctk.CTkFrame(self, height=25, fg_color="gray", corner_radius=5)
        self._status_bar.grid(row=2, column=0, columnspan=2, sticky="new", padx=25, pady=5)
        self._status_bar.grid_columnconfigure(0, weight=1)

        # --- 4. Text-Labels innerhalb des Statusbalkens ---
        self._label_feedback_message = ctk.CTkLabel(
            self._status_bar,
            text="...",
            font=ctk.CTkFont(family="Arial", size=15),
            text_color="black",
        )
        self._label_feedback_message.grid(row=0, column=0, sticky="ew", padx=25, pady=5)

        # Unsichtbares Hilfs-Label
        self._label_required_grade = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=0))

        # --- 5. Anzeige Zielnotendurchschnitt (Unten Links) ---
        self._label_target_gpa = ctk.CTkLabel(
            self,
            text="Ziel: Notendurchschnitt <= --",
            font=ctk.CTkFont(family="Arial", size=12),
            anchor="w"
        )
        self._label_target_gpa.grid(row=3, column=0, sticky="sw", padx=10, pady=(10, 10))

        # --- 6. Anzeige Gesamtschnitt des Studiums (Unten Rechts) ---
        self._label_total_gpa = ctk.CTkLabel(
            self,
            text="Gesamtschnitt Studium: --,---",
            font=ctk.CTkFont(family="Arial", size=12),
            anchor="e"
        )
        self._label_total_gpa.grid(row=3, column=1, sticky="se", padx=10, pady=(10, 10))

    def update_data(self, dto: 'AreaB2QualGoalsDTO') -> None:
        """
        Nimmt das qualitative Response-DTO entgegen, füllt alle Labels mit den
        berechneten Werten und steuert die Hintergrundfarbe des Ampelsystems.
        """
        if not dto:
            return

        # 1. Große Semester-Notenanzeige aktualisieren
        if dto.current_gpa > 0.0:
            self._label_current_gpa.configure(text=f">> {dto.current_gpa:.2f} <<")
        else:
            self._label_current_gpa.configure(text=">> --,--- <<")

        # 2. Zielnoten-Label befüllen
        self._label_target_gpa.configure(text=f"Ziel: Schnitt <= {dto.target_gpa:.1f}")

        # 3. Prognosetext im Statusbalken ausgeben
        self._label_feedback_message.configure(text=dto.correction_message)

        # 4. Gesamtschnitt des gesamten Studiums
        if dto.total_gpa > 0.0:
            self._label_total_gpa.configure(text=f"Gesamtschnitt Studium: {dto.total_gpa:.2f}")
        else:
            self._label_total_gpa.configure(text="Gesamtschnitt Studium: --,---")

        # 5. Dynamische Farbsteuerung des Ampelsystems (Statusbalken)
        if dto.performance_status == "GREEN":
            self._status_bar.configure(fg_color="mediumseagreen")
            self._label_feedback_message.configure(text_color="white")
        elif dto.performance_status == "YELLOW":
            self._status_bar.configure(fg_color="orange")
            self._label_feedback_message.configure(text_color="black")
        elif dto.performance_status == "RED":
            self._status_bar.configure(fg_color="indianred")
            self._label_feedback_message.configure(text_color="white")
        else:
            self._status_bar.configure(fg_color="gray")
            self._label_feedback_message.configure(text_color="black")