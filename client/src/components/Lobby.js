import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Rocket, Users, Globe, BookOpen, Trophy } from 'lucide-react';
import io from 'socket.io-client';

const Lobby = () => {
  const [playerName, setPlayerName] = useState('');
  const [socket, setSocket] = useState(null);
  const [players, setPlayers] = useState([]);
  const [gameStarted, setGameStarted] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);

    newSocket.on('playerJoined', (playerList) => {
      setPlayers(playerList);
    });

    newSocket.on('gameStarted', () => {
      setGameStarted(true);
      navigate('/game');
    });

    return () => newSocket.close();
  }, [navigate]);

  const joinGame = () => {
    if (playerName.trim() && socket) {
      socket.emit('joinGame', { name: playerName });
    }
  };

  const startGame = () => {
    if (socket) {
      socket.emit('startGame');
    }
  };

  return (
    <div className="lobby-container">
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="lobby-content"
      >
        <div className="game-title">
          <Rocket size={48} className="title-icon" />
          <h1>Cosmic Explorers</h1>
          <p>Multiplayer Planet Exploration Game</p>
        </div>

        <div className="lobby-form">
          <input
            type="text"
            placeholder="Enter your explorer name..."
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            className="player-name-input"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={joinGame}
            className="join-button"
            disabled={!playerName.trim()}
          >
            Join Expedition
          </motion.button>
        </div>

        <div className="players-list">
          <h3>Current Explorers ({players.length})</h3>
          <div className="players-grid">
            {players.map((player, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="player-card"
              >
                <Users size={20} />
                <span>{player.name}</span>
              </motion.div>
            ))}
          </div>
        </div>

        {players.length >= 2 && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={startGame}
            className="start-game-button"
          >
            Launch Expedition
          </motion.button>
        )}

        <div className="game-features">
          <div className="feature">
            <Globe size={24} />
            <span>Explore Unique Planets</span>
          </div>
          <div className="feature">
            <BookOpen size={24} />
            <span>Document Discoveries</span>
          </div>
          <div className="feature">
            <Trophy size={24} />
            <span>Compete with Others</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Lobby;