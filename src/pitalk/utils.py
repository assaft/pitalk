import logging

def init_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the log format
    )
