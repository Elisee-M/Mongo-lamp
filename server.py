from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
# http://127.0.0.1:5500/index.html
db = client["iot"]
collection = db["device"]

class Light(BaseModel):
    state: str


@app.post("/set")
def set_light(light: Light):
    collection.update_one(
        {"name": "esp32_light"},
        {"$set": {"state": light.state}}
    )
    return {"message": "updated"}


@app.get("/get")
def get_light():
    data = collection.find_one({"name":"esp32_light"})
    return {"state": data["state"]}