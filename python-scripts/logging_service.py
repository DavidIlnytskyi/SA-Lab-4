from fastapi import FastAPI
import uvicorn
import hazelcast
import sys
from urllib.parse import urlparse
from domain import *

app = FastAPI()
distributed_map = None
client = None
host_url = None
port = None

def write_log(message: str, port: int):
    with open(f"./logs-{port}.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

@app.post("/")
def add_data(data: DataModel):
    write_log(f"Added key: {data.uuid} with value: {data.msg} by logging service: {host_url}", port)
    distributed_map.set(data.uuid, data.msg)
    return {"msg": "success"}

@app.get("/")
def get_data():
    print("Inside logging service, getting the map")
    messages = distributed_map.entry_set()
    return {"messages": messages}

@app.on_event("startup")
def startup_event():
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
    print(f"Connected to Hazelcast at {hazelcast_url}")

if __name__ == "__main__":
    parsed_url = urlparse(sys.argv[1])
    uvicorn.run(app, host=parsed_url.hostname, port=parsed_url.port)
