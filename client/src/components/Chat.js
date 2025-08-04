import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Send, Users, MessageCircle, Fish, Music, Coffee } from 'lucide-react';

const Chat = ({ socket }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [players, setPlayers] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [babelFishStatus, setBabelFishStatus] = useState('active');
  const [vogonWarning, setVogonWarning] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!socket) return;

    socket.on('chatMessage', (message) => {
      setMessages(prev => [...prev, message]);
    });

    socket.on('playerTyping', (data) => {
      setIsTyping(data.isTyping);
    });

    socket.on('playerList', (playerList) => {
      setPlayers(playerList);
    });

    // Random Babel Fish malfunctions
    const babelInterval = setInterval(() => {
      if (Math.random() < 0.08) { // 8% chance every 30 seconds
        setBabelFishStatus('malfunctioning');
        setTimeout(() => setBabelFishStatus('active'), 5000);
      }
    }, 30000);

    // Random Vogon poetry warnings
    const vogonInterval = setInterval(() => {
      if (Math.random() < 0.05) { // 5% chance every 30 seconds
        setVogonWarning(true);
        setTimeout(() => setVogonWarning(false), 3000);
      }
    }, 30000);

    return () => {
      clearInterval(babelInterval);
      clearInterval(vogonInterval);
      socket.off('chatMessage');
      socket.off('playerTyping');
      socket.off('playerList');
    };
  }, [socket]);

  const sendMessage = () => {
    if (newMessage.trim() && socket) {
      const message = {
        id: Date.now(),
        text: newMessage.trim(),
        sender: 'You',
        timestamp: new Date().toLocaleTimeString(),
        type: 'message'
      };

      socket.emit('sendMessage', message);
      setNewMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleTyping = () => {
    if (socket) {
      socket.emit('typing', { isTyping: true });
      setTimeout(() => {
        socket.emit('typing', { isTyping: false });
      }, 1000);
    }
  };

  const getBabelFishStatusText = () => {
    switch (babelFishStatus) {
      case 'active':
        return 'Babel Fish Universal Translator Active';
      case 'malfunctioning':
        return 'Babel Fish Malfunctioning - Translation May Be Inaccurate';
      default:
        return 'Babel Fish Status Unknown';
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="babel-fish-status">
          <Fish size={16} />
          <span className={babelFishStatus}>{getBabelFishStatusText()}</span>
        </div>
        <div className="chat-title">
          <MessageCircle size={20} />
          <h3>Babel Fish Chat</h3>
        </div>
        <div className="online-players">
          <Users size={16} />
          <span>{players.length} hitchhikers online</span>
        </div>
      </div>

      {vogonWarning && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="vogon-warning"
        >
          <Music size={16} />
          <span>⚠️ Vogon Poetry Detected Nearby ⚠️</span>
        </motion.div>
      )}

      <div className="chat-messages">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`message ${message.sender === 'You' ? 'own-message' : 'other-message'}`}
          >
            <div className="message-header">
              <span className="message-sender">{message.sender}</span>
              <span className="message-time">{message.timestamp}</span>
            </div>
            <div className="message-content">
              {babelFishStatus === 'malfunctioning' && message.sender !== 'You' ? (
                <span className="translated-text">
                  [Translated]: {message.text.split('').reverse().join('')}
                </span>
              ) : (
                message.text
              )}
            </div>
          </motion.div>
        ))}
        
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="typing-indicator"
          >
            <span>Someone is composing a message...</span>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <textarea
          value={newMessage}
          onChange={(e) => {
            setNewMessage(e.target.value);
            handleTyping();
          }}
          onKeyPress={handleKeyPress}
          placeholder={babelFishStatus === 'malfunctioning' ? 
            "Babel Fish malfunctioning - type carefully..." : 
            "Type your message (Babel Fish will translate)..."
          }
          rows={2}
          disabled={babelFishStatus === 'malfunctioning'}
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={sendMessage}
          disabled={!newMessage.trim() || babelFishStatus === 'malfunctioning'}
          className="send-button"
        >
          <Send size={16} />
        </motion.button>
      </div>

      <div className="players-list">
        <h4>Online Hitchhikers</h4>
        <div className="players">
          {players.map((player, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="player-item"
            >
              <div className="player-avatar">
                {player.name.charAt(0).toUpperCase()}
              </div>
              <span className="player-name">{player.name}</span>
              {player.currentPlanet && (
                <span className="player-location">
                  at {player.currentPlanet}
                </span>
              )}
              <span className="player-status">Mostly Harmless</span>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="chat-footer">
        <div className="guide-reminder">
          <Coffee size={14} />
          <span>Remember: Always carry a towel</span>
        </div>
        <div className="panic-reminder">
          <span>DON'T PANIC</span>
        </div>
      </div>
    </div>
  );
};

export default Chat;