# EVCSFinder

**EVCSFinder** is an open-source project aimed at helping users find Electric Vehicle Charging Stations (EVCS) worldwide. The platform leverages data from **OpenChargeMap (OCM)** to provide a comprehensive and easy-to-use solution for locating EV charging stations.

## Credits

- **Data Source**: The data for this project is sourced from [OpenChargeMap](https://github.com/openchargemap/ocm-export) and the [OpenChargeMap platform](https://openchargemap.org/), which provides global data on EV charging stations.

## License Information

The data provided by OpenChargeMap is open-source, but it is subject to specific usage terms and conditions. You may use OpenChargeMap's data in accordance with their [terms of use](https://openchargemap.org/site/terms) and license. Please ensure compliance with these terms when using the data.

## Project Type 
This is an academic project to demonstrate a microservice-based application architecture for EV charging station discovery.

## Project Structure

The project consists of the following services:

1. **evcsfinder-db**: MongoDB service for storing charging station data.
2. **evcsfinder-service**: Flask-based backend service that provides APIs to search and retrieve data from MongoDB.
3. **evcsfinder-app**: React frontend application for interacting with the EVCS data.

### Backend Service (Flask)

The `evcsfinder-service` is a Flask-based backend API. It connects to the MongoDB database and allows the frontend to query and retrieve charging station data.

### Frontend

The frontend is built using **React** and serves as the user interface to interact with the EV charging station data.

## Running the Project

### Prerequisites

Prerequisites
Before setting up the project, ensure that Docker Desktop is installed. Docker Desktop includes everything you need to build and run containerized applications, along with Docker Compose and Kubernetes (for local development and orchestration). This project has been tested with Windows and Git Bash.

### Setup Instructions
#### Development setup using Docker Compose
For local development, Docker Compose sets up the following environment:

MongoDB: Database with persistent storage.
Flask API: Backend service running on port 5000.
React Frontend: Development server running on port 3000.
1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/evcsfinder.git
   cd evcsfinder
Build and start the services:

2. **Run the following command to build and start all the services defined in docker-compose.yml:**

bash
Copy code
FORCE_LOAD=true docker-compose up --build
FORCE_LOAD=true: This flag will instruct the evcsfinder-db container to clone the OpenChargeMap Export Repository and load the data into the MongoDB database.
Subsequent Runs: If the database is already loaded (after the first run), you can set FORCE_LOAD=false to skip reloading the data.
This feature allows you to reload data whenever new OpenChargeMap data is available.

3. **Access the services:**

Frontend: Visit the React application at http://localhost:3000
Backend API: Access the Flask-based API at http://localhost:5000

MongoDB is used to store the EV charging station data.

#### Deployment using Kubernetes
The application is deployed using Kubernetes. The evcsfinder deployment manifests are provided in the EVCSFinderDeployment directory.

To Deploy the Application:
1. **Run the following command to start the Kubernetes deployment:**

bash
./evcs-deploy-control.sh start

2. **Access the services:**
Frontend: Visit the React application at http://localhost:3000
Backend API: Access the Flask-based API at http://localhost:5000
   
3.**To Stop the Kubernetes Cluster:**

bash
./evcs-deploy-control.sh stop
This script automates the deployment and shutdown process of the Kubernetes cluster for the EVCSFinder application.

### Acknowledgements
The data from OpenChargeMap is provided as JSON files. These files contain detailed information about charging stations, including metadata and country references.
Data Provided by: OpenChargeMap.
Thanks to OpenChargeMap community for providing detailed and global EV charging station data.

