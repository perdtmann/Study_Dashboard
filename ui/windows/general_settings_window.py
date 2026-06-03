import customtkinter as ctk
from typing import TYPE_CHECKING, List, Any

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from controller.app_controller import AppController
    from dtos.requestDTOs.study_settings_dto import StudySettingsDTO
    from dtos.requestDTOs.semester_dto import SemesterDTO


class GeneralSettingsWindow(ctk.CTkToplevel):
    """
    Ein modales Pop-up-Fenster für die allgemeinen Studieneinstellungen.
    Erlaubt dem Benutzer das Bearbeiten der globalen Stammdaten, der Abschlussart,
    des Wunsch-Zielnotenschnitts sowie des ECTS-Gesamtziels des gesamten Studiums.
    """

    def __init__(self, master: Any, controller: 'AppController'):
        super().__init__(master)

        # Zuweisung des Controllers zur Steuerung der Benutzerinteraktionen
        self._controller = controller

        # Physische Konfiguration des Einstellungsfensters
        self.title("Einstellungen")
        self.geometry("420x460")
        self.resizable(False, False)

        # Fenster in den Vordergrund zwingen und Interaktionen mit der Main-UI sperren
        self.grab_set()

        # Spaltenraster für eine saubere Ausrichtung der Eingabemaske konfigurieren
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # --- Eingabemaske für globale Einstellungen ---

        # 1. Benutzername
        ctk.CTkLabel(self, text="Benutzername:", anchor="w").grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self._entry_user_name = ctk.CTkEntry(self)
        self._entry_user_name.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # 2. Abschlussart (z. B. B.Sc. oder M.Sc.)
        ctk.CTkLabel(self, text="Abschlussart:", anchor="w").grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self._entry_degree_type = ctk.CTkEntry(self)
        self._entry_degree_type.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # 3. Studiengang
        ctk.CTkLabel(self, text="Studiengang:", anchor="w").grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self._entry_study_program = ctk.CTkEntry(self)
        self._entry_study_program.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        # 4. Angestrebter Wunsch-Zielnotenschnitt (Target GPA)
        ctk.CTkLabel(self, text="Ziel-Schnitt (GPA):", anchor="w").grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self._entry_target_gpa = ctk.CTkEntry(self)
        self._entry_target_gpa.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        # 5. ECTS-Gesamtziel des gesamten Studiengangs (z. B. 180 ECTS)
        ctk.CTkLabel(self, text="Gesamt-ECTS Studium:", anchor="w").grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self._entry_total_ects_goal = ctk.CTkEntry(self, placeholder_text="z.B. 180")
        self._entry_total_ects_goal.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        # 6. Aktuell ausgewähltes/aktives Fachsemester
        ctk.CTkLabel(self, text="Aktives Semester:", anchor="w").grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self._option_active_semester = ctk.CTkOptionMenu(self, values=["Semester 1"])
        self._option_active_semester.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        # --- Funktionale Aktions-Buttons ---
        # Speichern-Schaltfläche (Klassisch blau hinterlegt)
        self._button_save = ctk.CTkButton(self, text="Speichern", command=self.on_save_click, fg_color="#2b719e")
        self._button_save.grid(row=6, column=0, columnspan=2, padx=20, pady=15, sticky="ew")

        # Zurücksetzen-Schaltfläche (Warnend rot hinterlegt)
        self._button_factory_reset = ctk.CTkButton(
            self,
            text="Werkseinstellungen",
            command=self.on_factory_reset_click,
            fg_color="#9e2b2b"
        )
        self._button_factory_reset.grid(row=7, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

    def set_data(self, dto: 'StudySettingsDTO', semesters: List['SemesterDTO']) -> None:
        """Befüllt die Formularfelder mit den aktuellen Konfigurationswerten des Benutzers."""
        self._entry_user_name.insert(0, getattr(dto, 'user_name', 'Student'))
        self._entry_study_program.insert(0, getattr(dto, 'study_program_name', ''))
        self._entry_degree_type.insert(0, getattr(dto, 'degree_type', 'B.Sc.'))
        self._entry_target_gpa.insert(0, str(getattr(dto, 'target_gpa', 2.0)))

        # Holt das globale ECTS-Ziel über den Controller-Service aus dem aktuellen Datenmodell
        if self._controller and self._controller._service:
            model = self._controller._service._model
            self._entry_total_ects_goal.insert(0, str(model.total_ects_goal))

        # Dropdown für das aktive Fachsemester dynamisch mit den existierenden Semesterdaten füttern
        if semesters:
            semester_values = [f"Semester {sem.semester_number}" for sem in semesters]
            self._option_active_semester.configure(values=semester_values)
            current_active = getattr(dto, 'current_semester_index', 1)
            if f"Semester {current_active}" in semester_values:
                self._option_active_semester.set(f"Semester {current_active}")

    def on_save_click(self) -> None:
        """
        Liest alle Formularfelder aus, validiert die Datentypen und übergibt
        die bereinigten Daten zur persistenten Speicherung an den Controller.
        """
        user_name_val = self._entry_user_name.get().strip()
        program_name_val = self._entry_study_program.get().strip()
        degree_val = self._entry_degree_type.get().strip()

        # Numerische Formularwerte parsen
        try:
            target_gpa_val = float(self._entry_target_gpa.get().strip() or 2.0)
        except ValueError:
            target_gpa_val = 2.0

        selected_sem_str = self._option_active_semester.get()
        try:
            semester_num = int(selected_sem_str.split(" ")[-1])
        except (ValueError, IndexError):
            semester_num = 1

        try:
            total_ects_val = int(self._entry_total_ects_goal.get().strip() or 180)
        except ValueError:
            total_ects_val = 180

        # Datenübergabe an den Controller zur persistenten Sicherung in der JSON-Datenbank
        if self._controller:
            # Architektonische Ausnahme: Setzen des ECTS-Gesamtziels direkt im Modellzustand
            if self._controller._service and self._controller._service._model:
                self._controller._service._model.total_ects_goal = total_ects_val

            self._controller.on_settings_save_requested(
                user_name=user_name_val,
                program_name=program_name_val,
                degree=degree_val,
                target_gpa=target_gpa_val,
                active_semester=semester_num
            )
            self.destroy()

    def on_factory_reset_click(self) -> None:
        """Öffnet das vorgeschaltete Bestätigungs-Popup vor dem Zurücksetzen der Datenbank."""
        from ui.windows.confirmation_window import ConfirmationWindow
        msg = "Möchtest du wirklich alle Daten unwiderruflich löschen? Das Dashboard wird zurückgesetzt."
        ConfirmationWindow(master=self, controller=self._controller, message=msg, action_type="factory_reset")