from typing import TYPE_CHECKING
import customtkinter as ctk

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from dtos.responseDTOs.area_b1_quant_goals_dto import AreaB1QuantGoalsDTO


class AreaB1QuantGoals(ctk.CTkFrame):
    """
    Repräsentiert den quantitativen Zielbereich (Area B1) des Dashboards.
    Visualisiert den ECTS-Fortschritt des aktuellen Semesters über ein dynamisches
    Kachelsystem und zeigt verbleibende Fristen sowie den Gesamtfortschritt an.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        # Spalten-Konfiguration: Spalte 0 dehnt sich aus, Spalte 1 bleibt rechtsbündig
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # --- 1. Header ---
        self._header_frame = ctk.CTkFrame(self, fg_color="#E0E0E0", corner_radius=0)
        self._header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self._title_label = ctk.CTkLabel(
            self._header_frame,
            text="Quantitative Ziele (ECTS)",
            font=ctk.CTkFont(family="Arial", size=15),
            text_color="black"
        )
        self._title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # --- 2. Große ECTS-Übersicht (Semester) ---
        self._label_ects = ctk.CTkLabel(
            self,
            text="-- / -- ECTS",
            font=ctk.CTkFont(family="Arial", size=30, weight="bold"),
        )
        self._label_ects.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # --- 3. Bereich für die dynamischen Modul-Kacheln ---
        self._tile_area = ctk.CTkFrame(self, fg_color="transparent")
        self._tile_area.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # --- 4. ECTS Prozent-Übersicht ---
        self._label_progress_percent = ctk.CTkLabel(
            self,
            text="-- % abgeschlossen",
            font=ctk.CTkFont(family="Arial", size=15),
        )
        self._label_progress_percent.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="n")

        # --- 5. Zeit bis Semesterende (Unten Links) ---
        self._label_deadline_info = ctk.CTkLabel(
            self,
            text="Zeit bis Semesterende: -- Tage",
            font=ctk.CTkFont(family="Arial", size=12),
            anchor="w"
        )
        self._label_deadline_info.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 5))

        # --- 6. Gesamte ECTS des Studiums (Unten Rechts) ---
        self._label_total_progress = ctk.CTkLabel(
            self,
            text="Gesamt: -- ECTS",
            font=ctk.CTkFont(family="Arial", size=12),
            anchor="e"
        )
        self._label_total_progress.grid(row=4, column=1, sticky="e", padx=10, pady=(0, 5))

    def update_data(self, dto: 'AreaB1QuantGoalsDTO') -> None:
        """
        Nimmt das quantitative Response-DTO entgegen, aktualisiert alle Textfelder
        und zeichnet das visuelle ECTS-Kachelsystem flexibel neu.
        """
        if not dto:
            return

        # 1. Daten aus dem DTO extrahieren
        ects_absolviert = dto.current_semester_ects
        ects_gesamt = dto.semester_target_ects
        ects_prozent = dto.total_progress_percent
        days_left = dto.days_until_semester_end
        total_study_ects = dto.total_study_ects

        # 2. Text-Labels mit den Werten befüllen
        self._label_ects.configure(text=f"{ects_absolviert} / {ects_gesamt} ECTS")
        self._label_progress_percent.configure(text=f"{ects_prozent} % abgeschlossen")
        self._label_deadline_info.configure(text=f"Zeit bis Semesterende: {days_left} Tage")
        self._label_total_progress.configure(text=f"Gesamt: {total_study_ects} ECTS")

        # 3. Dynamische Kacheln neu generieren (1 Kachel repräsentiert 5 ECTS)
        for widget in self._tile_area.winfo_children():
            widget.destroy()

        kacheln_gesamt = max(1, ects_gesamt // 5)
        kacheln_abgeschlossen = ects_absolviert // 5

        for i in range(kacheln_gesamt):
            farbe = "mediumseagreen" if i < kacheln_abgeschlossen else "indianred"

            kachel = ctk.CTkFrame(
                self._tile_area,
                width=50,
                height=25,
                fg_color=farbe,
                corner_radius=4
            )
            kachel.grid(row=0, column=i, padx=5, pady=5)
            kachel.grid_propagate(False)