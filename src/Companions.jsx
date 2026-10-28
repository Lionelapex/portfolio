import React from 'react';

export default function Companions({ greeting, onGreet }) {
  return <button className={`companions ${greeting ? 'is-greeting' : ''}`}
    onClick={onGreet}
    aria-label="Say hello to Lionel and his dog" title="A little hello?">
    <span className="companion-sprite" aria-hidden="true" />
    <span className="companion-message" role="status">{greeting ? 'Hey, friend! ♥' : ''}</span>
  </button>;
}
