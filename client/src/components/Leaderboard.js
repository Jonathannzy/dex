import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Trophy, 
  Medal, 
  Star, 
  Users, 
  Globe,
  BookOpen,
  TrendingUp
} from 'lucide-react';
import io from 'socket.io-client';

const Leaderboard = () => {
  const navigate = useNavigate();
  const [socket, setSocket] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('discoveries');
  const [timeFrame, setTimeFrame] = useState('all');

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);

    newSocket.on('leaderboardData', (data) => {
      setLeaderboard(data);
    });

    newSocket.emit('requestLeaderboard', { category: selectedCategory, timeFrame });

    return () => newSocket.close();
  }, [selectedCategory, timeFrame]);

  const goBack = () => {
    navigate('/game');
  };

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1:
        return <Trophy size={24} color="#FFD700" />;
      case 2:
        return <Medal size={24} color="#C0C0C0" />;
      case 3:
        return <Medal size={24} color="#CD7F32" />;
      default:
        return <Star size={20} color="#666" />;
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'discoveries':
        return <Globe size={20} />;
      case 'documentation':
        return <BookOpen size={20} />;
      case 'planets':
        return <Globe size={20} />;
      case 'score':
        return <TrendingUp size={20} />;
      default:
        return <Trophy size={20} />;
    }
  };

  const getCategoryTitle = (category) => {
    switch (category) {
      case 'discoveries':
        return 'Most Discoveries';
      case 'documentation':
        return 'Best Documenters';
      case 'planets':
        return 'Planet Explorers';
      case 'score':
        return 'Overall Score';
      default:
        return 'Leaderboard';
    }
  };

  const getCategoryDescription = (category) => {
    switch (category) {
      case 'discoveries':
        return 'Players with the most discoveries across all planets';
      case 'documentation':
        return 'Players who documented the most discoveries';
      case 'planets':
        return 'Players who explored the most planets';
      case 'score':
        return 'Overall ranking based on all achievements';
      default:
        return 'Top performers in the solar system';
    }
  };

  return (
    <div className="leaderboard-container">
      <div className="leaderboard-header">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={goBack}
          className="back-button"
        >
          <ArrowLeft size={20} />
          Back to Game
        </motion.button>

        <div className="header-content">
          <h1>Explorer Leaderboard</h1>
          <p>Top performers in the solar system</p>
        </div>
      </div>

      <div className="leaderboard-controls">
        <div className="category-selector">
          <label>Category:</label>
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="discoveries">Most Discoveries</option>
            <option value="documentation">Best Documenters</option>
            <option value="planets">Planet Explorers</option>
            <option value="score">Overall Score</option>
          </select>
        </div>

        <div className="timeframe-selector">
          <label>Time Frame:</label>
          <select 
            value={timeFrame} 
            onChange={(e) => setTimeFrame(e.target.value)}
          >
            <option value="all">All Time</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="today">Today</option>
          </select>
        </div>
      </div>

      <div className="category-info">
        <div className="category-icon">
          {getCategoryIcon(selectedCategory)}
        </div>
        <div>
          <h2>{getCategoryTitle(selectedCategory)}</h2>
          <p>{getCategoryDescription(selectedCategory)}</p>
        </div>
      </div>

      <div className="leaderboard-list">
        {leaderboard.map((player, index) => (
          <motion.div
            key={player.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`leaderboard-item ${index < 3 ? 'top-three' : ''}`}
          >
            <div className="rank-section">
              <div className="rank-icon">
                {getRankIcon(index + 1)}
              </div>
              <div className="rank-number">
                #{index + 1}
              </div>
            </div>

            <div className="player-section">
              <div className="player-avatar">
                {player.name.charAt(0).toUpperCase()}
              </div>
              <div className="player-info">
                <h3>{player.name}</h3>
                <p>{player.title || 'Explorer'}</p>
              </div>
            </div>

            <div className="stats-section">
              <div className="stat-item">
                <Globe size={16} />
                <span>{player.discoveries || 0} discoveries</span>
              </div>
              <div className="stat-item">
                <BookOpen size={16} />
                <span>{player.documentations || 0} documented</span>
              </div>
              <div className="stat-item">
                <Globe size={16} />
                <span>{player.planetsExplored || 0} planets</span>
              </div>
            </div>

            <div className="score-section">
              <div className="score-value">
                {selectedCategory === 'discoveries' && player.discoveries}
                {selectedCategory === 'documentation' && player.documentations}
                {selectedCategory === 'planets' && player.planetsExplored}
                {selectedCategory === 'score' && player.score}
              </div>
              <div className="score-label">
                {selectedCategory === 'discoveries' && 'discoveries'}
                {selectedCategory === 'documentation' && 'documented'}
                {selectedCategory === 'planets' && 'planets'}
                {selectedCategory === 'score' && 'points'}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {leaderboard.length === 0 && (
        <div className="no-leaderboard">
          <Trophy size={48} />
          <h3>No data available</h3>
          <p>Start exploring to see your ranking!</p>
        </div>
      )}

      <div className="achievement-info">
        <h3>How to climb the leaderboard:</h3>
        <div className="achievement-tips">
          <div className="tip">
            <Globe size={20} />
            <div>
              <h4>Make Discoveries</h4>
              <p>Explore planets and discover new features</p>
            </div>
          </div>
          <div className="tip">
            <BookOpen size={20} />
            <div>
              <h4>Document Findings</h4>
              <p>Write detailed documentation of your discoveries</p>
            </div>
          </div>
          <div className="tip">
            <Globe size={20} />
            <div>
              <h4>Explore Multiple Planets</h4>
              <p>Visit different planets to increase your score</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;