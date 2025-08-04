import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { 
  Globe, 
  Users, 
  BookOpen, 
  Coffee, 
  Home,
  MessageCircle,
  Heart,
  Zap,
  Ship
} from 'lucide-react';
import io from 'socket.io-client';
import Planet from './Planet';
import Chat from './Chat';

const Game = () => {
  const [socket, setSocket] = useState(null);
  const [players, setPlayers] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [planets, setPlanets] = useState([]);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [showChat, setShowChat] = useState(false);
  const [infiniteProbability, setInfiniteProbability] = useState(false);
  const navigate = useNavigate();

  // Generate Hitchhiker's Guide locations
  const generateLocations = () => {
    const locationTypes = [
      { name: 'Magrathea', type: 'planet_factory', color: '#8B4513', size: 1.8, distance: 2, description: 'The legendary planet-building factory' },
      { name: 'Vogon Homeworld', type: 'bureaucratic', color: '#556B2F', size: 1.2, distance: 3, description: 'Home of the bureaucratic Vogons' },
      { name: 'Damogran', type: 'tropical', color: '#228B22', size: 1.5, distance: 4, description: 'Where the Guide was first conceived' },
      { name: 'Vogon Constructor Fleet', type: 'space_station', color: '#696969', size: 2.0, distance: 5, description: 'Floating bureaucratic nightmare' },
      { name: 'Heart of Gold', type: 'spaceship', color: '#FFD700', size: 1.0, distance: 6, description: 'Ship with Infinite Improbability Drive' },
      { name: 'Milliways', type: 'restaurant', color: '#FF6347', size: 1.3, distance: 7, description: 'The Restaurant at the End of the Universe' },
      { name: 'Vogon Poetry Reading', type: 'cultural_event', color: '#8B0000', size: 0.8, distance: 8, description: 'The third worst poetry in the universe' },
      { name: 'Deep Thought', type: 'computer', color: '#4169E1', size: 1.6, distance: 9, description: 'The computer that calculated the answer to life' }
    ];

    return locationTypes.map((location, index) => ({
      ...location,
      id: index,
      discovered: false,
      discoveries: [],
      players: [],
      guideEntries: []
    }));
  };

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);
    setPlanets(generateLocations());

    newSocket.on('playerUpdate', (playerList) => {
      setPlayers(playerList);
    });

    newSocket.on('planetUpdate', (updatedPlanets) => {
      setPlanets(updatedPlanets);
    });

    newSocket.on('playerJoinedPlanet', (data) => {
      setPlanets(prev => prev.map(planet => 
        planet.id === data.planetId 
          ? { ...planet, players: [...planet.players, data.player] }
          : planet
      ));
    });

    newSocket.on('playerLeftPlanet', (data) => {
      setPlanets(prev => prev.map(planet => 
        planet.id === data.planetId 
          ? { ...planet, players: planet.players.filter(p => p.id !== data.playerId) }
          : planet
      ));
    });

    // Infinite Improbability Drive effect
    const improbabilityInterval = setInterval(() => {
      if (Math.random() < 0.05) { // 5% chance every 30 seconds
        setInfiniteProbability(true);
        setTimeout(() => setInfiniteProbability(false), 3000);
      }
    }, 30000);

    return () => {
      clearInterval(improbabilityInterval);
      newSocket.close();
    };
  }, []);

  const exploreLocation = (planetId) => {
    if (socket) {
      socket.emit('explorePlanet', { planetId });
      navigate(`/explore/${planetId}`);
    }
  };

  const goToDocumentation = () => {
    navigate('/documentation');
  };

  const goToLeaderboard = () => {
    navigate('/leaderboard');
  };

  const goToLobby = () => {
    navigate('/');
  };

  return (
    <div className="game-container">
      <div className="game-header">
        <div className="header-left">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToLobby}
            className="header-button"
          >
            <Home size={20} />
            Guide Lobby
          </motion.button>
        </div>
        
        <div className="header-center">
          <h2>The Hitchhiker's Guide to the Galaxy</h2>
          <div className="player-count">
            <Users size={16} />
            <span>{players.length} Hitchhikers Online</span>
          </div>
          <div className="guide-motto">
            <span>DON'T PANIC</span>
          </div>
        </div>

        <div className="header-right">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowChat(!showChat)}
            className="header-button"
          >
            <MessageCircle size={20} />
            Babel Fish Chat
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToDocumentation}
            className="header-button"
          >
            <BookOpen size={20} />
            Guide Entries
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToLeaderboard}
            className="header-button"
          >
            <Heart size={20} />
            Guide Rankings
          </motion.button>
        </div>
      </div>

      {infiniteProbability && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className="infinite-probability-alert"
        >
          <Zap size={24} />
          <span>Infinite Improbability Drive Activated!</span>
          <small>You may experience some temporal anomalies...</small>
        </motion.div>
      )}

      <div className="game-content">
        <div className="galaxy-view">
          <Canvas camera={{ position: [0, 5, 15], fov: 60 }}>
            <ambientLight intensity={0.3} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <Stars radius={100} depth={50} count={5000} factor={4} />
            
            {planets.map((planet, index) => (
              <Planet
                key={planet.id}
                planet={planet}
                onClick={() => exploreLocation(planet.id)}
                isSelected={selectedPlanet?.id === planet.id}
              />
            ))}
            
            <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
          </Canvas>
        </div>

        <div className="locations-panel">
          <h3>Galactic Destinations</h3>
          <div className="locations-list">
            {planets.map((planet) => (
              <motion.div
                key={planet.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`location-card ${planet.discovered ? 'discovered' : ''}`}
                onClick={() => exploreLocation(planet.id)}
              >
                <div className="location-info">
                  <Globe size={24} color={planet.color} />
                  <div>
                    <h4>{planet.name}</h4>
                    <p>{planet.description}</p>
                    <small>{planet.players.length} hitchhikers</small>
                  </div>
                </div>
                <div className="location-status">
                  {planet.discovered ? (
                    <span className="discovered-badge">Guide Entry Complete</span>
                  ) : (
                    <span className="undiscovered-badge">Unexplored</span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {showChat && (
          <div className="chat-panel">
            <Chat socket={socket} />
          </div>
        )}
      </div>

      <div className="guide-footer">
        <div className="guide-stats">
          <div className="stat">
            <span className="stat-number">42</span>
            <span className="stat-label">The Answer</span>
          </div>
          <div className="stat">
            <span className="stat-number">{planets.filter(p => p.discovered).length}</span>
            <span className="stat-label">Guide Entries</span>
          </div>
          <div className="stat">
            <span className="stat-number">{players.length}</span>
            <span className="stat-label">Mostly Harmless</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Game;