from Monitors.kafka_monitor import KafkaMonitor
from Monitors.oracle_monitor import OracleMonitor

class Messaging:
    """
    The Messaging class coordinates monitoring of Kafka and Oracle.
    """

    def __init__(self, kafka_topic, oracle_dsn, oracle_user, oracle_password):
        self.kafka_monitor = KafkaMonitor(kafka_topic)
        self.oracle_monitor = OracleMonitor(oracle_dsn, oracle_user, oracle_password)

    def monitor_kafka(self):
        """
        Start monitoring Kafka.
        """
        self.kafka_monitor.monitor()

    def monitor_oracle(self):
        """
        Start monitoring Oracle database.
        """
        self.oracle_monitor.monitor_active_sessions()
        # Call other Oracle monitoring methods as needed
