from typing import TYPE_CHECKING, Any
import customtkinter as ctk

# Schutz vor zyklischen Importen 
if TYPE_CHECKING:
    from controller.app_controller import AppController


class ConfirmationWindow(ctk.CTkToplevel):
    """
    Ein modales Dialogfenster zur Bestätigung kritischer Aktionen (z. B. Werkseinstellungen).
    Verhindert versehentliche Datenlöschungen durch den Nutzer.
    """

    def __init__(self, master: Any, controller: 'AppController', message: str, action_type: str):
        super().__init__(master)

        # Interne Attribute
        self._controller = controller
        self._action_type = action_type

        # Konfiguration des Pop-ups
        self.title("Bestätigung erforderlich")
        self.geometry("380x180")
        self.resizable(False, False)

        # Schiebt das Fenster in den Vordergrund und blockiert Interaktionen mit der Main-UI
        self.grab_set()

        # Raster-Konfiguration für eine saubere Schaltflächen-Anordnung
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Das Hinweistext-Label
        self._label_message = ctk.CTkLabel(self, text=message, wraplength=340, justify="center")
        self._label_message.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Abbrechen-Schaltfläche (Neutral grau hinterlegt)
        self._button_cancel = ctk.CTkButton(
            self,
            text="Abbrechen",
            command=self.on_cancel_click,
            fg_color="#7f8c8d"
        )
        self._button_cancel.grid(row=1, column=0, padx=20, pady=15, sticky="ew")

        # Bestätigen-Schaltfläche (Warnend rot hinterlegt)
        self._button_confirm = ctk.CTkButton(
            self,
            text="Ja, ausführen",
            command=self.on_confirm_click,
            fg_color="#c0392b"
        )
        self._button_confirm.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

    def on_confirm_click(self) -> None:
        """Führt die gewählte kritische Aktion aus und stößt den UI-Reset an."""
        if self._action_type == "factory_reset" and self._controller:
            try:
                from models.study_program import StudyProgram, DegreeType

                # Erstellt ein komplett leeres, frisches Studienprogramm-Modell
                blank_program = StudyProgram(
                    name="",
                    degree=DegreeType.BSC,
                    target_gpa=0.0,
                    total_ects_goal=0,
                    current_semester_index=1
                    )

                # Überschreibt den Zustand im Repository und im aktiven Laufzeit-Modell
                self._controller._service._repository.save(blank_program)
                self._controller._service._model = blank_program

                # Aktualisiert das gesamte Dashboard im Hintergrund
                self._controller.refresh_ui()

            except Exception as e:
                self._controller.show_error_message(f"Fehler beim Reset: {str(e)}")

        # Schließt erst das übergeordnete Einstellungsfenster und anschließend sich selbst
        if self.master and hasattr(self.master, "destroy"):
            self.master.destroy()
        self.destroy()

    def on_cancel_click(self) -> None:
        """Schließt ausschließlich das Bestätigungsfenster und lässt Einstellungen offen."""
        self.destroy()