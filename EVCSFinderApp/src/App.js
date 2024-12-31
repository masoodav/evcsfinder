import React, { useState } from "react";
import axios from "axios";
import ApiConfig from "./ApiConfig";
import "./App.css"; // Import the CSS file

function App() {
  const [stations, setStations] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);

  const searchStations = () => {
    setLoading(true);
    setSearchPerformed(true);
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
          {searchPerformed && stations.length === 0 && (
            <p>No stations found.</p>
          )}
          {stations.map((station) => (
            <li key={station.ID} className="station-item">
              <h3>{station.AddressInfo.Title}</h3>
              <p>Address: {station.AddressInfo.AddressLine1}, {station.AddressInfo.Town}, {station.AddressInfo.StateOrProvince}, {station.AddressInfo.Postcode}, {station.AddressInfo.Country}</p>
              <p>City: {station.AddressInfo.Town}</p>
              <p>Country: {station.AddressInfo.Country}</p>
              <p>Latitude: {station.AddressInfo.Latitude}</p>
              <p>Longitude: {station.AddressInfo.Longitude}</p>
              <p>Number of Points: {station.NumberOfPoints}</p>
              <p>Usage Cost: {station.UsageCost || "N/A"}</p>
              <p>General Comments: {station.GeneralComments || "None"}</p>
              {station.MediaItems && station.MediaItems.length > 0 && (
                <div>
                  <h4>Image:</h4>
                  <img src={station.MediaItems[0].ItemThumbnailURL} alt="Station Thumbnail" className="station-image" />
                </div>
              )}
              <p>Connections:</p>
              {station.Connections && station.Connections.length > 0 ? (
                <ul className="connections-list">
                  {station.Connections.map((connection) => (
                    <li key={connection.ID} className="connection-item">
                      <p>Connection Type: {connection.ConnectionType}</p>
                      <p>Current Type: {connection.CurrentType}</p>
                      <p>Power (kW): {connection.PowerKW}</p>
                      <p>Quantity: {connection.Quantity}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No connections available.</p>
              )}
              <hr />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
