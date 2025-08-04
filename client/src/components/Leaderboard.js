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
  TrendingUp,
  Heart,
  Coffee,
  Fish
} from 'lucide-react';
import io from 'socket.io-client';

const Leaderboard = () => {
  const navigate = useNavigate();
  const [socket, setSocket] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('discoveries');
  const [timeFrame, setTimeFrame] = useState('all');
  const [answerToLife, setAnswerToLife] = useState(42);

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
        return 'Most Guide Entries';
      case 'documentation':
        return 'Best Guide Contributors';
      case 'planets':
        return 'Galactic Travelers';
      case 'score':
        return 'Overall Guide Rating';
      default:
        return 'Guide Rankings';
    }
  };

  const getCategoryDescription = (category) => {
    switch (category) {
      case 'discoveries':
        return 'Hitchhikers with the most Guide entries across all locations';
      case 'documentation':
        return 'Contributors who wrote the most detailed Guide entries';
      case 'planets':
        return 'Hitchhikers who visited the most locations';
      case 'score':
        return 'Overall ranking based on all Guide contributions';
      default:
        return 'Top contributors to the Guide';
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
          Back to Galaxy
        </motion.button>

        <div className="header-content">
          <h1>Guide Contributor Rankings</h1>
          <div className="answer-to-life">
            <span>The Answer to Life, the Universe, and Everything: {answerToLife}</span>
          </div>
          <p>Top contributors to the Hitchhiker's Guide</p>
        </div>
      </div>

      <div className="leaderboard-controls">
        <div className="category-selector">
          <label>Category:</label>
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="discoveries">Most Guide Entries</option>
            <option value="documentation">Best Contributors</option>
            <option value="planets">Galactic Travelers</option>
            <option value="score">Overall Rating</option>
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
                <p>{player.title || 'Mostly Harmless Hitchhiker'}</p>
              </div>
            </div>

            <div className="stats-section">
              <div className="stat-item">
                <Globe size={16} />
                <span>{player.discoveries || 0} Guide entries</span>
              </div>
              <div className="stat-item">
                <BookOpen size={16} />
                <span>{player.documentations || 0} documented</span>
              </div>
              <div className="stat-item">
                <Globe size={16} />
                <span>{player.planetsExplored || 0} locations</span>
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
                {selectedCategory === 'discoveries' && 'entries'}
                {selectedCategory === 'documentation' && 'contributions'}
                {selectedCategory === 'planets' && 'locations'}
                {selectedCategory === 'score' && 'points'}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {leaderboard.length === 0 && (
        <div className="no-leaderboard">
          <Trophy size={48} />
          <h3>No Guide contributors yet</h3>
          <p>Start exploring to see your ranking!</p>
          <small>Remember: DON'T PANIC</small>
        </div>
      )}

      <div className="achievement-info">
        <h3>How to climb the Guide rankings:</h3>
        <div className="achievement-tips">
          <div className="tip">
            <Globe size={20} />
            <div>
              <h4>Add Guide Entries</h4>
              <p>Explore locations and add entries to the Guide</p>
            </div>
          </div>
          <div className="tip">
            <BookOpen size={20} />
            <div>
              <h4>Write Detailed Entries</h4>
              <p>Document your findings with detailed descriptions</p>
            </div>
          </div>
          <div className="tip">
            <Globe size={20} />
            <div>
              <h4>Visit Multiple Locations</h4>
              <p>Explore different places across the galaxy</p>
            </div>
          </div>
          <div className="tip">
            <Coffee size={20} />
            <div>
              <h4>Always Carry a Towel</h4>
              <p>Essential for any self-respecting hitchhiker</p>
            </div>
          </div>
        </div>
      </div>

      <div className="guide-footer">
        <div className="guide-stats">
          <div className="stat">
            <Fish size={20} />
            <span>Babel Fish Universal Translator Active</span>
          </div>
          <div className="stat">
            <Heart size={20} />
            <span>Mostly Harmless</span>
          </div>
          <div className="stat">
            <span className="panic-text">DON'T PANIC</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;