import logging

logger = logging.getLogger(__name__)


class ExamAchievement:
    """
    Repräsentiert die Prüfungsleistung eines Moduls.
    Verwaltet die erzielte Note und prüft automatisch, ob das Modul bestanden wurde.
    """

    def __init__(self):
        # Startwerte: Noch keine Note eingetragen, Modul gilt als nicht bestanden
        self._grade = None
        self.is_passed = False

    @property
    def grade(self):
        """Gibt die aktuell gespeicherte Note zurück."""
        return self._grade

    def is_successful(self, grade: float) -> bool:
        """
        Prüft und setzt den Notenwert. Aktualisiert den Bestanden-Status.
        Gibt True zurück, wenn das Modul mit 4.0 oder besser bestanden wurde.
        """
        # Validierung: Noten müssen im deutschen System zwischen 1.0 und 5.0 liegen
        if 1.0 <= grade <= 5.0:
            self._grade = grade

            # Ein Modul ist mit einer Note von 4.0 oder besser bestanden
            if grade <= 4.0:
                self.is_passed = True
                logger.info(f"Prüfung mit Note {grade} erfolgreich bestanden.")
            else:
                self.is_passed = False
                logger.info(f"Prüfung mit Note {grade} nicht bestanden.")

            return self.is_passed
        else:
            # Fehler protokollieren und abschicken, falls der Wert unplausibel ist
            logger.error(f"Ungültiger Notenwert eingegeben: {grade}")
            raise ValueError("Notenwert muss zwischen 1.0 und 5.0 liegen.")

    def update_grade(self, new_grade: float) -> float:
        """
        Aktualisiert eine bestehende Note mit einem neuen Wert
        und gibt die aktualisierte Note zurück.
        """
        logger.info(f"Notenänderung angefordert: Von {self._grade} auf {new_grade}.")
        self.is_successful(new_grade)
        return self._grade