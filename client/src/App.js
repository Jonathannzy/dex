import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import './App.css';

// Game Components
import Lobby from './components/Lobby';
import Game from './components/Game';
import PlanetExplorer from './components/PlanetExplorer';
import Documentation from './components/Documentation';
import Leaderboard from './components/Leaderboard';

function App() {
  return (
    <Router>
      <div className="App">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Routes>
            <Route path="/" element={<Lobby />} />
            <Route path="/game" element={<Game />} />
            <Route path="/explore/:planetId" element={<PlanetExplorer />} />
            <Route path="/documentation" element={<Documentation />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
          </Routes>
        </motion.div>
      </div>
    </Router>
  );
}

export default App;
