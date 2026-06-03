from datetime import date, datetime
from typing import TYPE_CHECKING, Any
import customtkinter as ctk

from dtos.requestDTOs.semester_dto import SemesterDTO

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from controller.app_controller import AppController


class EditSemesterWindow(ctk.CTkToplevel):
    """
    Ein modales Pop-up-Fenster (Top-Level) zum Bearbeiten der Semester-Stammdaten
    sowie zum Festlegen oder Löschen von Zeitzielen (Target ECTS).
    """

    def __init__(self, master: Any, controller: 'AppController'):
        super().__init__(master)

        # Interne Controller-Referenz zuweisen
        self._controller = controller

        # Physische Fenster-Grundkonfiguration
        self.title("Semester verwalten")
        self.geometry("400x320")
        self.resizable(False, False)

        # Fenster in den Vordergrund zwingen und Interaktionen mit dem Hauptfenster sperren
        self.grab_set()

        # Spalten-Konfiguration für ein sauberes Formular-Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # --- Formular-Eingabemaske ---

        # 1. Semester-Nummer
        lbl_sem_num = ctk.CTkLabel(self, text="Semester-Nummer:", anchor="w")
        lbl_sem_num.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self._entry_semester_number = ctk.CTkEntry(self)
        self._entry_semester_number.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        # 2. Ziel-ECTS
        lbl_target_ects = ctk.CTkLabel(self, text="Ziel-ECTS:", anchor="w")
        lbl_target_ects.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        self._entry_target_ects = ctk.CTkEntry(self)
        self._entry_target_ects.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        # 3. Startdatum
        lbl_start_date = ctk.CTkLabel(self, text="Startdatum (TT.MM.JJJJ):", anchor="w")
        lbl_start_date.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self._entry_start_date = ctk.CTkEntry(self)
        self._entry_start_date.grid(row=2, column=1, padx=15, pady=10, sticky="ew")

        # 4. Enddatum
        lbl_end_date = ctk.CTkLabel(self, text="Enddatum (TT.MM.JJJJ):", anchor="w")
        lbl_end_date.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self._entry_end_date = ctk.CTkEntry(self)
        self._entry_end_date.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        # --- Aktions-Schaltflächen ---
        # Löschen-Button
        self._button_delete_semester = ctk.CTkButton(
            self,
            text="Löschen",
            fg_color="indianred",
            hover_color="#b33939",
            command=self.on_delete_click
        )
        self._button_delete_semester.grid(row=4, column=0, padx=15, pady=20, sticky="w")

        # Speichern-Button
        self._button_save = ctk.CTkButton(
            self,
            text="Speichern",
            fg_color="mediumseagreen",
            hover_color="#26af5f",
            command=self.on_save_click
        )
        self._button_save.grid(row=4, column=1, padx=15, pady=20, sticky="e")

    # --- Funktionale UI-Methoden ---

    def set_data(self, dto: SemesterDTO) -> None:
        """Befüllt die Formularfelder mit den Werten des übergebenen Request-DTOs."""
        if not dto:
            return

        self._entry_semester_number.delete(0, ctk.END)
        self._entry_semester_number.insert(0, str(dto.semester_number))

        self._entry_target_ects.delete(0, ctk.END)
        self._entry_target_ects.insert(0, str(dto.target_ects))

        # Datumsobjekte für die Nutzersichtbarkeit in deutsches Textformat formatieren
        self._entry_start_date.delete(0, ctk.END)
        self._entry_start_date.insert(0, dto.start_date.strftime("%d.%m.%Y"))

        self._entry_end_date.delete(0, ctk.END)
        self._entry_end_date.insert(0, dto.end_date.strftime("%d.%m.%Y"))

    def on_save_click(self) -> None:
        """
        Liest das Formular aus, konvertiert die deutschen Datumstexte in Python date-Objekte,
        verpackt alles in ein SemesterDTO und übergibt es an den Controller.
        """
        try:
            # Datumsformate einlesen und validieren
            start_date_obj = datetime.strptime(self._entry_start_date.get().strip(), "%d.%m.%Y").date()
            end_date_obj = datetime.strptime(self._entry_end_date.get().strip(), "%d.%m.%Y").date()

            # Semester-Nummer und ECTS parsen
            sem_num = int(self._entry_semester_number.get().strip())
            target_ects = int(self._entry_target_ects.get().strip())

            saved_dto = SemesterDTO(
                semester_number=sem_num,
                target_ects=target_ects,
                start_date=start_date_obj,
                end_date=end_date_obj
            )

            if self._controller:
                self._controller.on_semester_settings_save_requested(saved_dto)
                self.destroy()

        except ValueError:
            if self._controller:
                self._controller.show_error_message(
                    "Ungültige Eingabe! Bitte stelle sicher, dass ECTS eine Zahl ist "
                    "und die Daten dem Format TT.MM.JJJJ entsprechen.",
                    master=self
                )

    def on_delete_click(self) -> None:
        """Nutzt die bestehende Speicher-Schnittstelle mit einem Signalwert (-1), um das Semester zu löschen."""
        try:
            sem_num = int(self._entry_semester_number.get().strip())

            # Anfangs reguläres DTO, aber mit Löschsignal (-1 ECTS) für das Modell
            delete_signal_dto = SemesterDTO(
                semester_number=sem_num,
                target_ects=-1,
                start_date=date.today(),
                end_date=date.today()
            )

            if self._controller:
                self._controller.on_semester_settings_save_requested(delete_signal_dto)
                self.destroy()
        except ValueError:
            self.destroy()