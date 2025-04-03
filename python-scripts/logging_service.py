from fastapi import FastAPI
import uvicorn
import hazelcast
import sys
import os
from urllib.parse import urlparse
from domain import *

app = FastAPI()
distributed_map = None
client = None
host_url = None
port = None


def write_log(message: str, port: int):
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    script_name = os.path.basename(sys.argv[0])
    log_path = os.path.join(log_dir, f"{script_name}-{port}.txt")

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


@app.post("/")
def add_data(data: DataModel):
    write_log("Post request", port)
    write_log(f"Added key: {data.uuid} with value: {data.msg} by logging service: {host_url}", port)
    distributed_map.set(data.uuid, data.msg)
    return {"msg": "success"}

@app.get("/")
def get_data():
    write_log("Get request", port)

    messages = distributed_map.entry_set()
    return {"messages": messages}

@app.on_event("startup")
def startup_event():
    # write_log("Start up service", port)

    global distributed_map, client, host_url, port

    if len(sys.argv) < 3:
        print("Usage: python main.py <host_url> <hazelcast_url>")
        sys.exit(1)

    host_url = sys.argv[1]
    hazelcast_url = sys.argv[2]

    parsed_url = urlparse(host_url)
    port = parsed_url.port

    client = hazelcast.HazelcastClient(cluster_members=[hazelcast_url])
    distributed_map = client.get_map("my-distributed-map").blocking()

if __name__ == "__main__":
    parsed_url = urlparse(sys.argv[1])
    uvicorn.run(app, host=parsed_url.hostname, port=parsed_url.port)
