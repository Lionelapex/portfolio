# Lionel’s portfolio

The first chapter: a React landing page reconstructed from the supplied desired landing-page reference and original pixel-art assets.

## Run locally

Paste this one line into PowerShell from any folder:

```powershell
npm.cmd --prefix E:\portfolio install; if ($LASTEXITCODE -eq 0) { npm.cmd --prefix E:\portfolio run dev -- --open }
```

This installs dependencies and opens the app in your browser. Keep the terminal open; press Ctrl+C to stop. See [START-HERE.md](START-HERE.md) for details. From the project folder, `npm run build` produces `dist/`; `npm run preview` serves that build locally.

## Included

- Responsive introduction, brand, navigation, character and dog, and clickable wooden sign.
- Static original character-and-dog artwork and a smaller wooden sign; an aligned waterfall animation, gently falling leaves, and birds crossing the sky. No animated flags.
- Day/night toggle, animation pause control, keyboard navigation, and reduced-motion support.
- A slower entrance sequence: “Hi” appears first, then “I’m Lionel,” followed by the introduction and buttons over about four seconds. Reduced-motion mode shows all content immediately.
- Clear coming-soon dialogs for the world, remaining portfolio chapters, and CV. No CV or personal contact details were supplied.

The world map, movement/collision system, and other pages are intentionally outside this first landing-page implementation.

## Assets

Original packs and ZIPs are preserved. `scripts/prepare_assets.py` creates landscape and environment web copies in `public/assets` using Pillow. It crops ambient layers to their union bounds and extracts the blank sign with a silhouette mask because its source has a baked checkerboard. The sign’s text is accessible HTML.

The active character asset is `public/assets/companions-idle.webp`, generated from the original resting pose in `landing_character_dog_idle_wave_pack` by `scripts/prepare_assets.py`. Python is not needed to launch or build the app.

Lionel, the dog, and the sign remain static. There is no wave timer, frame playback, or sign hover movement. Clicking the companions still shows the hello message. The smaller sign sits farther to the right to reveal both waterfalls on desktop.

The scene follows the viewport height without a fixed desktop/mobile minimum. The sign uses one bottom anchor across every breakpoint, with its post cropped just below the edge so it cannot float above the bottom. The smaller hero sits higher and slightly left on regular screens; compact height layouts preserve space around the character, with tighter typography and spacing on small phones.

The desktop hero has an additional 18-pixel upward adjustment and 10-pixel rightward offset to keep its actions above the character's head. Navigation gently fades in over 800 milliseconds. “Hi” begins at 180 milliseconds, “I’m Lionel” at one second, the role at 1.75 seconds, the paragraph at 2.15 seconds, and the buttons at 2.55 seconds. Each text stage eases in over roughly a second with a six-pixel rise. These entrances run once per page load, use opacity/transform only, and leave the character, dog, and sign static. Theme changes do not replay the entrance.

Tailwind CSS is integrated through `@tailwindcss/vite` in `vite.config.js`. `src/tailwind.css` imports the theme and utility layers without Preflight, preserving the existing custom reset, fonts, spacing, and artwork. Layout utilities are used in the React markup alongside the original stylesheet; custom animation utilities and `motion-safe:` variants handle the slower entrance timing. Continue using the same npm launch command.

The original waterfall highlights were offset onto the rock face. `align_waterfalls` in `scripts/prepare_assets.py` repositions the left and right strips independently in the background's native 2166 × 726 coordinates and masks them to the water and splash areas before atlas cropping. The background and overlays share one responsive landscape container, preserving their alignment as the scene scales.

The alternative sheet and its extracted atlases remain preserved in `source-assets` and `public/assets/companions` for future use. The waterfall retains its 2166 × 726 background coordinates. On narrow screens the background is cropped, never stretched; foreground characters and sign have independent layouts.

Leaves use individual sprites extracted from the supplied overlays. Each follows a continuous downward path with gentle sideways sway, exits below the landing viewport, and waits offscreen before restarting. Staggered 28–34-second cycles keep the motion sparse. Birds use the supplied wing poses with continuous horizontal flight at a fixed altitude, crossing right to left over 20.4 seconds and waiting 9.6 seconds offscreen. Their starts are staggered into a small flock.

The atmosphere spans the actual landing viewport using container-relative width/height units, independently of the panorama's responsive crop. This keeps exits outside the visible desktop, tablet, and phone edges. The pause control freezes travel, sway, and wing motion together. Reduced-motion mode hides these moving particles. The waving flag overlay is no longer generated or rendered; flags painted into the landscape remain static.

Fonts: Outfit and Press Start 2P, distributed under the SIL Open Font License; see `public/assets/*-OFL.txt`.
