# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
from pymongo import MongoClient
import json

# ------------------ MongoDB Setup ------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["iot_db"]          # Database name
    collection = db["data"]        # Collection name
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

# ------------------ HTTP Server ------------------
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Always respond properly to prevent infinite loading
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Example: fetch data from MongoDB
        try:
            items = list(collection.find({}, {"_id": 0}))  # Don't return _id
            response = {"status": "success", "data": items}
        except Exception as e:
            response = {"status": "error", "message": str(e)}

        self.wfile.write(json.dumps(response).encode("utf-8"))

# ------------------ Run Server ------------------
def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("🌐 Server running at http://127.0.0.1:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()