import cx_Oracle
from domain_event import DomainEvent

class OracleMonitor:
    """
    The OracleMonitor class is responsible for monitoring Oracle database performance metrics.
    """

    def __init__(self, oracle_dsn, oracle_user, oracle_password):
        self.oracle_dsn = oracle_dsn
        self.oracle_user = oracle_user
        self.oracle_password = oracle_password
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the Oracle database.
        """
        try:
            dsn = cx_Oracle.makedsn(*self.oracle_dsn)
            self.connection = cx_Oracle.connect(user=self.oracle_user, password=self.oracle_password, dsn=dsn)
            self.cursor = self.connection.cursor()
            print("Connected to Oracle database.")
        except cx_Oracle.DatabaseError as e:
            DomainEvent.raise_event(f"Error connecting to Oracle database: {str(e)}")

    def monitor_active_sessions(self):
        """
        Monitor active sessions in the Oracle database and raise events if thresholds are breached.
        """
        if not self.cursor or not self.connection:
            self.connect()

        try:
            # Check for active sessions
            self.cursor.execute("SELECT COUNT(*) FROM v$session WHERE status = 'ACTIVE'")
            active_sessions = self.cursor.fetchone()[0]

            if active_sessions > 100:  # Example threshold
                DomainEvent.raise_event(f"Active sessions in Oracle database exceed threshold: {active_sessions}")

        except Exception as e:
            DomainEvent.raise_event(f"Error monitoring Oracle database: {str(e)}")

    def close(self):
        """
        Closes the cursor and the database connection if they are open.
        """
        if self.cursor:
            try:
                self.cursor.close()
                print("Cursor closed.")
            except Exception as e:
                DomainEvent.raise_event(f"Error closing cursor: {str(e)}")

        if self.connection:
            try:
                self.connection.close()
                print("Connection closed.")
            except Exception as e:
                DomainEvent.raise_event(f"Error closing connection: {str(e)}")
