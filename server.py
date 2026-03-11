from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient

app = FastAPI()

# ------------------ CORS Setup ------------------
origins = ["*"]  # Allow all origins, can restrict to your IP later
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS...
    allow_headers=["*"],
)

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

@app.get("/get")
async def get_state():
    try:
        # Get the last command sent
        last_command = collection.find().sort("_id", -1).limit(1)
        state = "OFF"
        for cmd in last_command:
            state = cmd.get("state", "OFF")
        return {"status": "success", "state": state}
    except Exception as e:
        return {"status": "error", "message": str(e)}