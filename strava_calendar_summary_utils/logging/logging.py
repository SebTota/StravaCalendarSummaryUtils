from google.cloud.logging import Client as LogClient


class Logging:
    __single = None

    def __init__(self):
        if not Logging.__single:
            Logging.__single = self
            self.logging_client = LogClient()
            self.logging_client.setup_logging()
