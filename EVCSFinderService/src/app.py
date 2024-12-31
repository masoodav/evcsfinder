import os
import logging
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(filename='/app/debug.log', level=logging.DEBUG)

# Connect to MongoDB
db_url = os.getenv("DATABASE_URL", "mongodb://evcsfinder-db:27017/ev_charging")
client = MongoClient(db_url)
db = client.get_database()

# Ensure to have a text index on the AddressInfo field
db.stations.create_index([("AddressInfo.Title", "text"), ("AddressInfo.AddressLine1", "text"), ("AddressInfo.Town", "text"), ("AddressInfo.StateOrProvince", "text"), ("AddressInfo.Postcode", "text"), ("AddressInfo.CountryID", "text")])

# Endpoint: Health Check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# Endpoint: Search Charging Stations by Address
@app.route("/stations/search", methods=["GET"])
def search_stations():
    address_query = request.args.get("address")
    if not address_query:
        return jsonify({"error": "Address parameter is required"}), 400

    # Use regex to perform an exact match search
    regex = f"^.*{address_query}.*$"
    stations = db.stations.find({"AddressInfo.Title": {"$regex": regex, "$options": "i"}}, {"_id": 0})
    result = [station for station in stations]
    return jsonify(result)


# Endpoint: Check Database Status
@app.route("/db-status", methods=["GET"])
def db_status():
    try:
        # Perform a simple query to check if the DB is ready
        if db.stations.count_documents({}) > 0:
            return jsonify({"status": "ready"})
        else:
            return jsonify({"status": "initializing"})
    except ConnectionFailure:
        return jsonify({"status": "error", "message": "Cannot connect to database"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
