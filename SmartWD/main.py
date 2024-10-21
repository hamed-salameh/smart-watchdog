# main.py
from Monitors.process_monitor import ProcessMonitor
from messaging import Messaging
from response import Response
from domain_event import DomainEvent
import json

def load_configuration(file_path):
    """
    Load the process monitoring configuration from a JSON file.

    :param file_path: Path to the JSON configuration file.
    :return: List of process configurations.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config["processes"], config["kafka"], config["oracle"]
    except FileNotFoundError:
        raise Exception(f"Configuration file {file_path} not found.")
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON file: {str(e)}")


def main():
    """
    Main entry point of the application. It initializes all systems,
    subscribes observers, and starts monitoring Kafka topics, Oracle, and proc ess resources.
    """
    # Load configuration from a JSON file
    config_file = "monitoring_config.json"
    process_configs, kafka_config, oracle_config = load_configuration(config_file)

    # Initialize the response handler (observer)
    response = Response()

    # Subscribe the response handler to the event system
    DomainEvent.subscribe(response)

    # Initialize and start process monitors based on the loaded configuration
    for process_config in process_configs:
        process_monitor = ProcessMonitor(
            process_name=process_config["name"],
            memory_threshold_mb=process_config.get("memory_threshold_mb"),
            cpu_threshold_percent=process_config.get("cpu_threshold_percent"),
            thread_threshold=process_config.get("thread_threshold"),
            handle_threshold=process_config.get("handle_threshold")
        )

        # Start resource usage monitoring for each process
        print(f"Starting resource monitoring for {process_config['name']}...")
        process_monitor.monitor_resources()

    # Initialize the messaging system
    messaging = Messaging(kafka_topic=kafka_config["topic"],
                          oracle_dsn=(oracle_config["host"], oracle_config["port"]),
                          oracle_user=oracle_config["user"],
                          oracle_password=oracle_config["password"])

    # Start Kafka monitoring
    print("Starting Kafka monitoring...")
    messaging.monitor_kafka()

    # Start Oracle monitoring
    print("Starting Oracle monitoring...")
    messaging.monitor_oracle()

if __name__ == "__main__":
    main()
