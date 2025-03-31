import requests
import sys
import uvicorn
from random import randint
import uuid
import json
from random import shuffle
from fastapi import FastAPI
from domain import *
from urllib.parse import urlparse

messages_urls = None
logging_urls = []

app = FastAPI()

def get_service_ips(service_name):
    try:
        response = requests.get(f"{config_server_url}/services/{service_name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {service_name} IPs: {e}")
        return []

@app.post("/")
def add_data(message: dict):
    uuid_val = uuid.uuid4()
    data = {"uuid": str(uuid_val), "msg": message.get("msg", "")}
    
    shuffled_urls = logging_urls[:]
    shuffle(shuffled_urls)
    
    for url in shuffled_urls:
        try:
            response = requests.post(url, json=data, timeout=3)
            if response.status_code == 200:
                print("Message sent successfully")
                return {"msg": "success"}
        except requests.exceptions.RequestException as e:
            return(f"Error with logging service {url}: {e}")
    
    return {"msg": f"logging service mistake {response.status_code}"}


@app.get("/")
def get_data():
    shuffled_logging_urls = logging_urls[:]
    shuffle(shuffled_logging_urls)
    
    for url in shuffled_logging_urls:
        try:
            logging_service_response = requests.get(url, timeout=3)
            if logging_service_response.status_code == 200:
                logging_messages = json.loads(logging_service_response.content.decode("utf-8"))
                break
        except requests.exceptions.RequestException as e:
            print(f"Error with logging service {url}: {e}")
    else:
        logging_messages = {"error": "No logging service available"}
    
    try:
        messages_service_response = requests.get(messages_urls[0], timeout=3)
        messages_service_messages = json.loads(messages_service_response.content.decode("utf-8"))
    except requests.exceptions.RequestException as e:
        print(f"Error with messages service {messages_urls[0]}: {e}")
        messages_service_messages = {"error": "Messages service unavailable"}
    
    return {"logging_service_response": logging_messages, "messages_service_response": messages_service_messages}


if __name__ == "__main__":
    host_url = urlparse(sys.argv[1])
    config_server_url = sys.argv[2]

    messages_urls = get_service_ips("messages-service")
    logging_urls = get_service_ips("logging-services")

    uvicorn.run(app, host=host_url.hostname, port=host_url.port)
