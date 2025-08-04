import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Search, 
  Filter, 
  BookOpen, 
  Globe,
  Calendar,
  User,
  MapPin
} from 'lucide-react';
import io from 'socket.io-client';

const Documentation = () => {
  const navigate = useNavigate();
  const [socket, setSocket] = useState(null);
  const [allDiscoveries, setAllDiscoveries] = useState([]);
  const [filteredDiscoveries, setFilteredDiscoveries] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlanet, setSelectedPlanet] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  const planetNames = {
    0: 'Mercury',
    1: 'Venus', 
    2: 'Earth',
    3: 'Mars',
    4: 'Jupiter',
    5: 'Saturn',
    6: 'Uranus',
    7: 'Neptune'
  };

  const discoveryTypes = {
    craters: 'Impact Craters',
    mountains: 'Mountain Ranges',
    plains: 'Vast Plains',
    volcanoes: 'Active Volcanoes',
    acid_rain: 'Acid Rain',
    thick_atmosphere: 'Dense Atmosphere',
    oceans: 'Oceans',
    continents: 'Continents',
    life: 'Life Forms',
    canyons: 'Deep Canyons',
    dust_storms: 'Dust Storms',
    polar_caps: 'Polar Ice Caps',
    storms: 'Atmospheric Storms',
    moons: 'Natural Satellites',
    rings: 'Planetary Rings',
    ice: 'Ice Formations',
    wind: 'High Winds'
  };

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);

    newSocket.on('allDiscoveries', (discoveries) => {
      setAllDiscoveries(discoveries);
      setFilteredDiscoveries(discoveries);
    });

    newSocket.emit('requestAllDiscoveries');

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    let filtered = allDiscoveries;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(discovery => 
        discovery.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        discovery.discoveredBy.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (discovery.documentation && discovery.documentation.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by planet
    if (selectedPlanet !== 'all') {
      filtered = filtered.filter(discovery => discovery.planetId === parseInt(selectedPlanet));
    }

    // Filter by type
    if (selectedType !== 'all') {
      filtered = filtered.filter(discovery => discovery.type === selectedType);
    }

    // Sort discoveries
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.timestamp) - new Date(a.timestamp);
        case 'planet':
          return planetNames[a.planetId].localeCompare(planetNames[b.planetId]);
        case 'discoverer':
          return a.discoveredBy.localeCompare(b.discoveredBy);
        case 'type':
          return discoveryTypes[a.type].localeCompare(discoveryTypes[b.type]);
        default:
          return 0;
      }
    });

    setFilteredDiscoveries(filtered);
  }, [allDiscoveries, searchTerm, selectedPlanet, selectedType, sortBy]);

  const goBack = () => {
    navigate('/game');
  };

  const getPlanetColor = (planetId) => {
    const colors = {
      0: '#8B7355', // Mercury
      1: '#FFA500', // Venus
      2: '#4B9CD3', // Earth
      3: '#CD5C5C', // Mars
      4: '#DAA520', // Jupiter
      5: '#F4A460', // Saturn
      6: '#40E0D0', // Uranus
      7: '#4169E1'  // Neptune
    };
    return colors[planetId] || '#666';
  };

  return (
    <div className="documentation-container">
      <div className="documentation-header">
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
          <h1>Exploration Documentation</h1>
          <p>Complete record of all discoveries across the solar system</p>
        </div>
      </div>

      <div className="documentation-filters">
        <div className="search-section">
          <div className="search-input">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search discoveries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="filter-section">
          <div className="filter-group">
            <label>Planet:</label>
            <select 
              value={selectedPlanet} 
              onChange={(e) => setSelectedPlanet(e.target.value)}
            >
              <option value="all">All Planets</option>
              {Object.entries(planetNames).map(([id, name]) => (
                <option key={id} value={id}>{name}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Type:</label>
            <select 
              value={selectedType} 
              onChange={(e) => setSelectedType(e.target.value)}
            >
              <option value="all">All Types</option>
              {Object.entries(discoveryTypes).map(([key, name]) => (
                <option key={key} value={key}>{name}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Sort by:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="date">Date</option>
              <option value="planet">Planet</option>
              <option value="discoverer">Discoverer</option>
              <option value="type">Type</option>
            </select>
          </div>
        </div>
      </div>

      <div className="documentation-stats">
        <div className="stat-card">
          <Globe size={24} />
          <div>
            <h3>{allDiscoveries.length}</h3>
            <p>Total Discoveries</p>
          </div>
        </div>
        <div className="stat-card">
          <BookOpen size={24} />
          <div>
            <h3>{allDiscoveries.filter(d => d.documentation).length}</h3>
            <p>Documented</p>
          </div>
        </div>
        <div className="stat-card">
          <User size={24} />
          <div>
            <h3>{new Set(allDiscoveries.map(d => d.discoveredBy)).size}</h3>
            <p>Explorers</p>
          </div>
        </div>
      </div>

      <div className="discoveries-grid">
        {filteredDiscoveries.map((discovery) => (
          <motion.div
            key={discovery.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="discovery-document"
          >
            <div className="document-header">
              <div className="planet-indicator" style={{ backgroundColor: getPlanetColor(discovery.planetId) }}>
                <Globe size={16} />
              </div>
              <div className="discovery-meta">
                <h3>{discoveryTypes[discovery.type]}</h3>
                <p>on {planetNames[discovery.planetId]}</p>
              </div>
              <div className="discovery-date">
                <Calendar size={14} />
                <span>{new Date(discovery.timestamp).toLocaleDateString()}</span>
              </div>
            </div>

            <div className="discovery-content">
              <div className="discoverer-info">
                <User size={14} />
                <span>Discovered by {discovery.discoveredBy}</span>
              </div>
              
              {discovery.documentation && (
                <div className="documentation-text">
                  <BookOpen size={14} />
                  <p>{discovery.documentation}</p>
                </div>
              )}
            </div>

            <div className="document-footer">
              <span className="discovery-type">{discoveryTypes[discovery.type]}</span>
              {discovery.documentation && (
                <span className="documented-badge">Documented</span>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {filteredDiscoveries.length === 0 && (
        <div className="no-discoveries">
          <BookOpen size={48} />
          <h3>No discoveries found</h3>
          <p>Try adjusting your search criteria or explore more planets!</p>
        </div>
      )}
    </div>
  );
};

export default Documentation;