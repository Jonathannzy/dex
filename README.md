# 🌌 Cosmic Explorers - Multiplayer Planet Exploration Game

A real-time multiplayer game where players explore different planets in the solar system, make discoveries, document their findings, and compete with other explorers.

## 🚀 Features

### Multiplayer Experience
- **Real-time multiplayer**: Join with friends and explore together
- **Live chat system**: Communicate with other explorers
- **Player tracking**: See who's exploring which planets
- **Synchronized discoveries**: All players see discoveries in real-time

### Planet Exploration
- **8 Unique Planets**: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
- **3D Solar System**: Interactive 3D visualization using Three.js
- **Planet-specific features**: Each planet has unique discoverable features
- **Real-time exploration**: Click planets to explore them individually

### Discovery System
- **Multiple discovery types**: Craters, mountains, volcanoes, oceans, life forms, and more
- **Documentation system**: Write detailed descriptions of your findings
- **Discovery tracking**: Keep track of all discoveries across planets
- **Collaborative exploration**: Work together to discover all features

### Game Features
- **Leaderboard system**: Compete for top spots in various categories
- **Achievement tracking**: Monitor your exploration progress
- **Documentation library**: Browse all discoveries and documentation
- **Real-time updates**: See new discoveries as they happen

## 🛠️ Technology Stack

### Frontend
- **React 17**: Modern UI framework
- **Three.js**: 3D graphics and visualization
- **React Three Fiber**: React bindings for Three.js
- **Socket.IO Client**: Real-time communication
- **Framer Motion**: Smooth animations
- **Lucide React**: Beautiful icons

### Backend
- **Node.js**: Server runtime
- **Express**: Web framework
- **Socket.IO**: Real-time bidirectional communication
- **CORS**: Cross-origin resource sharing

## 📦 Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cosmic-explorers
   ```

2. **Install server dependencies**
   ```bash
   cd server
   npm install
   ```

3. **Install client dependencies**
   ```bash
   cd ../client
   npm install
   ```

## 🎮 Running the Game

### Start the Server
```bash
cd server
npm start
```
The server will start on `http://localhost:3001`

### Start the Client
```bash
cd client
npm start
```
The client will start on `http://localhost:3000`

### Development Mode
For development with auto-restart:
```bash
# Server (in server directory)
npm run dev

# Client (in client directory)
npm start
```

## 🎯 How to Play

### Getting Started
1. Open your browser and go to `http://localhost:3000`
2. Enter your explorer name in the lobby
3. Wait for other players to join (minimum 2 players recommended)
4. Click "Launch Expedition" to start the game

### Exploring Planets
1. **Solar System View**: See all planets in 3D space
2. **Click a Planet**: Navigate to explore a specific planet
3. **Make Discoveries**: Click "Make Discovery" to find new features
4. **Document Findings**: Write detailed descriptions of your discoveries
5. **Collaborate**: Work with other players to discover everything

### Game Mechanics
- **Discovery Points**: Earn points for each discovery (10 points)
- **Documentation Points**: Earn points for documenting discoveries (5 points)
- **Planet Completion**: Discover all features on a planet to mark it as "explored"
- **Leaderboard**: Compete for top positions in various categories

### Features by Planet
- **Mercury**: Craters, mountains, plains
- **Venus**: Volcanoes, acid rain, thick atmosphere
- **Earth**: Oceans, continents, life forms
- **Mars**: Canyons, dust storms, polar caps
- **Jupiter**: Storms, moons, rings
- **Saturn**: Rings, moons, storms
- **Uranus**: Ice formations, moons, atmosphere
- **Neptune**: Storms, moons, high winds

## 🏆 Leaderboard Categories

- **Most Discoveries**: Players with the highest number of discoveries
- **Best Documenters**: Players who documented the most discoveries
- **Planet Explorers**: Players who explored the most planets
- **Overall Score**: Combined ranking based on all achievements

## 📱 Features

### Real-time Communication
- **Live Chat**: Communicate with other explorers
- **Typing Indicators**: See when someone is typing
- **Player Status**: Know who's online and where they are

### Documentation System
- **Search Functionality**: Find specific discoveries
- **Filtering Options**: Filter by planet, discovery type, or date
- **Sorting**: Sort by various criteria
- **Statistics**: View overall game statistics

### 3D Visualization
- **Interactive Solar System**: Rotate, zoom, and pan the 3D view
- **Planet Details**: Each planet has unique appearance and features
- **Player Indicators**: See other players exploring the same planet
- **Discovery Markers**: Visual indicators for discoveries

## 🔧 API Endpoints

### Server API
- `GET /api/players` - Get all online players
- `GET /api/planets` - Get all planets and their states
- `GET /api/discoveries` - Get all discoveries
- `GET /api/leaderboard?category=score` - Get leaderboard data
- `GET /health` - Server health check

### Socket.IO Events
- `joinGame` - Player joins the game
- `startGame` - Game starts
- `joinPlanet` - Player joins a planet
- `leavePlanet` - Player leaves a planet
- `makeDiscovery` - Player makes a discovery
- `updateDiscovery` - Player updates discovery documentation
- `sendMessage` - Send chat message
- `typing` - Typing indicator

## 🎨 Customization

### Adding New Planets
1. Update the `planetTypes` array in `server/server.js`
2. Add planet features in `client/src/components/PlanetExplorer.js`
3. Update discovery types in the documentation component

### Modifying Discovery Types
1. Update `discoveryTypes` in `client/src/components/PlanetExplorer.js`
2. Add corresponding icons and descriptions
3. Update the server-side planet features

### Styling
- Main styles are in `client/src/App.css`
- Uses CSS custom properties for easy theming
- Responsive design for mobile and desktop

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
- Check if port 3001 is available
- Ensure all dependencies are installed
- Check Node.js version (v14+ required)

**Client won't connect to server**
- Verify server is running on port 3001
- Check browser console for CORS errors
- Ensure both client and server are running

**3D graphics not working**
- Check browser WebGL support
- Update graphics drivers
- Try a different browser

**Socket connection issues**
- Check firewall settings
- Verify network connectivity
- Restart both client and server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

- **Three.js** for 3D graphics
- **Socket.IO** for real-time communication
- **React** for the UI framework
- **Framer Motion** for animations
- **Lucide** for beautiful icons

---

**Happy Exploring! 🚀✨**