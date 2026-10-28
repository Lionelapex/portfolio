import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './tailwind.css';
import './styles.css';
import Companions from './Companions';
import Atmosphere from './Atmosphere';

const ASSETS = `${import.meta.env.BASE_URL}assets/`;
const chapters = ['Home', 'About', 'Projects', 'Skills', 'Experience', 'Blog', 'CV', 'Contact'];
const chapterCopy = {
  About: 'The story behind the developer. This chapter is coming next.',
  Projects: 'A collection of things I’ve built. This chapter is coming next.',
  Skills: 'The tools and technologies in my backpack. This chapter is coming next.',
  Experience: 'The journey so far. This chapter is coming next.',
  Blog: 'Ideas, discoveries, and notes along the way. This chapter is coming next.',
  CV: 'My CV hasn’t been added yet. Check back when the next chapter is ready.',
  Contact: 'A place to start a conversation. Contact details will be added in the next chapter.',
  World: 'You’ve arrived at the beginning. The explorable world is the next chapter — for now, take in the view and say hello to my companion.',
};

function Icon({ name, ...props }) {
  const paths = {
    arrow: <><path d="M5 12h14M13 6l6 6-6 6" /></>,
    download: <><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5" /></>,
    file: <><path d="M14 2H5v20h14V7l-5-5Z" /><path d="M14 2v6h5M8 12h8M8 16h8" /></>,
    game: <><path d="M7 7h10c3 0 5 9 4 11-1 3-4-1-6-2H9c-2 1-5 5-6 2-1-2 1-11 4-11Z" /><path d="M6 11h6m-3-3v6m7-3h.01m3 3h.01" /></>,
    sun: <><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5" /></>,
    moon: <path d="M20.7 13A9 9 0 0 1 11 3.3 9 9 0 1 0 20.7 13Z" />,
    pause: <><path d="M8 5v14M16 5v14" /></>,
    play: <path d="m8 4 12 8-12 8V4Z" />,
    menu: <path d="M4 6h16M4 12h16M4 18h16" />,
    close: <path d="m6 6 12 12M6 18 18 6" />,
  };
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>{paths[name]}</svg>;
}

function useSavedPreference(key, fallback) {
  const [value, setValue] = useState(() => {
    try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
  });
  useEffect(() => { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* Storage is optional. */ } }, [key, value]);
  return [value, setValue];
}

function App() {
  const [night, setNight] = useSavedPreference('lionel-night', false);
  const [paused, setPaused] = useSavedPreference('lionel-paused', false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [chapter, setChapter] = useState(null);
  const [pet, setPet] = useState(false);
  const [layers, setLayers] = useState({});
  const dialog = useRef(null);
  const petTimer = useRef(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${ASSETS}layers.json`, { signal: controller.signal }).then(r => {
      if (!r.ok) throw new Error('Ambient layers unavailable');
      return r.json();
    }).then(setLayers).catch(() => {});
    return () => controller.abort();
  }, []);
  useEffect(() => {
    if (chapter && !dialog.current.open) dialog.current.showModal();
  }, [chapter]);
  useEffect(() => () => clearTimeout(petTimer.current), []);

  function openChapter(name) {
    setMenuOpen(false);
    if (name === 'Home') { document.getElementById('home').focus({ preventScroll: true }); return; }
    setChapter(name);
  }
  function closeChapter() { dialog.current.close(); setChapter(null); }
  function greetCompanion() {
    clearTimeout(petTimer.current);
    setPet(true);
    petTimer.current = setTimeout(() => setPet(false), 2400);
  }

  return <div className={`portfolio isolate ${night ? 'is-night' : ''} ${paused ? 'is-paused' : ''}`}>
    <a href="#home" className="skip-link">Skip to content</a>
    <main id="home" className="landing relative" tabIndex="-1">
      <div className="sky" aria-hidden="true" />
      <div className="night-stars" aria-hidden="true" />
      <div className="landscape" aria-hidden="true">
        <img className="landscape-base" src={`${ASSETS}landscape.webp`} width="2166" height="726" alt="" fetchPriority="high" />
        {Object.entries(layers).filter(([name]) => name === 'waterfall').map(([name, box]) => <div key={name} className={`ambient ambient-${name}`} style={{ left: `${box.left}%`, top: `${box.top}%`, width: `${box.width}%`, height: `${box.height}%`, backgroundImage: `url(${ASSETS}${name}.webp)` }} />)}
      </div>
      <Atmosphere />

      <header className="header">
        <a className="brand flex shrink-0 items-center motion-safe:animate-page-navigation" href="#home" aria-label="Lionel — home" onClick={() => setMenuOpen(false)}>
          <img src={`${ASSETS}avatar.webp`} width="47" height="53" alt="" />
          <span className="brand-copy"><span className="brand-name">LIONEL</span><span className="brand-tagline">DEVELOPER · CREATOR · PROBLEM SOLVER</span></span>
        </a>
        <nav id="main-navigation" className={`navigation motion-safe:animate-page-navigation [--entrance-delay:100ms] ${menuOpen ? 'is-open' : ''}`} aria-label="Main navigation">
          {chapters.map(name => <button key={name} className={`nav-link ${name === 'Home' ? 'active' : ''}`} aria-current={name === 'Home' ? 'page' : undefined} onClick={() => openChapter(name)}>{name}</button>)}
        </nav>
        <div className="header-tools flex items-center motion-safe:animate-page-navigation [--entrance-delay:160ms]">
          <button className="icon-button theme-toggle" onClick={() => setNight(!night)} aria-label={night ? 'Switch to day' : 'Switch to night'} aria-pressed={night} title={night ? 'Bring back the sunshine' : 'Stay a little after dark'}><Icon name={night ? 'sun' : 'moon'} /></button>
          <span className="tools-divider" />
          <button className="icon-button world-shortcut" onClick={() => openChapter('World')} aria-label="Explore my world" title="Explore my world"><Icon name="game" /></button>
          <button className="icon-button menu-toggle" aria-label={menuOpen ? 'Close navigation' : 'Open navigation'} aria-expanded={menuOpen} aria-controls="main-navigation" onClick={() => setMenuOpen(!menuOpen)}><Icon name={menuOpen ? 'close' : 'menu'} /></button>
        </div>
      </header>

      <section className="introduction" aria-labelledby="greeting">
        <p className="eyebrow motion-safe:animate-soft-reveal [--entrance-delay:1500ms]"><span /> A LITTLE CODE. A LITTLE CURIOSITY.</p>
        <h1 id="greeting"><span className="greeting-hi inline-block motion-safe:animate-greeting-hi [--entrance-delay:180ms]">Hi,</span>{' '}<span className="greeting-name inline-block motion-safe:animate-soft-reveal [--entrance-delay:1000ms]">I’m <span className="name-accent">Lionel</span></span><span className="pixel-period">.</span></h1>
        <p className="role motion-safe:animate-soft-reveal [--entrance-delay:1750ms]">Developer <span>/</span> Creator <span>/</span> Problem Solver</p>
        <p className="intro-copy motion-safe:animate-soft-reveal [--entrance-delay:2150ms]">I build practical solutions, explore new technologies,<br className="desktop-break" /> and turn ideas into working projects. Welcome to my<br className="desktop-break" /> corner of the internet.</p>
        <div className="hero-actions flex items-center motion-safe:animate-soft-reveal [--entrance-delay:2550ms]">
          <button className="button button-primary" onClick={() => openChapter('World')}><Icon name="game" /><span>Explore My World</span><Icon name="arrow" /></button>
          <button className="button button-secondary" onClick={() => openChapter('CV')}><Icon name="file" /><span>View My CV</span><Icon name="download" /></button>
        </div>
      </section>

      <Companions greeting={pet} onGreet={greetCompanion} />

      <button className="world-sign" onClick={() => openChapter('World')} aria-label="Explore my world — my journey, projects, and interests">
        <img src={`${ASSETS}sign.webp`} width="577" height="559" alt="" />
        <span className="sign-copy"><strong>EXPLORE MY WORLD</strong><span>A small interactive world<br />showcasing my journey,<br />projects and interests.</span><Icon name="arrow" /></span>
      </button>

     
    </main>

    <dialog ref={dialog} className="chapter-dialog" onCancel={closeChapter} onClose={() => setChapter(null)} onClick={event => { if (event.target === dialog.current) closeChapter(); }} aria-labelledby="chapter-title" aria-describedby="chapter-description">
      <button className="dialog-close icon-button" onClick={closeChapter} aria-label="Close dialog"><Icon name="close" /></button>
      <span className="chapter-label">THE ADVENTURE IS JUST BEGINNING</span>
      <Icon className="chapter-icon" name={chapter === 'CV' ? 'file' : 'game'} />
      <h2 id="chapter-title">{chapter === 'World' ? 'A world in the making.' : chapter === 'CV' ? 'CV coming soon.' : `${chapter}, coming soon.`}</h2>
      <p id="chapter-description">{chapterCopy[chapter]}</p>
      <button className="button button-primary" onClick={closeChapter}>Back to the view <Icon name="arrow" /></button>
    </dialog>
  </div>;
}

createRoot(document.getElementById('root')).render(<App />);
