import customtkinter as ctk
from typing import Any


class ErrorWindow(ctk.CTkToplevel):
    """
    Ein modales Pop-up-Fenster zur standardisierten Anzeige von Laufzeitfehlern.
    Zwingt sich aktiv in den Vordergrund des Betriebssystems und sperrt die
    Interaktion mit den darunterliegenden Masken, bis der Fehler bestätigt wurde.
    """

    def __init__(self, master: Any, message: str = "", title: str = "Fehler", error_message: str = None):
        """Initialisiert das Fehlerfenster, setzt Fokus-Prioritäten und baut das Layout auf."""
        super().__init__(master)

        # Brücke zwischen Controller-Aufruf (error_message)
        actual_message = error_message if error_message is not None else message

        self.title(title)
        self.geometry("380x160")
        self.resizable(False, False)

        # Fenster im Betriebssystem ganz nach oben legen und sperren
        self.attributes("-topmost", True)
        self.focus_force()
        self.grab_set()

        # Raster-Konfiguration für Icon (Spalte 0) und Textmeldung (Spalte 1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Das Warn-Icon als separates Element
        self._icon_label = ctk.CTkLabel(
            self,
            text="⚠",
            text_color="#e74c3c",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold")
        )
        self._icon_label.grid(row=0, column=0, padx=(20, 10), pady=20)

        # Das Haupt-Label für den Fehlermeldungstext
        self._label_error_message = ctk.CTkLabel(
            self,
            text=actual_message,
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold")
        )
        self._label_error_message.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="w")

        # Bestätigungsschaltfläche
        self._button_ok = ctk.CTkButton(
            self,
            text="Ok",
            command=self.on_ok_click,
            fg_color="#2c3e50",
            hover_color="#34495e"
        )
        self._button_ok.grid(row=1, column=0, columnspan=2, padx=40, pady=15, sticky="ew")

        # Erzwingt das sofortige Rendern aller Widgets vor dem nächsten Event-Zyklus
        self.update_idletasks()

    def on_ok_click(self) -> None:
        """Schließt das Fehlerfenster und gibt den UI-Fokus wieder frei."""
        self.destroy()