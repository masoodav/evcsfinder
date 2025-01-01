// src/ApiConfig.js
const apiBaseUrl = process.env.REACT_APP_API_URL;

if (!apiBaseUrl) {
  console.warn('WARNING: The environment variable REACT_APP_API_URL is not set');
}

const ApiConfig = {
  status: apiBaseUrl ? `${apiBaseUrl}/status` : null, 
  search: apiBaseUrl ? `${apiBaseUrl}/stations/search` : null, 
  // Add more endpoints here as needed
};

export default ApiConfig;
