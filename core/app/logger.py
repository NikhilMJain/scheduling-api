import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s ----> %(message)s")

file_handler = logging.FileHandler(filename="error.log")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)