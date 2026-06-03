import logging
from datetime import date
from typing import TYPE_CHECKING
from models.module import Module, ModulStatus
from models.semester import Semester

# Schutz vor zyklischen Importen
if TYPE_CHECKING:
    from persistence.i_persistence import IPersistence
    from dtos.responseDTOs.area_a_header_dto import AreaAHeaderDTO
    from dtos.responseDTOs.area_b1_quant_goals_dto import AreaB1QuantGoalsDTO
    from dtos.responseDTOs.area_b2_qual_goals_dto import AreaB2QualGoalsDTO as AreaB2QualGoalsDTO
    from dtos.responseDTOs.area_c_module_list_dto import AreaCModuleListDTO
    from dtos.requestDTOs.module_dto import ModuleDTO
    from dtos.requestDTOs.semester_dto import SemesterDTO

logger = logging.getLogger(__name__)


class StudyService:
    """
    Der zentrale Anwendungs-Service (Business Logic Layer).
    Verarbeitet UI-Anfragen, bereitet die Modelldaten mithilfe von Hilfsservices
    als DTOs für die Oberfläche vor und steuert die Daten-Speicherung.
    """

    def __init__(self, repository: 'IPersistence'):
        self._repository = repository
        # Lädt den aktuellen Zustand des Studienprogramms aus der Datenquelle
        self._model = self._repository.load()

        # Hilfsservices für spezifische mathematische Auswertungen
        from services.grade_services import GradeService
        from services.ects_services import ECTSService
        self._grade_service = GradeService()
        self._ects_service = ECTSService()

    # --- RESPONSE METHODEN (Datenaufbereitung für das UI) ---

    def get_area_a_header(self) -> 'AreaAHeaderDTO':
        """Bereitet die Daten für den oberen Header-Bereich (Area A) vor."""
        from dtos.responseDTOs.area_a_header_dto import AreaAHeaderDTO
        return AreaAHeaderDTO(
            user_name=self._model.user_name,
            study_program_name=self._model.name,
            current_semester_count=len(self._model.semesters)
        )

    def get_area_b1_quant_goals(self) -> 'AreaB1QuantGoalsDTO':
        """Bereitet die quantitativen Daten (ECTS und Tage) für Area B1 vor."""
        from dtos.responseDTOs.area_b1_quant_goals_dto import AreaB1QuantGoalsDTO

        # Ausgewähltes Semester ermitteln
        current_semester_num = self._model.current_semester
        current_sem = next((s for s in self._model.semesters if s.number == current_semester_num), None)

        # Fallback auf das letzte Semester, falls der Index ungültig ist
        if not current_sem and self._model.semesters:
            current_sem = self._model.semesters[-1]

        return AreaB1QuantGoalsDTO(
            current_semester_ects=current_sem.calculate_current_ects() if current_sem else 0,
            semester_target_ects=current_sem.target_ects if current_sem else 0,
            total_study_ects=self._ects_service.get_total_study_summary(self._model),
            total_progress_percent=self._ects_service.calculate_semester_progress_percent(current_sem) if current_sem else 0,
            days_until_semester_end=current_sem.get_days_left() if current_sem else 0
        )

    def get_area_b2_qual_goals(self) -> 'AreaB2QualGoalsDTO':
        """
        Bereitet die qualitativen Daten (Notenschnitte und Prognosen) für Area B2 vor.
        Trennt den Schnitt des aktuellen Semesters vom Gesamtschnitt des Studiums.
        """
        from dtos.responseDTOs.area_b2_qual_goals_dto import AreaB2QualGoalsDTO

        # 1. Aktuell ausgewähltes Semester im Studienprogramm ermitteln
        current_semester_num = self._model.current_semester
        current_sem = next((s for s in self._model.semesters if s.number == current_semester_num), None)

        # 2. Notenschnitte strikt getrennt voneinander berechnen
        # Wenn kein Semester aktiv ist, starten wir beim Semester-Schnitt mit 0.0
        semester_gpa = current_sem.get_semester_gpa() if current_sem else 0.0
        overall_gpa = self._model.calculate_total_gpa()
        target = self._model.target_gpa

        # 3. Berechnen der Notenprognose über den GradeService
        if self._grade_service.is_target_reachable(self._model, target):
            needed = self._grade_service.predict_needed_grade(self._model, target)
            msg = f"Nächste Note benötigt: {needed}"
        else:
            n = self._grade_service.get_required_top_grades(self._model, target)
            msg = f"Serie von {n}x 1.0 benötigt!"

        # 4. Daten vollständig und getrennt an den Datencontainer übergeben
        return AreaB2QualGoalsDTO(
            current_gpa=semester_gpa,
            target_gpa=target,
            total_gpa=overall_gpa,  # Übergibt den echten Gesamtschnitt an das kleine Label
            correction_message=msg,
            performance_status=self._model.get_performance_status()
        )

    def get_area_c_module_list(self) -> 'AreaCModuleListDTO':
        """Bereitet die Modulliste strukturiert nach Semestern für die Anzeige (Area C) vor."""
        from dtos.responseDTOs.area_c_module_list_dto import AreaCModuleListDTO

        all_semester_data = []
        for sem in self._model.semesters:
            module_items = []
            for mod in sem.modules:
                module_items.append({
                    "module_code": mod.module_code,
                    "name": mod.name,
                    "ects": mod.ects,
                    "grade": mod.exam.grade if mod.is_finished() else None,
                    "status": mod.status.value
                })

            all_semester_data.append({
                "semester_number": sem.number,
                "modules": module_items
            })

        return AreaCModuleListDTO(semester_groups=all_semester_data)

    # --- REQUEST METHODEN (Datenverarbeitung aus dem UI) ---

    def save_module(self, dto: 'ModuleDTO') -> None:
        """
        Nimmt die Moduldaten aus der Maske entgegen, sucht das passende Semester
        und aktualisiert das bestehende Modul oder legt ein neues an.
        """
        # 1. Ziel-Semester bestimmen
        current_semester_num = self._model.current_semester
        target_semester = next((s for s in self._model.semesters if s.number == current_semester_num), None)

        # Automatisches Sicherheitsnetz: Erstellt das Semester, falls es noch fehlt
        if not target_semester:
            target_semester = Semester(current_semester_num, 30, date.today(), date.today())
            self._model.semesters.append(target_semester)

        # 2. Prüfen, ob das Modul bereits existiert
        existing_module = next((m for m in target_semester.modules if m.module_code == dto.module_code), None)

        if existing_module:
            # Fall A: Bestehendes Modul aktualisieren
            existing_module.name = dto.module_name
            existing_module.ects = dto.ects
            existing_module.status = ModulStatus(dto.status)

            # Notenstatus über die saubere Modell-Logik steuern
            if existing_module.status == ModulStatus.COMPLETED:
                existing_module.set_completion(dto.exam_grade)
            else:
                # Modul ist offen/geplant: Prüfung zurücksetzen
                existing_module.exam._grade = None
                existing_module.exam.is_passed = False
        else:
            # Fall B: Neues Modul registrieren
            new_module = Module(
                module_code=dto.module_code,
                name=dto.module_name,
                ects=dto.ects,
                status=ModulStatus(dto.status)
            )

            if new_module.status == ModulStatus.COMPLETED:
                new_module.set_completion(dto.exam_grade)

            target_semester.modules.append(new_module)

        # 3. Daten persistent in die JSON-Datei schreiben
        self._repository.save(self._model)
        logger.info(f"Modul '{dto.module_code}' erfolgreich verarbeitet und gespeichert.")

    def save_semester_settings(self, dto: 'SemesterDTO') -> None:
        """Aktualisiert die Zeitziele eines Semesters oder löscht es vollständig."""
        target_semester = next((s for s in self._model.semesters if s.number == dto.semester_number), None)

        # LÖSCH-LOGIK: Signalwert -1 bei ECTS löscht das Semester
        if dto.target_ects == -1:
            if target_semester:
                self._model.semesters.remove(target_semester)
                logger.info(f"Semester {dto.semester_number} aus dem Programm entfernt.")

                # Aktiven Semester-Index verschieben, falls das aktuelle gelöscht wurde
                if self._model.current_semester == dto.semester_number:
                    self._model.current_semester = self._model.semesters[-1].number if self._model.semesters else 1

            self._repository.save(self._model)
            return

        # SPEICHER- / AKTUALISIERUNGS-LOGIK
        if target_semester:
            target_semester.target_ects = dto.target_ects
            target_semester.start_date = dto.start_date
            target_semester.end_date = dto.end_date
            logger.info(f"Semester {dto.semester_number} Zeitziele angepasst.")
        else:
            new_semester = Semester(dto.semester_number, dto.target_ects, dto.start_date, dto.end_date)
            self._model.semesters.append(new_semester)
            logger.info(f"Semester {dto.semester_number} neu im Programm angelegt.")

        self._repository.save(self._model)