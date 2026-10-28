import React from 'react';

const leaves = [
  { left: '21%', drift: '-8cqw', cycle: '28s', delay: '0s', size: '19px', sway: '4.2s', sprite: 1 },
  { left: '43%', drift: '-12cqw', cycle: '32s', delay: '5s', size: '14px', sway: '5.1s', sprite: 2 },
  { left: '69%', drift: '-10cqw', cycle: '30s', delay: '10s', size: '17px', sway: '4.7s', sprite: 3 },
  { left: '89%', drift: '-15cqw', cycle: '34s', delay: '16s', size: '21px', sway: '5.6s', sprite: 4 },
  { left: '98%', drift: '-12cqw', cycle: '29s', delay: '22s', size: '15px', sway: '4.5s', sprite: 5 },
];

export default function Atmosphere() {
  return <div className="atmosphere" aria-hidden="true">
    {leaves.map((leaf, index) => <div key={`leaf-${index}`} className="leaf-fall" style={{ left: leaf.left, '--drift': leaf.drift, '--cycle': leaf.cycle, '--delay': leaf.delay, '--leaf-size': leaf.size, '--sway': leaf.sway }}>
      <img className="leaf-sway" src={`/assets/leaf-${leaf.sprite}.webp`} alt="" draggable="false" />
    </div>)}
    {[{ top: '17%', delay: '5s' }, { top: '21%', delay: '6.2s' }, { top: '18.5%', delay: '7.1s' }].map((bird, index) => <div key={`bird-${index}`} className="bird-flight" style={{ top: bird.top, '--delay': bird.delay }}>
      <span className="bird-wings" />
    </div>)}
  </div>;
}
