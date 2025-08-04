import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Send, Users, MessageCircle } from 'lucide-react';

const Chat = ({ socket }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [players, setPlayers] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
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

    return () => {
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

  return (
    <div className="chat-container">
      <div className="chat-header">
        <MessageCircle size={20} />
        <h3>Explorer Chat</h3>
        <div className="online-players">
          <Users size={16} />
          <span>{players.length} online</span>
        </div>
      </div>

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
              {message.text}
            </div>
          </motion.div>
        ))}
        
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="typing-indicator"
          >
            <span>Someone is typing...</span>
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
          placeholder="Type your message..."
          rows={2}
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={sendMessage}
          disabled={!newMessage.trim()}
          className="send-button"
        >
          <Send size={16} />
        </motion.button>
      </div>

      <div className="players-list">
        <h4>Online Explorers</h4>
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
                  on {player.currentPlanet}
                </span>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Chat;