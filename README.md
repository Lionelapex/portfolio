# Lionel Chapasuka — Portfolio

> An interactive pixel-art portfolio, built one chapter at a time.

I'm a Computer Science student at the **University of the People** and a developer at **LJ Tutors**. I build web applications, developer tooling, and small products that solve problems I actually run into — usually with JavaScript, React, and a growing amount of Python.

This repository is my main portfolio: a hand-built personal site that grows into a small explorable world. It is not a template. Every animation layer, interaction, and asset pipeline in here was written for this project.

---

## The idea

Most portfolios are a scroll and a grid of cards. This one treats the site as a place you arrive at: a pixel-art landscape with a character, a companion, a wooden sign, and a horizon that changes between day and night.

The landing page is **Chapter One**. Later chapters turn the scene into a navigable world where projects, writing, and background are found rather than listed. The site is deliberately chapter-based so it can keep growing without being redesigned each time something new is added.

---

## What the landing page does

- **Responsive hero scene** — character, dog, wooden sign, and a full waterfall panorama that scales with the viewport instead of being stretched or letterboxed.
- **Day / night toggle** — re-lights the whole scene from the same artwork.
- **Staged entrance sequence** — "Hi" → "I'm Lionel" → role → introduction → actions, eased in over roughly four seconds. Shown instantly when reduced motion is requested.
- **Atmosphere layers** — individually extracted falling leaves on staggered cycles and a bird flock crossing the sky, both frozen by the same pause control.
- **Keyboard navigation** and a visible pause control for every motion layer.
- **Accessible by default** — the wooden sign's text is real HTML rather than baked into an image, and placeholder dialogs are announced properly to screen readers.
- **Honest coming-soon destinations** — the world map, remaining chapters, and CV open clear placeholders instead of dead links.

---

## Selected work

Public projects, most with live demos.

### Featured

| Project | What it does | Live |
|---|---|---|
| **[latex-to-word](https://github.com/Lionelapex/latex-to-word)** | Converts ChatGPT and LaTeX output into Word documents with equations that stay editable instead of becoming images. | — |
| **[Retro Pokédex](https://github.com/Lionelapex/Retro-Pok-dex)** | A pixel-art Pokédex: search Pokémon, compare stats side by side, and toggle normal and shiny variants. | [Demo](https://lionelapex.github.io/Retro-Pok-dex/) |
| **[Realtime Voice Receptionist](https://github.com/Lionelapex/realtime-voice-receptionist)** | A browser-based voice agent that holds a receptionist conversation in real time. | — |
| **[Taste Haven](https://github.com/Lionelapex/Taste-haven-website)** | A responsive restaurant site covering menu, services, and online ordering. | [Demo](https://lionelapex.github.io/Taste-haven-website/) |

### Web applications

- **[Personal Finance Tracker](https://github.com/Lionelapex/Personal-Finance-Tracker)** — track income and spending with balances and category breakdowns. · [Demo](https://lionelapex.github.io/Personal-Finance-Tracker/)
- **[Email Notification](https://github.com/Lionelapex/EMAIL-NOTIFICATION)** — a scheduled notification flow built around email delivery.
- **[Rock Paper Crossblades](https://github.com/Lionelapex/Rock-paper-crossblades)** — a themed take on rock-paper-scissors from The Odin Project. · [Demo](https://lionelapex.github.io/Rock-paper-crossblades/)

### Experiments and learning builds

- **[Calculator](https://github.com/Lionelapex/calculator)** — a deliberately over-designed calculator built to test DOM handling and CSS-in-JS styling. · [Demo](https://lionelapex.github.io/calculator/)
- **[ToBinaryConvertor](https://github.com/Lionelapex/ToBinaryConvertor)** — decimal-to-binary conversion with a no-framework interface. · [Demo](https://lionelapex.github.io/ToBinaryConvertor/)
- **[Etch-to-Sketch](https://github.com/Lionelapex/Etch-to-sketch)** — grid-based drawing built to practise event handling.
- **[Interactive Card Component](https://github.com/Lionelapex/Interactive-card-component)** — a component exercise focused on layout and state.
- **[Web Development Resources](https://github.com/Lionelapex/web-development-resources)** — a curated list I keep for people starting out.

Some client and commercial work lives in private repositories. I'm happy to walk through it on request.

---

## Built with

- **React 19** for the component structure — scene layers, atmosphere, and controls are separate and independently pausable.
- **Vite 7** for development and production builds.
- **Tailwind CSS 4** through `@tailwindcss/vite`, imported without Preflight so the project's own reset and hand-tuned spacing survive alongside the utilities.
- **Plain CSS** for the scene itself: the panorama, overlays, and character anchors sit in the artwork's native coordinates and scale with the viewport, which is simpler to reason about than utility classes for this kind of positioning.
- **Python and Pillow** for asset preparation — cropping ambient layers to their union bounds, extracting the blank sign through a silhouette mask, and aligning the waterfall strips onto the rock face before the atlas is cut.

---

## Repository structure

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

The artwork in `public/assets` is generated from the original pixel-art packs by the scripts above. Those source packs stay local and are intentionally excluded from this repository; the shipped web copies are what the site loads.

---

## Roadmap

- [x] Chapter One — landing scene, atmosphere, controls, accessibility
- [ ] The world map — an explorable scene linking each section
- [ ] Movement and collision — walk the character through the world
- [ ] Portfolio chapters — projects, writing, and background as places
- [ ] CV chapter — download and in-page view

---

## Credits

The pixel-art world, character, companion, and sign are original assets made for this project. Interface fonts are **Outfit** and **Press Start 2P**, both distributed under the SIL Open Font License — license files ship in `public/assets`.

---

## Elsewhere

- GitHub — [@Lionelapex](https://github.com/Lionelapex)

<sub>Built and maintained by Lionel Chapasuka.</sub>
