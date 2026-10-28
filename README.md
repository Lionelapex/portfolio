# Lionel Chapasuka

I study Computer Science at the University of the People and work as a developer at LJ Tutors. This repository is my personal site, and it is also where I keep the projects I have built outside coursework. Most of them started as small irritations in my own workflow that I wanted to fix: a converter that kept breaking my equations, a finance tracker I could not find in a form I liked, a voice agent I wanted to understand from the inside.

The site is built in chapters rather than pages. Chapter one is the landing scene: a pixel art landscape with a character, a dog, a wooden sign, and a waterfall that runs across the width of the screen. Later chapters turn the same scene into somewhere you can walk, so the projects, notes, and background end up as places in a world instead of a long scroll of cards.

## What is finished so far

The landing page works and is what you see today. The panorama crops to the viewport instead of stretching, so it stays sharp on a phone and on a wide monitor while the character, dog, and sign keep their own placement. A toggle switches the scene between day and night by relighting the same artwork.

The introduction arrives in stages: a greeting first, then my name, then the role, the paragraph, and the buttons, spread across roughly four seconds. If your system asks for reduced motion, all of it appears at once. Leaves fall on staggered cycles and a small flock of birds crosses the sky. The pause control stops both of them along with the rest of the motion on the page.

The wooden sign carries real text instead of lettering painted into the image, so screen readers can read it. Sections that are not built yet open a short explanation rather than a dead link.

## Projects

The list below is the public work. Live links are included where the deployment is still running.

### Featured projects

- [latex-to-word](https://github.com/Lionelapex/latex-to-word) converts ChatGPT and LaTeX output into Word documents and keeps the equations editable instead of flattening them into pictures.
- [Retro Pokédex](https://github.com/Lionelapex/Retro-Pok-dex) is a pixel art Pokédex where you can search for a Pokémon, compare two sets of stats side by side, and switch between the normal and shiny sprites. There is a [live demo](https://lionelapex.github.io/Retro-Pok-dex/).
- [Realtime Voice Receptionist](https://github.com/Lionelapex/realtime-voice-receptionist) is a browser voice agent that holds a receptionist style conversation in real time.
- [Taste Haven](https://github.com/Lionelapex/Taste-haven-website) is a restaurant site with the menu, services, and online ordering laid out for phones and desktops. There is a [live demo](https://lionelapex.github.io/Taste-haven-website/).

### Web applications

- [Personal Finance Tracker](https://github.com/Lionelapex/Personal-Finance-Tracker) records income and spending and breaks the totals down by category. There is a [live demo](https://lionelapex.github.io/Personal-Finance-Tracker/).
- [Email Notification](https://github.com/Lionelapex/EMAIL-NOTIFICATION) is a scheduled notification flow built around email delivery.
- [Rock Paper Crossblades](https://github.com/Lionelapex/Rock-paper-crossblades) is a themed take on rock paper scissors from The Odin Project. There is a [live demo](https://lionelapex.github.io/Rock-paper-crossblades/).

### Smaller builds

- [Calculator](https://github.com/Lionelapex/calculator) was an excuse to practise DOM work and styling, so the design is louder than it needs to be. There is a [live demo](https://lionelapex.github.io/calculator/).
- [ToBinaryConvertor](https://github.com/Lionelapex/ToBinaryConvertor) turns decimal numbers into binary without a framework. There is a [live demo](https://lionelapex.github.io/ToBinaryConvertor/).
- [Etch-to-Sketch](https://github.com/Lionelapex/Etch-to-sketch) is a drawing grid I built while learning event handling.
- [Interactive Card Component](https://github.com/Lionelapex/Interactive-card-component) is a layout and state exercise.
- [Web Development Resources](https://github.com/Lionelapex/web-development-resources) collects the links I end up sending to people who are starting out.

Some client and commercial work sits in private repositories, and I can walk through it on request.

## How the site is put together

The interface is React 19 on Vite 7. Tailwind 4 is loaded through `@tailwindcss/vite` without Preflight, so the site keeps its own reset and spacing while I still get the utilities in markup.

The scene itself is plain CSS. The panorama, overlays, and character anchors are positioned in the artwork's own coordinates, 2166 by 726 for the background, and then scaled with the viewport. That is easier to reason about than a pile of utility classes once several layers have to line up.

Assets are prepared with Python and Pillow. The script crops the ambient layers to their combined bounds, pulls the blank sign out through a silhouette mask because the source image has a checkerboard baked into it, and realigns the waterfall strips onto the rock face before it cuts the atlas.

## Repository layout

```
index.html                  Entry document
vite.config.js              Vite and Tailwind plugin configuration
src/
  main.jsx                  Application entry
  App.jsx                   Landing scene composition
  Atmosphere.jsx            Leaves, birds, and motion controls
  Companions.jsx            Character, dog, and sign interactions
  styles.css                Scene layout, animation, and responsive rules
  tailwind.css              Theme and utility layers, without Preflight
public/
  assets/                   Prepared web assets: panorama, overlays,
                            companions, sign, fonts, and atlas metadata
scripts/
  prepare_assets.py         Landscape, overlay, and sign pipeline
  prepare_companions.py     Companion atlas extraction
  requirements-assets.txt   Asset pipeline dependencies
```

The files in `public/assets` are generated from the original pixel art packs by the scripts in `scripts/`. Those packs stay on my machine and are excluded from the repository, so the site loads the prepared copies instead of the sources.

## What comes next

- [x] Chapter one: landing scene, atmosphere, controls, and accessibility
- [ ] The world map, which will link the sections together
- [ ] Movement and collision so the character can walk the map
- [ ] The portfolio chapters, with projects and background as places
- [ ] A CV chapter you can read in the page or download

## Credits

The world, character, dog, and sign are original artwork made for this project. The interface uses Outfit and Press Start 2P, both under the SIL Open Font License, and the licence files ship alongside the fonts in `public/assets`.

## Elsewhere

You can find the rest of my work on [GitHub](https://github.com/Lionelapex).

<sub>Maintained by Lionel Chapasuka.</sub>
