# EVCSFinder

EVCSFinder is an open-source project designed to help users find Electric Vehicle Charging Stations (EVCS) worldwide. The project leverages data from OpenChargeMap (OCM) to provide a comprehensive, easy-to-use platform for locating EV charging stations.

## Credits

- **Data Source**: The data for this project is sourced from [OpenChargeMap](https://github.com/openchargemap/ocm-export) and the [OpenChargeMap platform](https://openchargemap.org/), which provides global data on EV charging stations.
- **Project Type**: This is an open-source project under the MIT License.

## License Information

The data provided by OpenChargeMap is open-source but subject to specific usage terms and conditions. OpenChargeMap's data may be used in accordance with their [terms of use](https://openchargemap.org/site/terms) and license. Please ensure you are compliant with these terms when using this data.

For the software code and repository content, this project is licensed under the **MIT License**.

## Project Structure

The project is composed of the following services:

1. **evcsfinder-db**: MongoDB service that stores charging station data.
2. **evcsfinder-service**: A Flask-based backend service that exposes APIs to search and retrieve data from the MongoDB database.
3. **evcsfinder-app-dev**: React development frontend application for interacting with the EVCS data.
4. **evcsfinder-app-prod**: React production frontend application, served via NGINX.

### Backend Service (Flask)

The `evcsfinder-service` is a Flask-based backend API. It connects to MongoDB and allows the frontend to query the charging station data stored in the database.

### Frontend

The frontend is a React application, with separate setups for both development and production environments.

- **Development**: A React app running on port `3000` for easy development and debugging.
- **Production**: The app is bundled and served via NGINX on port `8080`.

## Running the Project

### Prerequisites

Ensure the following are installed before setting up the project:

- Docker
- Docker Compose

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/evcsfinder.git
   cd evcsfinder
2. Build and start the services:

Run the following command to start all the services defined in the docker-compose.yml:
docker-compose up --build
3. Access the services:

Frontend (Development): http://localhost:3000
Frontend (Production): http://localhost:8080
Backend API: http://localhost:5000

4. Database:

MongoDB is used to store the EV charging station data. The database can be accessed at the following URL:

MongoDB: mongodb://evcsfinder-db:27017/ev_charging

Data Directory
The charging station data is located in the ocm-data volume, which is populated from the OpenChargeMap export files (referencedata.json and country-specific files). When the Docker containers start, the data is imported into MongoDB.

API Endpoints
GET /stations: Fetch all charging stations.
GET /stations/{id}: Get details of a specific charging station by ID.
GET /search: Search for stations based on filters such as location, type, and availability.
Data Import from OpenChargeMap
The data from OpenChargeMap is provided as JSON files. These files contain detailed information about charging stations, metadata, and country references. The referencedata.json file is used to enrich the POI data with additional metadata (e.g., country, station type).

referencedata.json: Contains ID lookups for country codes, connection types, and other metadata fields.
Country folders: Each folder represents a country, named by its 2-digit ISO code (e.g., US, GB). These folders contain JSON files representing POIs (Points of Interest) for the charging stations in that country.
Project Workflow
Database: MongoDB stores the charging station data and serves it via the backend API.
Backend: The Flask service provides an API to search for charging stations.
Frontend: The React frontend enables users to search and view charging stations in an interactive UI.
Development Setup
For local development, Docker Compose will automatically set up the environment:

MongoDB: The database is configured with persistent storage.
Flask API: Backend service running on port 5000.
React Frontend: Development server running on port 3000.
Environment Variables
DATABASE_URL: The URL for the MongoDB service (e.g., mongodb://evcsfinder-db:27017/ev_charging).
React app uses REACT_APP_API_URL to point to the backend API (e.g., http://localhost:5000).

## Deployment
To deploy the application for production, use the following:

Build the production React app:

docker-compose up --build

## License
The code is available under the MIT License.

For the OpenChargeMap data, please refer to their terms of use and license.

## Acknowledgements
Data provided by OpenChargeMap and OpenChargeMap website.
Thanks to contributors and the OpenChargeMap community for providing detailed and global EV charging station data.
