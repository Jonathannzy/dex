import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Ring } from '@react-three/drei';
import { motion } from 'framer-motion-3d';

const Planet = ({ planet, onClick, isSelected }) => {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005;
    }
  });

  const getPlanetTexture = (type) => {
    switch (type) {
      case 'rocky':
        return { roughness: 0.8, metalness: 0.1 };
      case 'volcanic':
        return { roughness: 0.6, metalness: 0.2 };
      case 'terrestrial':
        return { roughness: 0.3, metalness: 0.1 };
      case 'desert':
        return { roughness: 0.9, metalness: 0.05 };
      case 'gas_giant':
        return { roughness: 0.4, metalness: 0.3 };
      case 'ringed':
        return { roughness: 0.5, metalness: 0.2 };
      case 'ice_giant':
        return { roughness: 0.2, metalness: 0.4 };
      default:
        return { roughness: 0.5, metalness: 0.2 };
    }
  };

  const position = [
    planet.distance * Math.cos(planet.id * Math.PI / 4),
    0,
    planet.distance * Math.sin(planet.id * Math.PI / 4)
  ];

  return (
    <group position={position}>
      <motion.mesh
        ref={meshRef}
        scale={hovered || isSelected ? planet.size * 1.2 : planet.size}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
        onClick={onClick}
        whileHover={{ scale: planet.size * 1.2 }}
        whileTap={{ scale: planet.size * 0.9 }}
      >
        <Sphere args={[1, 32, 32]}>
          <meshStandardMaterial
            color={planet.color}
            {...getPlanetTexture(planet.type)}
          />
        </Sphere>
      </motion.mesh>

      {/* Rings for Saturn */}
      {planet.type === 'ringed' && (
        <Ring
          args={[1.5, 2.5, 64]}
          rotation={[Math.PI / 2, 0, 0]}
        >
          <meshStandardMaterial
            color="#F4A460"
            transparent
            opacity={0.6}
            side="double"
          />
        </Ring>
      )}

      {/* Planet label */}
      {hovered && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="planet-label"
          style={{
            position: 'absolute',
            top: '-30px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '12px',
            whiteSpace: 'nowrap',
            pointerEvents: 'none'
          }}
        >
          {planet.name}
        </motion.div>
      )}

      {/* Player indicators */}
      {planet.players.length > 0 && (
        <group position={[0, 1.5, 0]}>
          {planet.players.map((player, index) => (
            <mesh
              key={player.id}
              position={[
                Math.cos(index * Math.PI / 2) * 0.3,
                0,
                Math.sin(index * Math.PI / 2) * 0.3
              ]}
            >
              <sphereGeometry args={[0.1, 8, 8]} />
              <meshStandardMaterial color="#00ff00" />
            </mesh>
          ))}
        </group>
      )}
    </group>
  );
};

export default Planet;