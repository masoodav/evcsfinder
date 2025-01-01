#!/bin/bash


# Define YAML file paths
BACKEND_DEPLOYMENT="backend-deployment.yaml"
BACKEND_SERVICE="backend-service.yaml"
DB_DEPLOYMENT="db-deployment.yaml"
DB_SERVICE="db-service.yaml"
FRONTEND_DEPLOYMENT="frontend-deployment.yaml"
FRONTEND_SERVICE="frontend-service.yaml"

# Function to start the services
start() {
  echo "Starting backend, db, and frontend services..."

  kubectl apply -f $BACKEND_DEPLOYMENT
  kubectl apply -f $BACKEND_SERVICE
  kubectl apply -f $DB_DEPLOYMENT
  kubectl apply -f $DB_SERVICE
  kubectl apply -f $FRONTEND_DEPLOYMENT
  kubectl apply -f $FRONTEND_SERVICE

  echo "Services started successfully."
}

# Function to stop the services
stop() {
  echo "Stopping backend, db, and frontend services..."

  kubectl delete -f $BACKEND_DEPLOYMENT
  kubectl delete -f $BACKEND_SERVICE
  kubectl delete -f $DB_DEPLOYMENT
  kubectl delete -f $DB_SERVICE
  kubectl delete -f $FRONTEND_DEPLOYMENT
  kubectl delete -f $FRONTEND_SERVICE

  echo "Services stopped successfully."
}

# Check the argument and decide to start or stop
case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac
