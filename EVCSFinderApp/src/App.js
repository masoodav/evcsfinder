import React, { useState } from "react";
import axios from "axios";
import ApiConfig from "./ApiConfig";
import "./App.css"; // Import the CSS file

function App() {
  const [stations, setStations] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const searchStations = () => {
    setLoading(true);
    axios
      .get(ApiConfig.search, { params: { address: searchQuery } })
      .then((response) => {
        setStations(response.data);
        setLoading(false);
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error searching stations:", error);
        setLoading(false);
      });
  };

  return (
    <div className="app-container">
      <h1 className="title">EV Charger Finder</h1>
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by address"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <button onClick={searchStations} className="search-button">Search</button>
      </div>
      {loading ? (
        <div className="loader">Loading...</div>
      ) : (
        <ul className="stations-list">
          {stations.map((station) => (
            <li key={station.ID} className="station-item">
              <h3>{station.AddressInfo.Title}</h3>
              <p>Address: {station.AddressInfo.AddressLine1}, {station.AddressInfo.Town}, {station.AddressInfo.StateOrProvince}, {station.AddressInfo.Postcode}, {station.AddressInfo.CountryID}</p>
              <p>City: {station.AddressInfo.Town}</p>
              <p>Country: {station.AddressInfo.CountryID}</p>
              <p>Latitude: {station.AddressInfo.Latitude}</p>
              <p>Longitude: {station.AddressInfo.Longitude}</p>
              <p>Number of Points: {station.NumberOfPoints}</p>
              <p>Usage Cost: {station.UsageCost || "N/A"}</p>
              <p>General Comments: {station.GeneralComments || "None"}</p>
              <p>Connections:</p>
              <ul className="connections-list">
                {station.Connections.map((connection) => (
                  <li key={connection.ID} className="connection-item">
                    <p>Connection Type ID: {connection.ConnectionTypeID}</p>
                    <p>Current Type ID: {connection.CurrentTypeID}</p>
                    <p>Level ID: {connection.LevelID}</p>
                    <p>Power (kW): {connection.PowerKW}</p>
                    <p>Quantity: {connection.Quantity}</p>
                    <p>Status Type ID: {connection.StatusTypeID}</p>
                  </li>
                ))}
              </ul>
              <hr />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
