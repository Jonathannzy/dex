import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BookOpen, Users, Globe, Coffee, Heart, Zap } from 'lucide-react';
import io from 'socket.io-client';

const Lobby = () => {
  const [playerName, setPlayerName] = useState('');
  const [socket, setSocket] = useState(null);
  const [players, setPlayers] = useState([]);
  const [gameStarted, setGameStarted] = useState(false);
  const [vogonPoetry, setVogonPoetry] = useState(false);
  const navigate = useNavigate();

  const vogonPoems = [
    "Oh freddled gruntbuggly, thy micturations are to me as plurdled gabbleblotchits on a lurgid bee.",
    "Groop, I implore thee, my foonting turlingdromes, and hooptiously drangle me with crinkly bindlewurdles.",
    "Or I will rend thee in the gobberwarts with my blurglecruncheon, see if I don't!"
  ];

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

    // Random Vogon poetry trigger
    const poetryInterval = setInterval(() => {
      if (Math.random() < 0.1) { // 10% chance every 30 seconds
        setVogonPoetry(true);
        setTimeout(() => setVogonPoetry(false), 5000);
      }
    }, 30000);

    return () => {
      clearInterval(poetryInterval);
      newSocket.close();
    };
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

  const getRandomVogonPoem = () => {
    return vogonPoems[Math.floor(Math.random() * vogonPoems.length)];
  };

  return (
    <div className="lobby-container">
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="lobby-content"
      >
        <div className="guide-title">
          <BookOpen size={48} className="title-icon" />
          <h1>The Hitchhiker's Guide to the Galaxy</h1>
          <div className="don-t-panic">
            <span className="panic-text">DON'T PANIC</span>
          </div>
          <p>Multiplayer Edition - A Mostly Harmless Adventure</p>
        </div>

        <div className="guide-info">
          <div className="guide-quote">
            <p>"The Hitchhiker's Guide to the Galaxy has already supplanted the great Encyclopedia Galactica as the standard repository of all knowledge and wisdom, for though it has many omissions and contains much that is apocryphal, or at least wildly inaccurate, it scores over the older, more pedestrian work in two important respects.</p>
            <p>First, it is slightly cheaper; and secondly, it has the words DON'T PANIC inscribed in large friendly letters on its cover."</p>
          </div>
        </div>

        <div className="lobby-form">
          <div className="babel-fish-section">
            <div className="babel-fish">
              <span>🐟</span>
              <small>Babel Fish Universal Translator Active</small>
            </div>
          </div>
          
          <input
            type="text"
            placeholder="Enter your hitchhiker name..."
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
            <Heart size={20} />
            Join the Guide
          </motion.button>
        </div>

        <div className="players-list">
          <h3>Current Hitchhikers ({players.length})</h3>
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
                <small>Mostly Harmless</small>
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
            <Zap size={20} />
            Begin Your Journey Through Space and Time
          </motion.button>
        )}

        <div className="game-features">
          <div className="feature">
            <Globe size={24} />
            <span>Explore the Galaxy</span>
          </div>
          <div className="feature">
            <BookOpen size={24} />
            <span>Contribute to the Guide</span>
          </div>
          <div className="feature">
            <Coffee size={24} />
            <span>Find the Perfect Cup of Tea</span>
          </div>
        </div>

        <div className="guide-tips">
          <h4>Essential Guide Tips:</h4>
          <ul>
            <li>Always carry a towel</li>
            <li>The answer to life, the universe, and everything is 42</li>
            <li>Avoid Vogon poetry at all costs</li>
            <li>Remember: DON'T PANIC</li>
          </ul>
        </div>
      </motion.div>

      {vogonPoetry && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          className="vogon-poetry-modal"
        >
          <div className="vogon-poetry-content">
            <h3>⚠️ VOGON POETRY ALERT ⚠️</h3>
            <p className="vogon-poem">{getRandomVogonPoem()}</p>
            <small>This is the third worst poetry in the universe</small>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Lobby;