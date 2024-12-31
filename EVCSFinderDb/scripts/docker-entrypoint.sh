#!/bin/sh

# Start MongoDB
mongod --bind_ip_all --logpath /var/log/mongod.log &

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until mongo --eval "print('MongoDB is ready')" 2>/dev/null; do
    sleep 1
done

# Populate the MongoDB database
echo "Populating the database, please wait. This might take a few minutes..."
python3 -u /app/scripts/populate_db.py
echo "Database successfully populated"

# Keep MongoDB running in the foreground
wait
