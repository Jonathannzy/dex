const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());

// Game state
let players = [];
let planets = [];
let allDiscoveries = [];
let planetDiscoveries = {};

  // Initialize Hitchhiker's Guide locations
  const initializePlanets = () => {
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

    planets = locationTypes.map((location, index) => ({
      ...location,
      id: index,
      discovered: false,
      discoveries: [],
      players: [],
      guideEntries: []
    }));

    // Initialize location discoveries
    for (let i = 0; i < planets.length; i++) {
      planetDiscoveries[i] = [];
    }
  };

// Initialize the game
initializePlanets();

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('New player connected:', socket.id);

  // Join game
  socket.on('joinGame', (data) => {
    const player = {
      id: socket.id,
      name: data.name,
      currentPlanet: null,
      discoveries: 0,
      documentations: 0,
      planetsExplored: 0,
      score: 0
    };

    players.push(player);
    
    // Broadcast updated player list
    io.emit('playerJoined', players);
    
    console.log(`Player ${data.name} joined the game`);
  });

  // Start game
  socket.on('startGame', () => {
    io.emit('gameStarted');
    console.log('Game started');
  });

  // Join planet
  socket.on('joinPlanet', (data) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      player.currentPlanet = data.planetId;
      
      // Add player to planet
      const planet = planets.find(p => p.id === data.planetId);
      if (planet && !planet.players.find(p => p.id === socket.id)) {
        planet.players.push(player);
      }

      // Send planet discoveries to player
      socket.emit('planetDiscoveries', planetDiscoveries[data.planetId] || []);
      
      // Broadcast player joined planet
      io.emit('playerJoinedPlanet', {
        planetId: data.planetId,
        player: player
      });

      console.log(`Player ${player.name} joined planet ${data.planetId}`);
    }
  });

  // Leave planet
  socket.on('leavePlanet', (data) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      player.currentPlanet = null;
      
      // Remove player from planet
      const planet = planets.find(p => p.id === data.planetId);
      if (planet) {
        planet.players = planet.players.filter(p => p.id !== socket.id);
      }

      // Broadcast player left planet
      io.emit('playerLeftPlanet', {
        planetId: data.planetId,
        playerId: socket.id
      });

      console.log(`Player ${player.name} left planet ${data.planetId}`);
    }
  });

  // Make discovery
  socket.on('makeDiscovery', (data) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      const discovery = {
        ...data.discovery,
        planetId: data.planetId,
        discoveredBy: player.name,
        timestamp: new Date().toISOString()
      };

      // Add to planet discoveries
      if (!planetDiscoveries[data.planetId]) {
        planetDiscoveries[data.planetId] = [];
      }
      planetDiscoveries[data.planetId].push(discovery);

      // Add to all discoveries
      allDiscoveries.push(discovery);

      // Update player stats
      player.discoveries++;
      player.score += 10;

      // Update planet
      const planet = planets.find(p => p.id === data.planetId);
      if (planet) {
        planet.discoveries.push(discovery);
        if (planet.discoveries.length >= 3) {
          planet.discovered = true;
        }
      }

      // Broadcast new discovery
      io.emit('newDiscovery', discovery);
      io.emit('planetUpdate', planets);
      io.emit('playerUpdate', players);

      console.log(`Player ${player.name} made discovery on planet ${data.planetId}`);
    }
  });

  // Update discovery
  socket.on('updateDiscovery', (data) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      // Update in planet discoveries
      const planetDisc = planetDiscoveries[data.planetId];
      if (planetDisc) {
        const index = planetDisc.findIndex(d => d.id === data.discovery.id);
        if (index !== -1) {
          planetDisc[index] = data.discovery;
        }
      }

      // Update in all discoveries
      const allDiscIndex = allDiscoveries.findIndex(d => d.id === data.discovery.id);
      if (allDiscIndex !== -1) {
        allDiscoveries[allDiscIndex] = data.discovery;
      }

      // Update player stats
      player.documentations++;
      player.score += 5;

      // Broadcast updates
      io.emit('planetUpdate', planets);
      io.emit('playerUpdate', players);

      console.log(`Player ${player.name} updated discovery on planet ${data.planetId}`);
    }
  });

  // Chat messages
  socket.on('sendMessage', (message) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      const chatMessage = {
        ...message,
        sender: player.name,
        timestamp: new Date().toLocaleTimeString()
      };

      io.emit('chatMessage', chatMessage);
      console.log(`Chat message from ${player.name}: ${message.text}`);
    }
  });

  // Typing indicator
  socket.on('typing', (data) => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      socket.broadcast.emit('playerTyping', {
        player: player.name,
        isTyping: data.isTyping
      });
    }
  });

  // Request all discoveries
  socket.on('requestAllDiscoveries', () => {
    socket.emit('allDiscoveries', allDiscoveries);
  });

  // Request leaderboard
  socket.on('requestLeaderboard', (data) => {
    let sortedPlayers = [...players];
    
    switch (data.category) {
      case 'discoveries':
        sortedPlayers.sort((a, b) => b.discoveries - a.discoveries);
        break;
      case 'documentation':
        sortedPlayers.sort((a, b) => b.documentations - a.documentations);
        break;
      case 'planets':
        sortedPlayers.sort((a, b) => b.planetsExplored - a.planetsExplored);
        break;
      case 'score':
        sortedPlayers.sort((a, b) => b.score - a.score);
        break;
      default:
        sortedPlayers.sort((a, b) => b.score - a.score);
    }

    socket.emit('leaderboardData', sortedPlayers);
  });

  // Disconnect
  socket.on('disconnect', () => {
    const player = players.find(p => p.id === socket.id);
    if (player) {
      // Remove player from current planet
      if (player.currentPlanet !== null) {
        const planet = planets.find(p => p.id === player.currentPlanet);
        if (planet) {
          planet.players = planet.players.filter(p => p.id !== socket.id);
        }
      }

      // Remove player from players list
      players = players.filter(p => p.id !== socket.id);
      
      // Broadcast updated player list
      io.emit('playerUpdate', players);
      
      console.log(`Player ${player.name} disconnected`);
    }
  });
});

// API Routes
app.get('/api/players', (req, res) => {
  res.json(players);
});

app.get('/api/planets', (req, res) => {
  res.json(planets);
});

app.get('/api/discoveries', (req, res) => {
  res.json(allDiscoveries);
});

app.get('/api/leaderboard', (req, res) => {
  const { category = 'score' } = req.query;
  let sortedPlayers = [...players];
  
  switch (category) {
    case 'discoveries':
      sortedPlayers.sort((a, b) => b.discoveries - a.discoveries);
      break;
    case 'documentation':
      sortedPlayers.sort((a, b) => b.documentations - a.documentations);
      break;
    case 'planets':
      sortedPlayers.sort((a, b) => b.planetsExplored - a.planetsExplored);
      break;
    case 'score':
    default:
      sortedPlayers.sort((a, b) => b.score - a.score);
  }
  
  res.json(sortedPlayers);
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    players: players.length, 
    planets: planets.length,
    discoveries: allDiscoveries.length 
  });
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
  console.log(`🚀 Cosmic Explorers Server running on port ${PORT}`);
  console.log(`📊 Game Stats:`);
  console.log(`   - Players: ${players.length}`);
  console.log(`   - Planets: ${planets.length}`);
  console.log(`   - Discoveries: ${allDiscoveries.length}`);
});