from fastapi import FastAPI
from util_functions import write_log
import uvicorn
import sys
from urllib.parse import urlparse
import requests
from kafka import KafkaConsumer

app = FastAPI()

TOPIC_NAME = "messages"

def get_service_ips(service_name):
    try:
        response = requests.get(f"{config_server_url}/services/{service_name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {service_name} IPs: {e}")
        return []

@app.get("/")
def get_data():
    write_log("Get request", port)

    messages = []
    
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=kafka_url,
        auto_offset_reset="earliest",
        consumer_timeout_ms=5000
    )

    for msg in consumer:
        messages.append(msg.value.decode())

    write_log(f"Get request answer: {messages}", port)

    return {"msg": messages}

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: script.py <host_url> <config_server_url> <messages_service_idx>")
        sys.exit(1)

    host_url = urlparse(sys.argv[1])
    config_server_url = sys.argv[2]
    messages_service_idx = int(sys.argv[3])

    kafka_services = get_service_ips("kafka-services")
    kafka_url = kafka_services[messages_service_idx]

    port = host_url.port

    write_log("Starting up server", port)

    uvicorn.run(app, host=host_url.hostname, port=port)
