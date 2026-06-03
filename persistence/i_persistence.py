from abc import ABC, abstractmethod
from models.study_program import StudyProgram


class IPersistence(ABC):
    """
    Schnittstelle für die Datenhaltung.
    Definiert die notwendigen Methoden zum Speichern und Laden des Studienprogramms.
    Dies ermöglicht es, die Speicherart (z. B. JSON oder später eine Datenbank)
    flexibel auszutauschen.
    """

    @abstractmethod
    def save(self, program: StudyProgram) -> None:
        """
        Abstrakte Methode zum Speichern des gesamten Studienprogramms.
        Muss von der implementierenden Klasse überschrieben werden.
        """
        pass

    @abstractmethod
    def load(self) -> StudyProgram:
        """
        Abstrakte Methode zum Laden und Zurückgeben des Studienprogramms.
        Muss von der implementierenden Klasse überschrieben werden.
        """
        pass