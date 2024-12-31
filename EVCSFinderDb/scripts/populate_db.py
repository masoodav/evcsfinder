import os
import json
import logging
from pymongo import MongoClient
from tqdm import tqdm
import sys
from pymongo.errors import BulkWriteError

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(message)s")  # Updated to DEBUG level
sys.stdout.reconfigure(line_buffering=True)  # Ensure logs are not buffered

# Database configuration
db_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017/ev_charging")
client = MongoClient(db_url)
db = client.get_database()

BATCH_SIZE = 100  # Adjust batch size as needed

def process_file(file_path):
    """Read and load JSON data from a file."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON in {file_path}: {e}")
        return []
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return []

def load_referencedata(referencedata_path):
    """Load reference data for ID lookups."""
    if not os.path.exists(referencedata_path):
        logging.error(f"Referencedata file {referencedata_path} does not exist.")
        return {}
    return process_file(referencedata_path)

def sanitize_poi_data(poi_data):
    """Sanitize POI data by removing or replacing invalid fields."""
    sanitized_data = []
    for poi in poi_data:
        if poi.get("DataType") is None:
            poi["DataType"] = ""  # Replace None with an empty string
        if poi.get("MetadataFieldOptions") is None:
            poi["MetadataFieldOptions"] = []  # Replace None with an empty list

        # Remove keys with None or empty values
        poi = {key: value for key, value in poi.items() if value not in [None, {}, []]}

        sanitized_data.append(poi)
    return sanitized_data

def optimize_data_with_referencedata(poi_data, referencedata):
    """Optimize POI data by replacing IDs with human-readable values."""
    sanitized_data = sanitize_poi_data(poi_data)

    # Create a lookup dictionary for countries by their ID
    country_lookup = {country["ID"]: country["Title"] for country in referencedata.get("Countries", [])}
    
    # Create a lookup dictionary for connection types by their ID
    conn_type_lookup = {conn["ID"]: conn["Title"] for conn in referencedata.get("ConnectionTypes", [])}

    # Create a lookup dictionary for current types by their ID
    current_type_lookup = {curr_type["ID"]: curr_type["Title"] for curr_type in referencedata.get("CurrentTypes", [])}

    for poi in sanitized_data:
        # Replace CountryID in AddressInfo if it exists
        if "AddressInfo" in poi and "CountryID" in poi["AddressInfo"]:
            country_id = poi["AddressInfo"]["CountryID"]
            if country_id in country_lookup:
                poi["AddressInfo"]["Country"] = country_lookup[country_id]
        
        # Replace ConnectionTypeID and CurrentTypeID in Connections if they exist
        if "Connections" in poi:
            for connection in poi["Connections"]:
                conn_type_id = connection.get("ConnectionTypeID")
                if conn_type_id in conn_type_lookup:
                    connection["ConnectionType"] = conn_type_lookup[conn_type_id]
                current_type_id = connection.get("CurrentTypeID")
                if current_type_id in current_type_lookup:
                    connection["CurrentType"] = current_type_lookup[current_type_id]
    
    return sanitized_data

def load_ocm_data(data_dir, referencedata_path, force_load=False):
    """Load OCM data from multiple JSON files in nested directories into MongoDB."""
    logging.debug(f"Force Load: {force_load}")  # Log the force load status

    if not os.path.exists(data_dir):
        logging.error(f"Data directory {data_dir} does not exist.")
        return

    referencedata = load_referencedata(referencedata_path)
    if not referencedata:
        logging.error("Failed to load referencedata. Aborting.")
        return

    # Check if the collection is already populated
    if not force_load and db.stations.estimated_document_count() > 0:
        logging.info("Database is already populated. Skipping data load.")
        return

    # Clear existing data
    try:
        db.stations.delete_many({})
        logging.info("Cleared existing data from the 'stations' collection.")
    except Exception as e:
        logging.error(f"Error clearing data from 'stations' collection: {e}")
        return

    # Collect all JSON files
    file_list = [
        os.path.join(root, filename)
        for root, _, files in os.walk(data_dir)
        for filename in files
        if filename.endswith(".json") and filename != "referencedata.json"
    ]

    if not file_list:
        logging.error("No JSON files found in the specified directory.")
        return

    logging.info(f"Found {len(file_list)} files to process.")

    # Process files and insert data in batches
    current_batch = []
    total_inserted = 0

    with tqdm(total=len(file_list), desc="Processing files", unit="file", ncols=80, dynamic_ncols=True, leave=True, file=sys.stdout) as pbar:
        for file_path in file_list:
            file_data = process_file(file_path)

            if isinstance(file_data, list):  # Add multiple records if it's a list
                optimized_data = optimize_data_with_referencedata(file_data, referencedata)
                current_batch.extend(optimized_data)
            elif isinstance(file_data, dict):  # Add a single record if it's a dict
                optimized_data = optimize_data_with_referencedata([file_data], referencedata)
                current_batch.extend(optimized_data)

            # Insert the batch if it reaches the specified size
            if len(current_batch) >= BATCH_SIZE:
                try:
                    db.stations.insert_many(current_batch)
                    total_inserted += len(current_batch)
                    current_batch.clear()  # Clear the batch after insertion
                except BulkWriteError as bwe:
                    logging.error(f"Bulk write error: {bwe.details}")
                except Exception as e:
                    logging.error(f"Error inserting batch: {e}")

            pbar.update(1)

    # Insert any remaining data in the batch
    if current_batch:
        try:
            db.stations.insert_many(current_batch)
            total_inserted += len(current_batch)
        except BulkWriteError as bwe:
            logging.error(f"Bulk write error: {bwe.details}")
        except Exception as e:
            logging.error(f"Error inserting final batch: {e}")

    logging.info(f"Inserted {total_inserted} documents into the 'stations' collection.")

if __name__ == "__main__":
    force_load = os.getenv("FORCE_LOAD", "false").lower() == "true"
    referencedata_path = "/app/ocm-export/data/referencedata.json"
    data_dir = "/app/ocm-export/data"
    load_ocm_data(data_dir, referencedata_path, force_load=force_load)
