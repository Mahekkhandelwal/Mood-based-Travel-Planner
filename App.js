// src/App.js

import React from 'react';
import MoodSelector from './components/MoodSelector';
import './App.css';

function App() {
  const handleMoodSelect = (mood) => {
    const url = `http://localhost:5000/plan?mood=${mood}`;
    window.open(url, '_blank');
  };

  return (
    <div className="App">
      <main className="main-content"> {/* This is the new div */}
        <MoodSelector onSelectMood={handleMoodSelect} />
      </main>
    </div>
  );
}

export default App;