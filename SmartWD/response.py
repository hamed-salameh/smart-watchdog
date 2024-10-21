# response.py
from observer import Observer

class Response(Observer):
    """
    The Response class is an observer that reacts to events raised by the DomainEvent.
    """

    def handle_event(self, message):
        """
        Handle the event and respond by printing the message.

        :param message: The event message.
        """
        print(f"Response to event: {message}")
