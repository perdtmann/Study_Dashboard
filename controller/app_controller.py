import logging
from typing import TYPE_CHECKING

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from services.study_services import StudyService
    from dtos.requestDTOs.module_dto import ModuleDTO
    from dtos.requestDTOs.semester_dto import SemesterDTO


class AppController:
    """
    Der zentrale Controller der Anwendung.
    Steuert die Kommunikation zwischen der UI-Schicht und der Logikschicht (Service).
    Reicht Benutzereingaben weiter und stößt die Aktualisierung der Bildschirminhalte an.
    """

    def __init__(self, view, service: 'StudyService'):
        """Initialisiert den Controller mit der zuständigen View und dem Service."""
        self._view = view
        self._service = service
        self._logger = logging.getLogger(__name__)

    def startup(self) -> None:
        """Startet den Controller und initialisiert die allererste UI-Aktualisierung beim App-Start."""
        self._logger.info("AppController erfolgreich gestartet.")
        self.refresh_ui()

    def refresh_ui(self) -> None:
        """Holt die aktuellen Datenstrukturen (DTOs) vom Service und übergibt sie gesammelt an die View."""

        try:
            # Alle benötigten Datenbereiche als DTOs abfragen
            area_a_dto = self._service.get_area_a_header()
            area_b1_dto = self._service.get_area_b1_quant_goals()
            area_b2_dto = self._service.get_area_b2_qual_goals()
            area_c_dto = self._service.get_area_c_module_list()

            # Daten an die Haupt-View übergeben, damit sich die Labels neu zeichnen
            self._view.update_view(area_a_dto, area_b1_dto, area_b2_dto, area_c_dto)
            self._logger.debug("UI-Komponenten erfolgreich mit frischen DTOs versorgt.")

        except Exception as e:
            self.show_error_message(f"Fehler beim Aktualisieren des Dashboards: {str(e)}")

    def on_module_save_requested(self, dto: 'ModuleDTO', window_master=None) -> bool:
        """
        Wird aufgerufen, wenn im Bearbeitungsfenster ein Modul gespeichert werden soll.
        Gibt True zurück, wenn der Speicherprozess im Service erfolgreich war.
        """
        try:
            self._service.save_module(dto)
            self.refresh_ui()
            return True
        except Exception as e:
            self._logger.error(f"Fehler beim Speichern des Moduls abgefangen: {str(e)}")
            self.show_error_message(str(e), master=window_master)
            return False

    def on_semester_settings_save_requested(self, dto: 'SemesterDTO') -> None:
        """Nimmt die geänderten Semestereinstellungen entgegen und reicht sie an den Service weiter."""
        try:
            self._service.save_semester_settings(dto)
            self.refresh_ui()
        except Exception as e:
            self.show_error_message(f"Fehler beim Speichern der Semesterziele: {str(e)}")

    def show_error_message(self, msg: str, master=None) -> None:
        """Öffnet ein modales Fehler-Popup."""
        from ui.windows.error_window import ErrorWindow

        # Fallback auf die Hauptansicht, falls kein spezifischer Master übergeben wurde
        chosen_master = master if master is not None else self._view

        try:
            # Die Referenz wird im Controller gehalten, damit das Fenster geöffnet bleibt
            self._active_error_win = ErrorWindow(master=chosen_master, title="Ungültige Eingabe", error_message=msg)

            # Das Fenster aktiv in den Vordergrund des Betriebssystems zwingen
            self._active_error_win.lift()
            self._active_error_win.attributes("-topmost", True)
        except Exception as e:
            self._logger.error(f"Kritischer Fehler beim Rendern des Error-Fensters: {str(e)}")

    def open_edit_semester_dialog(self) -> None:
        """Öffnet das Konfigurationsfenster für das aktuell aktive Semester oder ein neues Folgesemester."""
        from ui.windows.edit_semester_window import EditSemesterWindow
        from dtos.requestDTOs.semester_dto import SemesterDTO
        from datetime import date

        semester_window = EditSemesterWindow(master=self._view, controller=self)
        current_num = self._service._model.current_semester

        # Suchen, ob für die aktuelle Semesternummer bereits Daten vorliegen
        target_semester = next((s for s in self._service._model.semesters if s.number == current_num), None)

        if target_semester:
            # Fall A: Semester existiert bereits -> Bestehende Infromationen in der Maske laden
            semester_req_dto = SemesterDTO(
                semester_number=target_semester.number,
                target_ects=target_semester.target_ects,
                start_date=target_semester.start_date,
                end_date=target_semester.end_date
            )
            semester_window.set_data(semester_req_dto)
        else:
            # Fall B: Neues Semester anlegen -> Standard-Vorauswahl anbieten
            new_semester_num = len(self._service._model.semesters) + 1
            blank_dto = SemesterDTO(
                semester_number=new_semester_num,
                target_ects=30,
                start_date=date.today(),
                end_date=date.today()
            )
            semester_window.set_data(blank_dto)

    def open_add_module_dialog(self) -> None:
        """Öffnet das Eingabefenster für Module und lädt die verfügbaren Semester für das Dropdown."""
        from ui.windows.edit_module_window import EditModuleWindow
        from dtos.requestDTOs.semester_dto import SemesterDTO

        module_window = EditModuleWindow(master=self._view, controller=self)

        # Liste aller registrierten Semester als DTOs für das UI-Auswahlmenü aufbereiten
        semesters_dtos = []
        for sem in self._service._model.semesters:
            semesters_dtos.append(
                SemesterDTO(
                    semester_number=sem.number,
                    target_ects=sem.target_ects,
                    start_date=sem.start_date,
                    end_date=sem.end_date
                )
            )
        module_window.set_data(semesters_dtos)

    def open_general_settings_dialog(self) -> None:
        """Öffnet das globale Einstellungsfenster und übergibt die aktuellen Stammdaten."""
        from ui.windows.general_settings_window import GeneralSettingsWindow
        from dtos.requestDTOs.semester_dto import SemesterDTO

        settings_window = GeneralSettingsWindow(master=self._view, controller=self)
        settings_dto = self._service.get_area_a_header()

        # Ergänzen der reinen Modelldaten für das Einstellungsformular
        settings_dto.current_semester_index = self._service._model.current_semester
        settings_dto.target_gpa = self._service._model.target_gpa
        settings_dto.degree_type = self._service._model.degree.value

        # Semesterliste für die Zuordnung des aktiven Semesters aufbereiten
        semesters_dtos = []
        for sem in self._service._model.semesters:
            semesters_dtos.append(
                SemesterDTO(
                    semester_number=sem.number,
                    target_ects=sem.target_ects,
                    start_date=sem.start_date,
                    end_date=sem.end_date
                )
            )
        settings_window.set_data(settings_dto, semesters_dtos)

    def on_settings_save_requested(self, user_name: str, program_name: str, degree: str, target_gpa: float,
                                   active_semester: int) -> None:
        """Nimmt die geänderten globalen Stammdaten entgegen und schreibt sie direkt in das Datenmodell."""
        try:
            self._logger.info(f"Globale Einstellungen für Studierende(n) '{user_name}' werden verarbeitet.")
            model = self._service._model

            # Validierung des Namensfeldes gegen Leerzeichen oder Total-Löschungen
            if user_name and str(user_name).strip():
                model.user_name = str(user_name).strip()
            else:
                model.user_name = "Student"

            model.name = program_name
            model.target_gpa = target_gpa
            model.current_semester = active_semester

            from models.enums import DegreeType
            try:
                model.degree = DegreeType(degree)
            except ValueError:
                pass

            # Über den Service direkt das Repository anweisen, den neuen Zustand in der JSON zu sichern
            self._service._repository.save(model)
            self.refresh_ui()

        except Exception as e:
            self._logger.error(f"Fehler beim Sichern der globalen Stammdaten: {str(e)}")