# domain_event.py
class DomainEvent:
    """
    A class that acts as the Subject in the Observer pattern.
    It maintains a list of observers and notifies them of events.
    """
    _observers = []

    @classmethod
    def subscribe(cls, observer):
        """
        Subscribe an observer to listen for events.

        :param observer: An instance of a class that implements the Observer interface.
        """
        cls._observers.append(observer)

    @classmethod
    def unsubscribe(cls, observer):
        """
        Unsubscribe an observer from the event system.

        :param observer: An instance of a class that implements the Observer interface.
        """
        cls._observers.remove(observer)

    @classmethod
    def raise_event(cls, message):
        """
        Notify all subscribed observers of an event.

        :param message: The event message to be passed to observers.
        """
        for observer in cls._observers:
            observer.handle_event(message)
