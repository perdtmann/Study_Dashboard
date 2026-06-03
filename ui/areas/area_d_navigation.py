from typing import TYPE_CHECKING
import customtkinter as ctk

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from controller.app_controller import AppController


class AreaDNavigation(ctk.CTkFrame):
    """
    Repräsentiert den Navigations- und Aktionsbereich (Area D) des Dashboards.
    Erbt von ctk.CTkFrame. Platziert die funktionalen Schaltflächen und leitet
    Benutzerinteraktionen direkt an den steuernden Controller weiter.
    """

    def __init__(self, master: ctk.CTkFrame, controller: 'AppController', **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)

        # Referenz auf den Controller zur Event-Weiterleitung
        self._controller = controller

        # Layout-Konfiguration für den umschließenden Hauptbereich
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._button_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._button_frame.grid(column=0, row=0, sticky="nsew")

        # Gleichmäßige Gitter-Aufteilung für die Buttons (2 Spalten, 2 Zeilen)
        self._button_frame.grid_columnconfigure((0, 1), weight=1)
        self._button_frame.grid_rowconfigure((0, 1), weight=1)

        # --- ZEILE 0: Funktionale Masken-Buttons ---
        # Button für das Verwalten / Neuanlegen von Semestern
        self._button_new_semester = ctk.CTkButton(
            master=self._button_frame,
            text="Semester verwalten",
            command=self.on_new_semester
        )
        self._button_new_semester.grid(column=0, row=0, sticky="nsew", padx=10, pady=5)

        # Button für das Verwalten / Hinzufügen von Modulen
        self._button_edit_semester = ctk.CTkButton(
            master=self._button_frame,
            text="Modul verwalten",
            command=self.on_edit_module_click
        )
        self._button_edit_semester.grid(column=1, row=0, sticky="nsew", padx=10, pady=5)

        # --- ZEILE 1: Globale Anwendungseinstellungen ---
        # Erstreckt sich über columnspan=2 über die gesamte Fensterbreite
        self._button_general_settings = ctk.CTkButton(
            master=self._button_frame,
            text="Einstellungen",
            command=self.on_general_settings_click
        )
        self._button_general_settings.grid(column=0, row=1, columnspan=2, sticky="nsew", padx=10, pady=5)

    # --- Funktionale UI-Methoden (Ereignis-Weiterleitung) ---

    def on_new_semester(self) -> None:
        """Ruft die Semester-Konfigurationsmaske über den Controller auf."""
        self._controller.open_edit_semester_dialog()

    def on_edit_module_click(self) -> None:
        """Ruft die Modul-Eingabemaske über den Controller auf."""
        self._controller.open_add_module_dialog()

    def on_general_settings_click(self) -> None:
        """Ruft den Dialog für die globalen Stammdaten über den Controller auf."""
        self._controller.open_general_settings_dialog()