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
  Coffee,
  Heart,
  Zap
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
  const [guideEdition, setGuideEdition] = useState('42nd Edition');

  const locationNames = {
    0: 'Magrathea',
    1: 'Vogon Homeworld', 
    2: 'Damogran',
    3: 'Vogon Constructor Fleet',
    4: 'Heart of Gold',
    5: 'Milliways',
    6: 'Vogon Poetry Reading',
    7: 'Deep Thought'
  };

  const discoveryTypes = {
    planet_factory: 'Planet Factory',
    underground_cities: 'Underground Cities',
    slumbering_workers: 'Slumbering Workers',
    bureaucracy_offices: 'Bureaucracy Offices',
    paperwork_mountains: 'Paperwork Mountains',
    vogon_poetry: 'Vogon Poetry',
    guide_offices: 'Guide Offices',
    tropical_beaches: 'Tropical Beaches',
    babel_fish_pools: 'Babel Fish Pools',
    constructor_ships: 'Constructor Ships',
    demolition_orders: 'Demolition Orders',
    bureaucratic_red_tape: 'Bureaucratic Red Tape',
    infinite_improbability_drive: 'Infinite Improbability Drive',
    tea_machine: 'Tea Machine',
    marvin_android: 'Marvin Android',
    restaurant_kitchen: 'Restaurant Kitchen',
    time_viewing_windows: 'Time Viewing Windows',
    cosmic_cuisine: 'Cosmic Cuisine',
    poetry_podium: 'Poetry Podium',
    audience_seats: 'Audience Seats',
    third_worst_poetry: 'Third Worst Poetry',
    computer_terminals: 'Computer Terminals',
    answer_calculation: 'Answer Calculation',
    seven_million_years: 'Seven Million Years'
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
          return locationNames[a.planetId].localeCompare(locationNames[b.planetId]);
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

  const getLocationColor = (planetId) => {
    const colors = {
      0: '#8B4513', // Magrathea
      1: '#556B2F', // Vogon Homeworld
      2: '#228B22', // Damogran
      3: '#696969', // Vogon Constructor Fleet
      4: '#FFD700', // Heart of Gold
      5: '#FF6347', // Milliways
      6: '#8B0000', // Vogon Poetry Reading
      7: '#4169E1'  // Deep Thought
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
          Back to Galaxy
        </motion.button>

        <div className="header-content">
          <h1>The Hitchhiker's Guide to the Galaxy</h1>
          <div className="guide-edition">
            <BookOpen size={24} />
            <span>{guideEdition}</span>
          </div>
          <p>Complete repository of all knowledge and wisdom (mostly harmless)</p>
        </div>
      </div>

      <div className="guide-intro">
        <div className="guide-quote">
          <p>"The Hitchhiker's Guide to the Galaxy has already supplanted the great Encyclopedia Galactica as the standard repository of all knowledge and wisdom, for though it has many omissions and contains much that is apocryphal, or at least wildly inaccurate, it scores over the older, more pedestrian work in two important respects.</p>
          <p>First, it is slightly cheaper; and secondly, it has the words DON'T PANIC inscribed in large friendly letters on its cover."</p>
        </div>
      </div>

      <div className="documentation-filters">
        <div className="search-section">
          <div className="search-input">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search Guide entries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="filter-section">
          <div className="filter-group">
            <label>Location:</label>
            <select 
              value={selectedPlanet} 
              onChange={(e) => setSelectedPlanet(e.target.value)}
            >
              <option value="all">All Locations</option>
              {Object.entries(locationNames).map(([id, name]) => (
                <option key={id} value={id}>{name}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Entry Type:</label>
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
              <option value="planet">Location</option>
              <option value="discoverer">Contributor</option>
              <option value="type">Entry Type</option>
            </select>
          </div>
        </div>
      </div>

      <div className="documentation-stats">
        <div className="stat-card">
          <Globe size={24} />
          <div>
            <h3>{allDiscoveries.length}</h3>
            <p>Guide Entries</p>
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
            <p>Contributors</p>
          </div>
        </div>
        <div className="stat-card">
          <Heart size={24} />
          <div>
            <h3>42</h3>
            <p>The Answer</p>
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
              <div className="planet-indicator" style={{ backgroundColor: getLocationColor(discovery.planetId) }}>
                <Globe size={16} />
              </div>
              <div className="discovery-meta">
                <h3>{discoveryTypes[discovery.type]}</h3>
                <p>at {locationNames[discovery.planetId]}</p>
              </div>
              <div className="discovery-date">
                <Calendar size={14} />
                <span>{new Date(discovery.timestamp).toLocaleDateString()}</span>
              </div>
            </div>

            <div className="discovery-content">
              <div className="discoverer-info">
                <User size={14} />
                <span>Contributed by {discovery.discoveredBy}</span>
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
                <span className="documented-badge">Guide Entry Complete</span>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {filteredDiscoveries.length === 0 && (
        <div className="no-discoveries">
          <BookOpen size={48} />
          <h3>No Guide entries found</h3>
          <p>Try adjusting your search criteria or explore more locations!</p>
          <small>Remember: DON'T PANIC</small>
        </div>
      )}

      <div className="guide-footer">
        <div className="guide-disclaimer">
          <Coffee size={20} />
          <div>
            <h4>Guide Disclaimer</h4>
            <p>This Guide contains many omissions and much that is apocryphal, or at least wildly inaccurate. However, it is slightly cheaper than the Encyclopedia Galactica and has the words DON'T PANIC inscribed in large friendly letters on its cover.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Documentation;