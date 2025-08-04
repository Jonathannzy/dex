import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { 
  ArrowLeft, 
  Camera, 
  BookOpen, 
  Users, 
  MapPin,
  MessageCircle,
  Trophy,
  Zap,
  Tree,
  Mountain,
  Droplets,
  Flame
} from 'lucide-react';
import io from 'socket.io-client';

const PlanetExplorer = () => {
  const { planetId } = useParams();
  const navigate = useNavigate();
  const [socket, setSocket] = useState(null);
  const [planet, setPlanet] = useState(null);
  const [discoveries, setDiscoveries] = useState([]);
  const [currentDiscovery, setCurrentDiscovery] = useState(null);
  const [players, setPlayers] = useState([]);
  const [showDocumentation, setShowDocumentation] = useState(false);
  const [documentation, setDocumentation] = useState('');

  const planetData = {
    0: { name: 'Mercury', type: 'rocky', color: '#8B7355', features: ['craters', 'mountains', 'plains'] },
    1: { name: 'Venus', type: 'volcanic', color: '#FFA500', features: ['volcanoes', 'acid_rain', 'thick_atmosphere'] },
    2: { name: 'Earth', type: 'terrestrial', color: '#4B9CD3', features: ['oceans', 'continents', 'life'] },
    3: { name: 'Mars', type: 'desert', color: '#CD5C5C', features: ['canyons', 'dust_storms', 'polar_caps'] },
    4: { name: 'Jupiter', type: 'gas_giant', color: '#DAA520', features: ['storms', 'moons', 'rings'] },
    5: { name: 'Saturn', type: 'ringed', color: '#F4A460', features: ['rings', 'moons', 'storms'] },
    6: { name: 'Uranus', type: 'ice_giant', color: '#40E0D0', features: ['ice', 'moons', 'atmosphere'] },
    7: { name: 'Neptune', type: 'ice_giant', color: '#4169E1', features: ['storms', 'moons', 'wind'] }
  };

  const discoveryTypes = {
    craters: { icon: <Zap />, name: 'Impact Craters', description: 'Ancient meteorite impacts' },
    mountains: { icon: <Mountain />, name: 'Mountain Ranges', description: 'Tectonic formations' },
    plains: { icon: <MapPin />, name: 'Vast Plains', description: 'Flat terrain areas' },
    volcanoes: { icon: <Flame />, name: 'Active Volcanoes', description: 'Volcanic activity' },
    acid_rain: { icon: <Droplets />, name: 'Acid Rain', description: 'Corrosive precipitation' },
    thick_atmosphere: { icon: <Zap />, name: 'Dense Atmosphere', description: 'Heavy atmospheric pressure' },
    oceans: { icon: <Droplets />, name: 'Oceans', description: 'Large bodies of water' },
    continents: { icon: <Mountain />, name: 'Continents', description: 'Land masses' },
    life: { icon: <Tree />, name: 'Life Forms', description: 'Biological organisms' },
    canyons: { icon: <Mountain />, name: 'Deep Canyons', description: 'Erosional features' },
    dust_storms: { icon: <Zap />, name: 'Dust Storms', description: 'Atmospheric phenomena' },
    polar_caps: { icon: <Droplets />, name: 'Polar Ice Caps', description: 'Frozen regions' },
    storms: { icon: <Zap />, name: 'Atmospheric Storms', description: 'Weather systems' },
    moons: { icon: <MapPin />, name: 'Natural Satellites', description: 'Orbiting bodies' },
    rings: { icon: <Zap />, name: 'Planetary Rings', description: 'Orbital debris' },
    ice: { icon: <Droplets />, name: 'Ice Formations', description: 'Frozen compounds' },
    wind: { icon: <Zap />, name: 'High Winds', description: 'Atmospheric currents' }
  };

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);
    setPlanet(planetData[planetId]);

    newSocket.emit('joinPlanet', { planetId: parseInt(planetId) });

    newSocket.on('planetPlayers', (planetPlayers) => {
      setPlayers(planetPlayers);
    });

    newSocket.on('newDiscovery', (discovery) => {
      setDiscoveries(prev => [...prev, discovery]);
    });

    newSocket.on('planetDiscoveries', (planetDiscoveries) => {
      setDiscoveries(planetDiscoveries);
    });

    return () => {
      newSocket.emit('leavePlanet', { planetId: parseInt(planetId) });
      newSocket.close();
    };
  }, [planetId]);

  const makeDiscovery = () => {
    if (!planet) return;

    const availableFeatures = planet.features.filter(
      feature => !discoveries.some(d => d.type === feature)
    );

    if (availableFeatures.length === 0) return;

    const randomFeature = availableFeatures[Math.floor(Math.random() * availableFeatures.length)];
    const discovery = {
      id: Date.now(),
      type: randomFeature,
      discoveredBy: 'You',
      timestamp: new Date().toLocaleTimeString(),
      description: discoveryTypes[randomFeature].description
    };

    if (socket) {
      socket.emit('makeDiscovery', { planetId: parseInt(planetId), discovery });
    }
  };

  const documentDiscovery = (discovery) => {
    setCurrentDiscovery(discovery);
    setShowDocumentation(true);
  };

  const saveDocumentation = () => {
    if (currentDiscovery && documentation.trim()) {
      const updatedDiscovery = {
        ...currentDiscovery,
        documentation: documentation.trim()
      };

      if (socket) {
        socket.emit('updateDiscovery', { planetId: parseInt(planetId), discovery: updatedDiscovery });
      }

      setDiscoveries(prev => prev.map(d => 
        d.id === currentDiscovery.id ? updatedDiscovery : d
      ));

      setShowDocumentation(false);
      setDocumentation('');
      setCurrentDiscovery(null);
    }
  };

  const goBack = () => {
    navigate('/game');
  };

  if (!planet) return <div>Loading...</div>;

  return (
    <div className="planet-explorer">
      <div className="explorer-header">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={goBack}
          className="back-button"
        >
          <ArrowLeft size={20} />
          Back to Solar System
        </motion.button>

        <div className="planet-info">
          <h2>{planet.name}</h2>
          <p>{planet.type} planet</p>
          <div className="player-count">
            <Users size={16} />
            <span>{players.length} explorers here</span>
          </div>
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={makeDiscovery}
          className="discover-button"
          disabled={discoveries.length >= planet.features.length}
        >
          <Camera size={20} />
          Make Discovery
        </motion.button>
      </div>

      <div className="explorer-content">
        <div className="planet-view">
          <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
            <ambientLight intensity={0.3} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <Stars radius={50} depth={25} count={2000} factor={2} />
            
            <mesh>
              <sphereGeometry args={[2, 32, 32]} />
              <meshStandardMaterial color={planet.color} />
            </mesh>
            
            <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
          </Canvas>
        </div>

        <div className="discoveries-panel">
          <h3>Discoveries ({discoveries.length}/{planet.features.length})</h3>
          
          <div className="discoveries-list">
            {discoveries.map((discovery) => (
              <motion.div
                key={discovery.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="discovery-card"
              >
                <div className="discovery-header">
                  <div className="discovery-icon">
                    {discoveryTypes[discovery.type]?.icon}
                  </div>
                  <div className="discovery-info">
                    <h4>{discoveryTypes[discovery.type]?.name}</h4>
                    <p>{discovery.description}</p>
                    <small>Discovered by {discovery.discoveredBy} at {discovery.timestamp}</small>
                  </div>
                </div>
                
                {discovery.documentation && (
                  <div className="discovery-documentation">
                    <BookOpen size={16} />
                    <span>{discovery.documentation}</span>
                  </div>
                )}
                
                {!discovery.documentation && (
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => documentDiscovery(discovery)}
                    className="document-button"
                  >
                    <BookOpen size={16} />
                    Document
                  </motion.button>
                )}
              </motion.div>
            ))}
          </div>

          {discoveries.length === 0 && (
            <div className="no-discoveries">
              <Camera size={48} />
              <p>No discoveries yet. Start exploring!</p>
            </div>
          )}
        </div>
      </div>

      {showDocumentation && (
        <div className="documentation-modal">
          <div className="modal-content">
            <h3>Document Discovery</h3>
            <p>Document your findings about: {discoveryTypes[currentDiscovery?.type]?.name}</p>
            
            <textarea
              value={documentation}
              onChange={(e) => setDocumentation(e.target.value)}
              placeholder="Describe what you found..."
              rows={4}
            />
            
            <div className="modal-actions">
              <button onClick={() => setShowDocumentation(false)}>Cancel</button>
              <button onClick={saveDocumentation}>Save Documentation</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlanetExplorer;