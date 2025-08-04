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
  Coffee,
  MessageCircle,
  Heart,
  Zap,
  Tree,
  Ship,
  Building,
  Utensils,
  Music,
  Cpu
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
  const [vogonEncounter, setVogonEncounter] = useState(false);

  const locationData = {
    0: { 
      name: 'Magrathea', 
      type: 'planet_factory', 
      color: '#8B4513', 
      features: ['planet_factory', 'underground_cities', 'slumbering_workers'],
      description: 'The legendary planet-building factory where worlds are crafted'
    },
    1: { 
      name: 'Vogon Homeworld', 
      type: 'bureaucratic', 
      color: '#556B2F', 
      features: ['bureaucracy_offices', 'paperwork_mountains', 'vogon_poetry'],
      description: 'Home of the bureaucratic Vogons and their paperwork'
    },
    2: { 
      name: 'Damogran', 
      type: 'tropical', 
      color: '#228B22', 
      features: ['guide_offices', 'tropical_beaches', 'babel_fish_pools'],
      description: 'Where the Hitchhiker\'s Guide was first conceived'
    },
    3: { 
      name: 'Vogon Constructor Fleet', 
      type: 'space_station', 
      color: '#696969', 
      features: ['constructor_ships', 'demolition_orders', 'bureaucratic_red_tape'],
      description: 'Floating bureaucratic nightmare in space'
    },
    4: { 
      name: 'Heart of Gold', 
      type: 'spaceship', 
      color: '#FFD700', 
      features: ['infinite_improbability_drive', 'tea_machine', 'marvin_android'],
      description: 'Ship with Infinite Improbability Drive'
    },
    5: { 
      name: 'Milliways', 
      type: 'restaurant', 
      color: '#FF6347', 
      features: ['restaurant_kitchen', 'time_viewing_windows', 'cosmic_cuisine'],
      description: 'The Restaurant at the End of the Universe'
    },
    6: { 
      name: 'Vogon Poetry Reading', 
      type: 'cultural_event', 
      color: '#8B0000', 
      features: ['poetry_podium', 'audience_seats', 'third_worst_poetry'],
      description: 'The third worst poetry in the universe'
    },
    7: { 
      name: 'Deep Thought', 
      type: 'computer', 
      color: '#4169E1', 
      features: ['computer_terminals', 'answer_calculation', 'seven_million_years'],
      description: 'The computer that calculated the answer to life'
    }
  };

  const discoveryTypes = {
    planet_factory: { icon: <Building />, name: 'Planet Factory', description: 'Where worlds are manufactured' },
    underground_cities: { icon: <Building />, name: 'Underground Cities', description: 'Slumbering workers in suspended animation' },
    slumbering_workers: { icon: <Users />, name: 'Slumbering Workers', description: 'Workers in deep sleep for millennia' },
    bureaucracy_offices: { icon: <Building />, name: 'Bureaucracy Offices', description: 'Endless paperwork and forms' },
    paperwork_mountains: { icon: <BookOpen />, name: 'Paperwork Mountains', description: 'Mountains of bureaucratic forms' },
    vogon_poetry: { icon: <Music />, name: 'Vogon Poetry', description: 'The third worst poetry in the universe' },
    guide_offices: { icon: <BookOpen />, name: 'Guide Offices', description: 'Where the Guide is compiled' },
    tropical_beaches: { icon: <Tree />, name: 'Tropical Beaches', description: 'Beautiful beaches of Damogran' },
    babel_fish_pools: { icon: <MessageCircle />, name: 'Babel Fish Pools', description: 'Universal translators swimming' },
    constructor_ships: { icon: <Ship />, name: 'Constructor Ships', description: 'Massive planet-destroying vessels' },
    demolition_orders: { icon: <Zap />, name: 'Demolition Orders', description: 'Official paperwork for planet destruction' },
    bureaucratic_red_tape: { icon: <BookOpen />, name: 'Bureaucratic Red Tape', description: 'Endless administrative procedures' },
    infinite_improbability_drive: { icon: <Zap />, name: 'Infinite Improbability Drive', description: 'Makes the impossible possible' },
    tea_machine: { icon: <Coffee />, name: 'Tea Machine', description: 'Produces the perfect cup of tea' },
    marvin_android: { icon: <Heart />, name: 'Marvin Android', description: 'Depressed robot with a brain the size of a planet' },
    restaurant_kitchen: { icon: <Utensils />, name: 'Restaurant Kitchen', description: 'Where cosmic cuisine is prepared' },
    time_viewing_windows: { icon: <Camera />, name: 'Time Viewing Windows', description: 'Watch the end of the universe' },
    cosmic_cuisine: { icon: <Utensils />, name: 'Cosmic Cuisine', description: 'Food from across the galaxy' },
    poetry_podium: { icon: <Music />, name: 'Poetry Podium', description: 'Where Vogon poetry is recited' },
    audience_seats: { icon: <Users />, name: 'Audience Seats', description: 'Seats for poetry victims' },
    third_worst_poetry: { icon: <Music />, name: 'Third Worst Poetry', description: 'The actual poetry being recited' },
    computer_terminals: { icon: <Cpu />, name: 'Computer Terminals', description: 'Deep Thought\'s interface' },
    answer_calculation: { icon: <Cpu />, name: 'Answer Calculation', description: 'The process of calculating 42' },
    seven_million_years: { icon: <Zap />, name: 'Seven Million Years', description: 'How long the calculation took' }
  };

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);
    setPlanet(locationData[planetId]);

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

    // Random Vogon encounter
    const vogonInterval = setInterval(() => {
      if (Math.random() < 0.15) { // 15% chance every 30 seconds
        setVogonEncounter(true);
        setTimeout(() => setVogonEncounter(false), 4000);
      }
    }, 30000);

    return () => {
      clearInterval(vogonInterval);
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
          Back to Galaxy
        </motion.button>

        <div className="planet-info">
          <h2>{planet.name}</h2>
          <p>{planet.description}</p>
          <div className="player-count">
            <Users size={16} />
            <span>{players.length} hitchhikers here</span>
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
          Add to Guide
        </motion.button>
      </div>

      {vogonEncounter && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className="vogon-encounter-alert"
        >
          <Music size={24} />
          <span>Vogon Poetry Reading in Progress!</span>
          <small>Cover your ears and hope for the best...</small>
        </motion.div>
      )}

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
          <h3>Guide Entries ({discoveries.length}/{planet.features.length})</h3>
          
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
                    <small>Added by {discovery.discoveredBy} at {discovery.timestamp}</small>
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
                    Write Guide Entry
                  </motion.button>
                )}
              </motion.div>
            ))}
          </div>

          {discoveries.length === 0 && (
            <div className="no-discoveries">
              <Camera size={48} />
              <p>No Guide entries yet. Start exploring!</p>
              <small>Remember: DON'T PANIC</small>
            </div>
          )}
        </div>
      </div>

      {showDocumentation && (
        <div className="documentation-modal">
          <div className="modal-content">
            <h3>Write Guide Entry</h3>
            <p>Contribute to the Guide about: {discoveryTypes[currentDiscovery?.type]?.name}</p>
            
            <textarea
              value={documentation}
              onChange={(e) => setDocumentation(e.target.value)}
              placeholder="Share your mostly harmless observations..."
              rows={4}
            />
            
            <div className="modal-actions">
              <button onClick={() => setShowDocumentation(false)}>Cancel</button>
              <button onClick={saveDocumentation}>Save to Guide</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlanetExplorer;