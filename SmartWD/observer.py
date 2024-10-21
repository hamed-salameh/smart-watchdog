# observer.py
from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Abstract base class for observers in the Observer pattern.
    Observers must implement the 'handle_event' method to handle events.
    """
    @abstractmethod
    def handle_event(self, message):
        """
        Handle the event raised by the Subject (DomainEvent).

        :param message: The event message to handle.
        """
        pass
