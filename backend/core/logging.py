import logging

def setup_logger(log_file="app.log", log_level=logging.INFO):
    logging.basicConfig(
        level = log_level,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
