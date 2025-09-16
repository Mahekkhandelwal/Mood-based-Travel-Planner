import React from 'react';
import './MoodSelector.css';

const moods = ['Adventure', 'Relaxing', 'Romantic', 'Cultural', 'Party'];

const MoodSelector = ({ onSelectMood }) => {
  return (
    <div className="mood-selector">
      <h2>Choose your mood to get a travel plan:</h2>
      <div className="mood-buttons">
        {moods.map((mood) => (
          <button 
            key={mood} 
            className="mood-button" 
            onClick={() => onSelectMood(mood.toLowerCase())}
          >
            {mood}
          </button>
        ))}
      </div>
    </div>
  );
};

export default MoodSelector;