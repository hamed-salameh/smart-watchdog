import psutil
from domain_event import DomainEvent

class ProcessMonitor:
    """
    The ProcessMonitor class monitors various resources of a process such as CPU utilization,
    memory usage, thread count, and handle count. It handles multiple instances of the same
    process name. If any resource exceeds the provided threshold, an event is raised.
    If no processes match the provided name, a 'ProcessNotFound' event is raised.
    """

    def __init__(self, process_name, memory_threshold_mb=None, cpu_threshold_percent=None,
                 thread_threshold=None, handle_threshold=None):
        """
        Initialize the ProcessMonitor object with process details and thresholds for monitoring.

        :param process_name: Name of the process to monitor.
        :param memory_threshold_mb: Memory usage threshold in MB (None means no threshold check).
        :param cpu_threshold_percent: CPU usage threshold in percentage (None means no threshold check).
        :param thread_threshold: Thread count threshold (None means no threshold check).
        :param handle_threshold: Handle count threshold (None means no threshold check).
        """
        self.process_name = process_name
        self.memory_threshold_mb = memory_threshold_mb
        self.cpu_threshold_percent = cpu_threshold_percent
        self.thread_threshold = thread_threshold
        self.handle_threshold = handle_threshold

    def monitor_resources(self):
        """
        Monitor various process resources and raise events if any exceed the defined thresholds.
        If no processes with the specified name are found, a 'ProcessNotFound' event is raised.
        """
        found_processes = []  # List to track found processes
        try:
            for proc in psutil.process_iter(
                    ['pid', 'name', 'memory_info', 'cpu_percent', 'num_threads', 'num_handles']):
                if proc.info['name'] == self.process_name:
                    found_processes.append(proc)  # Collect found processes

                    memory_usage_mb = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                    cpu_usage_percent = proc.info['cpu_percent']
                    thread_count = proc.info['num_threads']
                    handle_count = proc.info['num_handles'] if hasattr(proc.info,
                                                                       'num_handles') else None  # Windows only

                    # Check memory usage threshold
                    if self.memory_threshold_mb is not None and memory_usage_mb > self.memory_threshold_mb:
                        DomainEvent.raise_event(
                            f"Memory usage of process '{self.process_name}' (PID: {proc.info['pid']}) exceeds {self.memory_threshold_mb} MB: {memory_usage_mb:.2f} MB"
                        )

                    # Check CPU usage threshold
                    if self.cpu_threshold_percent is not None and cpu_usage_percent > self.cpu_threshold_percent:
                        DomainEvent.raise_event(
                            f"CPU usage of process '{self.process_name}' (PID: {proc.info['pid']}) exceeds {self.cpu_threshold_percent}%: {cpu_usage_percent:.2f}%"
                        )

                    # Check thread count threshold
                    if self.thread_threshold is not None and thread_count > self.thread_threshold:
                        DomainEvent.raise_event(
                            f"Thread count of process '{self.process_name}' (PID: {proc.info['pid']}) exceeds {self.thread_threshold}: {thread_count} threads"
                        )

                    # Check handle count threshold (Windows-specific)
                    if handle_count is not None and self.handle_threshold is not None and handle_count > self.handle_threshold:
                        DomainEvent.raise_event(
                            f"Handle count of process '{self.process_name}' (PID: {proc.info['pid']}) exceeds {self.handle_threshold}: {handle_count} handles"
                        )

            # Raise event if no processes were found
            if not found_processes:
                DomainEvent.raise_event(f"Process '{self.process_name}' not found")

        except Exception as e:
            DomainEvent.raise_event(f"Error monitoring resources for '{self.process_name}': {str(e)}")
