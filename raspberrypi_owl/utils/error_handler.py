import logging

class ErrorHandler:
    def __init__(self, logger):
        self.logger = logger

    def handle_error(self, error_message):
        self.logger.error(f"Error occurred: {error_message}")
        # Add recovery steps or cleanup as needed
