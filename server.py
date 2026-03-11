from fastapi import FastAPI, Request
from pymongo import MongoClient
from fastapi.responses import JSONResponse

app = FastAPI()

# ------------------ MongoDB ------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["iot_db"]
    collection = db["commands"]
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

# ------------------ GET test ------------------
@app.get("/")
async def root():
    return {"message": "Server is running"}

# ------------------ POST /set ------------------
@app.post("/set")
async def set_state(request: Request):
    data = await request.json()  # get JSON from client
    state = data.get("state", "UNKNOWN")

    # Save to MongoDB
    try:
        collection.insert_one({"state": state})
        print(f"📌 Button pressed: {state}")  # Show in terminal
    except Exception as e:
        print("❌ DB insert error:", e)
        return JSONResponse(content={"status": "error", "message": str(e)})

    return {"status": "success", "state": state}