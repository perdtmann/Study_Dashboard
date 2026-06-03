"""
Haupt-Einstiegspunkt für das Study Dashboard.
Initialisiert das Protokollierungssystem, instanziiert die Kernkomponenten
der Anwendungsarchitektur gemäß dem Model-View-Controller-Muster
und startet die grafische Benutzeroberfläche.
"""

import logging
import os
from controller.app_controller import AppController
from persistence.json_handler import JSONHandler
from services.study_services import StudyService
from ui.app_interface import AppInterface


def setup_logging() -> None:
    """
    Initialisiert das globale Protokollierungssystem (Logging) der Anwendung.
    Sichert die Existenz des Datenverzeichnisses und konfiguriert die
    standardisierte Ausgabe in Datei und Konsole.
    """
    log_dir = "data"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            # Schreibt Protokolleinträge im Append-Modus mit UTF-8-Kodierung
            logging.FileHandler(log_file, encoding="utf-8"),
            # Spiegelt die Einträge parallel in den Standard-Ausgabestrom (Konsole)
            logging.StreamHandler()
        ]
    )


def main() -> None:
    """
    Zentrale Hauptfunktion der Anwendung.
    Orchestriert den Initialisierungs- und Verknüpfungsprozess der Systemschichten.
    """
    # 1. Protokollierungssystem initialisieren
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Anwendung 'Study Dashboard' wird initialisiert.")

    # 2. Persistenz- und Geschäftslogikschicht instanziieren (Model / Service)
    handler = JSONHandler()
    service = StudyService(handler)

    # 3. Steuerungsschicht (Controller) vorbereiten
    controller = AppController(view=None, service=service)

    # 4. Präsentationsschicht (View) instanziieren
    app = AppInterface(controller=controller)

    # View im Controller registrieren (Auflösung der zyklischen Abhängigkeit)
    controller._view = app

    # 5. Anwendungssystem starten und Hauptschleife betreten
    controller.startup()
    app.mainloop()


if __name__ == "__main__":
    main()