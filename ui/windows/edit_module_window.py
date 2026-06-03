from typing import TYPE_CHECKING, List, Any
import customtkinter as ctk

from dtos.requestDTOs.module_dto import ModuleDTO

# Schutz vor zyklischen Importen 
if TYPE_CHECKING:
    from controller.app_controller import AppController
    from dtos.requestDTOs.semester_dto import SemesterDTO


class EditModuleWindow(ctk.CTkToplevel):
    """
    Ein modales Pop-up-Fenster zum Anlegen oder Bearbeiten eines Studienmoduls.
    Ermöglicht die Eingabe von Code, Name, ECTS, Status und erzielter Note.
    """

    def __init__(self, master: Any, controller: 'AppController'):
        super().__init__(master)

        # Interne Controller-Referenz zuweisen
        self._controller = controller

        # Fenster-Grundkonfiguration
        self.title("Modul verwalten")
        self.geometry("420x380")
        self.resizable(False, False)

        # Fenster in den Vordergrund zwingen und Interaktionen mit dem Hauptfenster sperren
        self.grab_set()

        # Spalten-Konfiguration für ein sauberes Formular-Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # --- Formular-Eingabemaske ---

        # 1. Semester-Auswahl
        ctk.CTkLabel(self, text="Semester wählen:", anchor="w").grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self._option_semester_selection = ctk.CTkOptionMenu(self, values=["Bitte laden..."])
        self._option_semester_selection.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        # 2. Modul-Kürzel / Code
        ctk.CTkLabel(self, text="Modul-Code (z.B. DLB...):", anchor="w").grid(row=1, column=0, padx=15, pady=10,
                                                                              sticky="ew")
        self._entry_module_code = ctk.CTkEntry(self, placeholder_text="z.B. DLBDSOOFPP01")
        self._entry_module_code.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        # 3. Modul-Name
        ctk.CTkLabel(self, text="Modul-Name:", anchor="w").grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self._entry_module_name = ctk.CTkEntry(self, placeholder_text="z.B. Programmieren mit Python")
        self._entry_module_name.grid(row=2, column=1, padx=15, pady=10, sticky="ew")

        # 4. ECTS-Punkte
        ctk.CTkLabel(self, text="ECTS-Punkte:", anchor="w").grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self._entry_module_ects = ctk.CTkEntry(self, placeholder_text="z.B. 5")
        self._entry_module_ects.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        # 5. Modul-Status
        ctk.CTkLabel(self, text="Status:", anchor="w").grid(row=4, column=0, padx=15, pady=10, sticky="ew")
        self._entry_module_status = ctk.CTkOptionMenu(self, values=["Geplant", "Begonnen", "Abgeschlossen"])
        self._entry_module_status.grid(row=4, column=1, padx=15, pady=10, sticky="ew")

        # 6. Erzielte Modulnote
        ctk.CTkLabel(self, text="Note (0.0 falls offen):", anchor="w").grid(row=5, column=0, padx=15, pady=10,
                                                                            sticky="ew")
        self._entry_module_grade = ctk.CTkEntry(self, placeholder_text="z.B. 1.7")
        self._entry_module_grade.grid(row=5, column=1, padx=15, pady=10, sticky="ew")
        self._entry_module_grade.insert(0, "0.0")

        # --- Speichern-Schaltfläche ---
        self._button_save = ctk.CTkButton(
            self,
            text="Modul speichern",
            fg_color="mediumseagreen",
            hover_color="#26af5f",
            command=self.on_save_click
        )
        self._button_save.grid(row=6, column=1, padx=15, pady=20, sticky="e")

        # Event-Binding: Sobald das Feld für den Modul-Code verlassen wird, Daten vorbefüllen
        self._entry_module_code.bind("<FocusOut>", self.on_module_code_changed)

    # --- Funktionale UI-Methoden ---

    def set_data(self, semesters: List['SemesterDTO']) -> None:
        """Befüllt das Dropdown-Menü dynamisch mit den existierenden Semestern."""
        if not semesters:
            return

        semester_strings = [f"Semester {sem.semester_number}" for sem in semesters]
        self._option_semester_selection.configure(values=semester_strings)
        self._option_semester_selection.set(semester_strings[-1])

    def on_save_click(self) -> None:
        """
        Liest das Eingabeformular aus, validiert die numerischen Basistypen,
        verpackt die Daten in ein ModuleDTO und übergibt dieses an den Controller.
        """
        try:
            # Numerische Datentypen sicher parsen
            ects_val = int(self._entry_module_ects.get()) if self._entry_module_ects.get().isdigit() else 0

            try:
                grade_val = float(self._entry_module_grade.get().replace(",", "."))
            except ValueError:
                grade_val = 0.0

            # Ausgelesene Semester-Nummer aus dem Dropdown bestimmen
            selected_sem_str = self._option_semester_selection.get()
            try:
                semester_num = int(selected_sem_str.split(" ")[-1])
            except (ValueError, IndexError):
                semester_num = 1

            # Das Request-DTO instanziieren
            saved_dto = ModuleDTO(
                module_code=self._entry_module_code.get().strip(),
                module_name=self._entry_module_name.get().strip(),
                ects=ects_val,
                status=self._entry_module_status.get(),
                exam_grade=grade_val
            )

            # Übergabe an den Controller zur logischen Validierung und Speicherung
            if self._controller:
                # Wichtig für den Service: Wir teilen dem Controller mit, für welches Semester das Modul gilt
                self._controller._service._model.current_semester = semester_num

                # Übergabe des DTOs. Das Fenster schließt sich nur, wenn der Controller Erfolg (True) meldet
                success = self._controller.on_module_save_requested(saved_dto, window_master=self)
                if success:
                    self.destroy()

        except Exception as e:
            if self._controller:
                self._controller.show_error_message(f"Fehler beim Erstellen des Modul-DTOs: {str(e)}")

    def on_module_code_changed(self, event=None) -> None:
        """
        Prüft beim Verlassen des Code-Feldes, ob das Modul im ausgewählten Semester
        bereits existiert, und füllt die restlichen Formularfelder automatisch vor.
        """
        code = self._entry_module_code.get().strip()
        if not code or not self._controller:
            return

        selected_sem_str = self._option_semester_selection.get()
        try:
            semester_num = int(selected_sem_str.split(" ")[-1])
        except (ValueError, IndexError):
            semester_num = 1

        # Sicherer Durchgriff auf das Modell zur reinen UI-Vorbefüllung
        model = self._controller._service._model
        target_semester = next((s for s in model.semesters if s.number == semester_num), None)

        if target_semester:
            existing_module = next((m for m in target_semester.modules if m.module_code == code), None)

            if existing_module:
                self._entry_module_name.delete(0, ctk.END)
                self._entry_module_name.insert(0, existing_module.name)

                self._entry_module_ects.delete(0, ctk.END)
                self._entry_module_ects.insert(0, str(existing_module.ects))

                self._entry_module_status.set(existing_module.status.value)

                if existing_module.exam.grade is not None and existing_module.exam.grade > 0:
                    self._entry_module_grade.delete(0, ctk.END)
                    self._entry_module_grade.insert(0, str(existing_module.exam.grade))