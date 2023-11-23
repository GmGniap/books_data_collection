import logging
import json


def set_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s|%(levelname)s - %(message)s", datefmt="%d-%b-%Y %H:%M"
    )
    fh = logging.FileHandler("log_files/we.log", "a")
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


def write_json_file(filename: str, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False)
