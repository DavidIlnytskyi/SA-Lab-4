import os
import sys

def write_log(message: str, port: int):
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    script_name = os.path.basename(sys.argv[0])
    log_path = os.path.join(log_dir, f"{script_name}-{port}.txt")

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

