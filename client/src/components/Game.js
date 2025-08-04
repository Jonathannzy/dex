import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { 
  Globe, 
  Users, 
  BookOpen, 
  Trophy, 
  Home,
  MessageCircle,
  Settings
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
  const navigate = useNavigate();

  // Generate planets data
  const generatePlanets = () => {
    const planetTypes = [
      { name: 'Mercury', type: 'rocky', color: '#8B7355', size: 0.8, distance: 2 },
      { name: 'Venus', type: 'volcanic', color: '#FFA500', size: 1.2, distance: 3 },
      { name: 'Earth', type: 'terrestrial', color: '#4B9CD3', size: 1.5, distance: 4 },
      { name: 'Mars', type: 'desert', color: '#CD5C5C', size: 1.0, distance: 5 },
      { name: 'Jupiter', type: 'gas_giant', color: '#DAA520', size: 2.5, distance: 7 },
      { name: 'Saturn', type: 'ringed', color: '#F4A460', size: 2.2, distance: 9 },
      { name: 'Uranus', type: 'ice_giant', color: '#40E0D0', size: 1.8, distance: 11 },
      { name: 'Neptune', type: 'ice_giant', color: '#4169E1', size: 1.7, distance: 13 }
    ];

    return planetTypes.map((planet, index) => ({
      ...planet,
      id: index,
      discovered: false,
      discoveries: [],
      players: []
    }));
  };

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);
    setPlanets(generatePlanets());

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

    return () => newSocket.close();
  }, []);

  const explorePlanet = (planetId) => {
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
            Lobby
          </motion.button>
        </div>
        
        <div className="header-center">
          <h2>Solar System Explorer</h2>
          <div className="player-count">
            <Users size={16} />
            <span>{players.length} Explorers Online</span>
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
            Chat
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToDocumentation}
            className="header-button"
          >
            <BookOpen size={20} />
            Docs
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToLeaderboard}
            className="header-button"
          >
            <Trophy size={20} />
            Leaderboard
          </motion.button>
        </div>
      </div>

      <div className="game-content">
        <div className="solar-system">
          <Canvas camera={{ position: [0, 5, 15], fov: 60 }}>
            <ambientLight intensity={0.3} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <Stars radius={100} depth={50} count={5000} factor={4} />
            
            {planets.map((planet, index) => (
              <Planet
                key={planet.id}
                planet={planet}
                onClick={() => explorePlanet(planet.id)}
                isSelected={selectedPlanet?.id === planet.id}
              />
            ))}
            
            <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
          </Canvas>
        </div>

        <div className="planets-panel">
          <h3>Available Planets</h3>
          <div className="planets-list">
            {planets.map((planet) => (
              <motion.div
                key={planet.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`planet-card ${planet.discovered ? 'discovered' : ''}`}
                onClick={() => explorePlanet(planet.id)}
              >
                <div className="planet-info">
                  <Globe size={24} color={planet.color} />
                  <div>
                    <h4>{planet.name}</h4>
                    <p>{planet.type}</p>
                    <small>{planet.players.length} explorers</small>
                  </div>
                </div>
                <div className="planet-status">
                  {planet.discovered ? (
                    <span className="discovered-badge">Explored</span>
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
    </div>
  );
};

export default Game;