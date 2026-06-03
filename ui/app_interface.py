from typing import TYPE_CHECKING
import customtkinter as ctk

from ui.areas.area_a_header import AreaAHeader
from ui.areas.area_b1_quant_goals import AreaB1QuantGoals
from ui.areas.area_b2_qual_goals import AreaB2QualGoals
from ui.areas.area_c_module_list import AreaCModuleList
from ui.areas.area_d_navigation import AreaDNavigation

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from controller.app_controller import AppController
    from dtos.responseDTOs.area_a_header_dto import AreaAHeaderDTO
    from dtos.responseDTOs.area_b1_quant_goals_dto import AreaB1QuantGoalsDTO
    from dtos.responseDTOs.area_b2_qual_goals_dto import AreaB2QualGoalsDTO
    from dtos.responseDTOs.area_c_module_list_dto import AreaCModuleListDTO


class AppInterface(ctk.CTk):
    """
    Das Hauptfenster der Anwendung.
    Erbt von ctk.CTk und baut das visuelle Grundgerüst des Dashboards auf.
    Verteilt die vom Controller gelieferten Daten an die spezifischen Unterbereiche (Area A bis Area D).
    """

    def __init__(self, controller: 'AppController') -> None:
        """Initialisiert das Hauptfenster und konfiguriert das Layout-Raster."""
        super().__init__()

        self.title("Study Dashboard")
        self.geometry("1100x700")

        self._controller = controller

        # Referenzen für die visuellen Unterbereiche (Sub-Views)
        self._area_a = None
        self._area_b1 = None
        self._area_b2 = None
        self._area_c = None
        self._area_d = None

        # Grid-System und Komponenten-Montage starten
        self._setup_grid()
        self._assemble_areas()

    def _setup_grid(self) -> None:
        """Konfiguriert das Spalten- und Zeilenraster des Hauptfensters."""
        # Zwei Spalten für Bereich B1 und B2 in der Mitte
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Zeilen-Definitionen für den vertikalen Aufbau
        self.grid_rowconfigure(0, weight=0, minsize=60)  # Zeile 1: Header (Area A)
        self.grid_rowconfigure(1, weight=0, minsize=250)  # Zeile 2: Ziele (Area B1 & B2)
        self.grid_rowconfigure(2, weight=1)  # Zeile 3: Modulliste (Area C, dehnbar)
        self.grid_rowconfigure(3, weight=0, minsize=120)  # Zeile 4: Navigation (Area D)

    def _assemble_areas(self) -> None:
        """Instanziiert die einzelnen Unterbereiche und platziert sie im Layout."""
        # Area A (Header) erstreckt sich über die gesamte Breite
        self._area_a = AreaAHeader(master=self)
        self._area_a.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Area B1 & B2 (quantitative und qualitative Ziele) werden Nebeneinander platziert
        self._area_b1 = AreaB1QuantGoals(master=self)
        self._area_b1.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self._area_b2 = AreaB2QualGoals(master=self)
        self._area_b2.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        # Area C (Modulliste) erstreckt sich über die gesamte Breite
        self._area_c = AreaCModuleList(master=self)
        self._area_c.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Area D (Navigation und Aktions-Buttons)
        self._area_d = AreaDNavigation(master=self, controller=self._controller)
        self._area_d.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

    def update_view(
            self,
            area_a_dto: 'AreaAHeaderDTO',
            area_b1_dto: 'AreaB1QuantGoalsDTO',
            area_b2_dto: 'AreaB2QualGoalsDTO',
            area_c_dto: 'AreaCModuleListDTO'
        ) -> None:
        """
        Zentraler Aktualisierungskanal der View.
        Nimmt die frischen DTOs vom Controller entgegen und reicht sie
        direkt zur grafischen Aktualisierung an die Sub-Views weiter.
        """
        self._area_a.update_data(area_a_dto)
        self._area_b1.update_data(area_b1_dto)
        self._area_b2.update_data(area_b2_dto)
        self._area_c.update_data(area_c_dto)