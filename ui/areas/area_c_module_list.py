from typing import TYPE_CHECKING
import customtkinter as ctk

# Schutz vor zyklischen Importen für die IDE
if TYPE_CHECKING:
    from dtos.responseDTOs.area_c_module_list_dto import AreaCModuleListDTO


class AreaCModuleList(ctk.CTkFrame):
    """
    Repräsentiert die Modulübersicht (Area C) des Dashboards.
    Besteht aus einer fixierten Kopfzeile für die Spaltenbeschriftungen
    und einem darunter liegenden scrollbaren Bereich, in dem die Module
    nach Semestern gruppiert dynamisch als Kacheln gerendert werden.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)

        # 1. Fixierte Kopfzeile oben verankern
        self._setup_header()

        # 2. Scrollbarer Container für die dynamischen Modulkarten
        self._scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def _setup_header(self) -> None:
        """Erstellt die statische Kopfzeile für die Spaltenbeschriftungen."""
        header_card = ctk.CTkFrame(master=self, fg_color="transparent", height=30)
        header_card.pack(padx=10, pady=(10, 0), fill="x")
        header_card.pack_propagate(False)

        # Linker Bereich: Spaltentitel für Code und Name
        label_name = ctk.CTkLabel(
            header_card,
            text="CODE & MODULNAME",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#777777"
        )
        label_name.pack(side="left", padx=20)

        # Rechter Bereich: Werte (von rechts nach links gepackt für bündiges Layout)
        label_status = ctk.CTkLabel(
            header_card,
            text="STATUS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#777777"
        )
        label_status.pack(side="right", padx=30)

        label_note = ctk.CTkLabel(
            header_card,
            text="NOTE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#777777"
        )
        label_note.pack(side="right", padx=45)

        label_ects = ctk.CTkLabel(
            header_card,
            text="ECTS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#777777"
        )
        label_ects.pack(side="right", padx=25)

        # Horizontale Trennlinie unter dem Header
        trennlinie = ctk.CTkFrame(master=self, height=2, fg_color="#444444")
        trennlinie.pack(padx=15, pady=(5, 5), fill="x")

    def update_data(self, dto: 'AreaCModuleListDTO') -> None:
        """
        Nimmt das hierarchische Modullisten-Response-DTO entgegen,
        leert den scrollbaren Bereich und zeichnet alle enthaltenen Module
        strukturiert nach Semestergruppen sortiert neu.
        """
        if not dto:
            return

        # Bestehende UI-Elemente im Scrollbereich löschen, um Duplikate zu verhindern
        for widget in self._scrollable_frame.winfo_children():
            widget.destroy()

        # Iteration durch die vom Service bereitgestellten Semestergruppen
        for group in dto.semester_groups:
            sem_num = group.get("semester_number", 0)
            modules = group.get("modules", [])

            if not modules:
                continue

            # Visuelle Semester-Überschrift in den Scroll-Bereich einfügen
            sem_header = ctk.CTkLabel(
                self._scrollable_frame,
                text=f"--- {sem_num}. Semester ---",
                font=ctk.CTkFont(size=12, weight="bold", slant="italic"),
                text_color="gray"
            )
            sem_header.pack(padx=15, pady=(10, 5), anchor="w")

            # Einzelne Modulkarten innerhalb der Gruppe rendern
            for modul in modules:
                code = modul.get("module_code", "M00")
                name = modul.get("name", "Unbekanntes Modul")
                ects = modul.get("ects", 0)
                status_wert = modul.get("status", "Geplant")
                note_wert = modul.get("grade", None)

                # Basis-Kachel für das Modul zeilenweise anlegen
                karte = ctk.CTkFrame(
                    master=self._scrollable_frame,
                    fg_color="#2B2B2B",
                    corner_radius=8,
                    height=45
                    )
                karte.pack(padx=10, pady=3, fill="x")
                karte.pack_propagate(False)

                # Spalten-Inhalt links: Code und Bezeichnung
                info_text = f"[{code}]  {name}"
                label_info = ctk.CTkLabel(
                    karte,
                    text=info_text,
                    font=ctk.CTkFont(size=13, weight="bold")
                )
                label_info.pack(side="left", padx=20)

                # Spalten-Inhalt rechts (Reihenfolge beachten):
                # 1. Status-Badge mit dynamischer Hintergrundfarbe
                if status_wert == "Abgeschlossen":
                    status_color = "mediumseagreen"
                    text_color = "white"
                elif status_wert == "Begonnen":
                    status_color = "orange"
                    text_color = "black"
                else:
                    status_color = "#444444"
                    text_color = "#AAAAAA"

                badge_frame = ctk.CTkFrame(
                    karte,
                    fg_color=status_color,
                    corner_radius=4,
                    width=105,
                    height=22
                )
                badge_frame.pack(side="right", padx=15)
                badge_frame.pack_propagate(False)

                lbl_status = ctk.CTkLabel(
                    badge_frame,
                    text=status_wert,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=text_color
                )
                lbl_status.pack(expand=True, fill="both")

                # 2. Modulnote (wird nur formatiert ausgegeben, wenn eine Note existiert)
                if note_wert is not None:
                    note_str = f"{note_wert:.1f}"
                    note_color = "indianred" if note_wert > 4.0 else "white"
                else:
                    note_str = "--"
                    note_color = "#777777"

                lbl_note = ctk.CTkLabel(
                    karte,
                    text=note_str,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=note_color
                )
                lbl_note.pack(side="right", padx=55)

                # 3. Credit-Points (ECTS)
                lbl_ects = ctk.CTkLabel(
                    karte,
                    text=f"{ects} CP",
                    font=ctk.CTkFont(size=13),
                    text_color="#CCCCCC"
                )
                lbl_ects.pack(side="right", padx=25)