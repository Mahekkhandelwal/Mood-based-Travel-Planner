import React from 'react';
import './TripDisplay.css';

const TripDisplay = ({ data }) => {
  if (!data) return null;

  const { destination, weather, attractions, hotels, itinerary } = data;

  return (
    <div className="trip-display">
      <h2>Your Trip to {destination}</h2>
      <div className="trip-sections">
        <div className="section">
          <h3>Weather</h3>
          <p>{weather.temperature}, {weather.condition}</p>
        </div>
        <div className="section">
          <h3>Top Attractions</h3>
          <ul>
            {attractions.map((attraction, index) => (
              <li key={index}>{attraction.name}</li>
            ))}
          </ul>
        </div>
        <div className="section">
          <h3>Hotel Suggestions</h3>
          <ul>
            {hotels.map((hotel, index) => (
              <li key={index}>{hotel.name}</li>
            ))}
          </ul>
        </div>
        <div className="section">
          <h3>Sample Itinerary</h3>
          <ul>
            {itinerary.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TripDisplay;