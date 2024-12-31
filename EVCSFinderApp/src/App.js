import React, { useEffect, useState } from "react";
import axios from "axios";
import ApiConfig from "./ApiConfig";

function App() {
  const [stations, setStations] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true); // Initially set to true to show loading on first render

  useEffect(() => {
    if (!ApiConfig.search) {
      console.error("API URL for search is not set.");
      return;
    }
  }, []);


  const fetchStations = () => {
    setLoading(true);
    axios
      .get(ApiConfig.search)
      .then((response) => {
        setStations(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error searching stations:", error);
        setLoading(false);
      });
  };

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
    <div>
      <h1>EV Charger Finder</h1>
      <div>
        <input
          type="text"
          placeholder="Search by address, city, or country"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={searchStations}>Search</button>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {stations.map((station) => (
            station.location && station.location.lat && station.location.lng ? (
              <div key={station._id}>
                <h3>{station.name}</h3>
                <p>Location: {station.location.lat}, {station.location.lng}</p>
              </div>
            ) : (
              <div key={station._id}>
                <h3>{station.name}</h3>
                <p>Location data unavailable</p>
              </div>
            )
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
