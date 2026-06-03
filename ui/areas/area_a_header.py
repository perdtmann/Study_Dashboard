from typing import TYPE_CHECKING
import customtkinter as ctk

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from dtos.responseDTOs.area_a_header_dto import AreaAHeaderDTO


class AreaAHeader(ctk.CTkFrame):
    """
    Repräsentiert den oberen Header-Bereich (Area A) des Dashboards.
    Erbt direkt von ctk.CTkFrame. Zeigt links ein skalierendes
    Unicode-Icon mit dem App-Titel und rechts die dynamischen Benutzerdaten.
    """

    def __init__(self, master: ctk.CTkFrame):
        # Initialisiert das Frame direkt als übergeordnetes Widget
        super().__init__(master, fg_color="transparent")

        # Raster-Konfiguration für die zwei Hauptbereiche (links und rechts)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- LINKE SEITE: Icon & App-Titel ---
        self._left_container = ctk.CTkFrame(self, fg_color="transparent")
        self._left_container.grid(row=0, column=0, sticky="w")

        # Ein systemunabhängiges Unicode-Icon als Text-Label
        self._icon_label = ctk.CTkLabel(
            self._left_container,
            text="🎓",
            font=ctk.CTkFont(size=26)
        )
        self._icon_label.pack(side="left", padx=(0, 10))

        # Titel-Label der Anwendung
        self._app_name = ctk.CTkLabel(
            self._left_container,
            text="Study Dashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self._app_name.pack(side="left")

        # --- RECHTE SEITE: Studentendaten ---
        self._right_container = ctk.CTkFrame(self, fg_color="transparent")
        self._right_container.grid(row=0, column=1, sticky="e")

        # Label für den Benutzernamen
        self._student_name = ctk.CTkLabel(
            self._right_container,
            text="Name: -",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="e"
        )
        self._student_name.pack(anchor="e")

        # Label für den Studiengang und das aktuelle Fachsemester
        self._student_course = ctk.CTkLabel(
            self._right_container,
            text="Studiengang: - | Fachsemester: -",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="e"
        )
        self._student_course.pack(anchor="e")

    def update_data(self, dto: 'AreaAHeaderDTO') -> None:
        """
        Nimmt das eintreffende Response-DTO entgegen und aktualisiert
        die Oberflächenelemente des Headers mit den echten Modelldaten.
        """
        self._student_name.configure(text=f"Name: {dto.user_name}")
        self._student_course.configure(
            text=f"Studiengang: {dto.study_program_name} | Fachsemester: {dto.current_semester_count}"
        )