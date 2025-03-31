from fastapi import FastAPI
import uvicorn
import sys
from domain import *
from urllib.parse import urlparse

app = FastAPI()

@app.get("/")
def get_data():
    return {"msg": "Not implemented yet."}

if __name__ == "__main__":
    host_url = urlparse(sys.argv[1])
    uvicorn.run(app, host=host_url.hostname, port=host_url.port)
