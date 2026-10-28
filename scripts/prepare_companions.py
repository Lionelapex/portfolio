"""Slice the supplied presentation sheet into aligned transparent web atlases.

No artwork is generated. Separate the opaque presentation background using
graph-cut, retain the connected sprite, and align frames by their shoes/paws.
"""
from pathlib import Path
from collections import deque
import argparse
import json
import shutil
import numpy as np
import cv2
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'source-assets' / 'character-corgi-animation-sheet.png'
OUT = ROOT / 'public' / 'assets' / 'companions'
QA = ROOT / 'artifacts' / 'companions'

ROWS = {
    'character-idle': {'centers': [65, 186, 311, 435, 559, 681, 804, 925, 1048, 1157, 1265, 1368, 1473], 'y': (53, 239), 'height': 180, 'cell': (116, 194)},
    'character-wave': {'centers': [48, 136, 238, 331, 419, 501, 581, 664, 746, 830, 917, 1010, 1104, 1196, 1292, 1379, 1473], 'y': (309, 477), 'height': 180, 'cell': (116, 194)},
    'dog-idle': {'centers': [60, 174, 291, 418, 541, 669, 800, 931, 1057, 1185, 1310, 1443], 'y': (554, 665), 'height': 104, 'cell': (112, 124)},
    'dog-happy': {'centers': [59, 150, 243, 331, 416, 497, 585, 678, 772, 868, 966, 1062, 1161, 1259, 1359, 1464], 'y': (753, 849), 'height': 104, 'cell': (112, 124)},
}

def connected(mask):
    """Keep the sprite, excluding detached background gradients and shadows."""
    h, w = mask.shape
    visited = np.zeros_like(mask)
    components = []
    for y, x in zip(*np.nonzero(mask)):
        if visited[y, x]:
            continue
        queue = deque([(int(x), int(y))])
        visited[y, x] = True
        component = []
        while queue:
            px, py = queue.popleft()
            component.append((px, py))
            for nx, ny in ((px-1, py), (px+1, py), (px, py-1), (px, py+1)):
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((nx, ny))
        components.append(component)
    largest = max(components, key=len)
    result = np.zeros_like(mask)
    for x, y in largest:
        result[y, x] = True
    # Fill enclosed regions: outlines surround fur and clothing that can match
    # the presentation background in colour.
    outside = np.zeros_like(mask)
    queue = deque([(x, 0) for x in range(w)] + [(x, h-1) for x in range(w)] + [(0, y) for y in range(h)] + [(w-1, y) for y in range(h)])
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < w and 0 <= y < h) or outside[y, x] or result[y, x]:
            continue
        outside[y, x] = True
        queue.extend(((x-1, y), (x+1, y), (x, y-1), (x, y+1)))
    return ~outside

def isolate(im):
    rgb = np.asarray(im.convert('RGB'))
    h, w = rgb.shape[:2]
    # Graph-cut separates the opaque gradient from the existing artwork.
    # The two-pixel perimeter is known background; internal colour models
    # preserve dark hair, white fur, and enclosed clothing details.
    mask = np.zeros((h, w), dtype=np.uint8)
    bg = np.zeros((1, 65), dtype=np.float64)
    fg = np.zeros((1, 65), dtype=np.float64)
    cv2.grabCut(rgb, mask, (2, 2, w-4, h-4), bg, fg, 7, cv2.GC_INIT_WITH_RECT)
    alpha = connected((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD))
    result = np.asarray(im.convert('RGBA')).copy()
    result[:, :, 3] = alpha.astype(np.uint8) * 255
    return Image.fromarray(result)

def prepare():
    cv2.setRNGSeed(0)
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE)
    manifest = {}
    previews = []
    for name, row in ROWS.items():
        centers = row['centers']
        frames = []
        # One scale per row, preserving frame-to-frame breathing and motion.
        scale = row['height'] / (180 if name == 'character-idle' else 162 if name == 'character-wave' else 104 if name == 'dog-idle' else 90)
        for i, center in enumerate(centers):
            left = round((centers[i-1] + center) / 2) if i else 4
            right = round((center + centers[i+1]) / 2) if i < len(centers)-1 else 1532
            frame = isolate(source.crop((left, row['y'][0], right, row['y'][1])))
            box = frame.getbbox()
            if not box:
                raise ValueError(f'Empty frame: {name} {i}')
            alpha = np.asarray(frame.getchannel('A'))
            # Feet are the stable anchor; the raised arm must never shift it.
            foot_y, foot_x = np.nonzero(alpha[max(0, box[3]-12):box[3]])
            anchor = (foot_x.min() + foot_x.max()) / 2
            frame = frame.resize((round(frame.width*scale), round(frame.height*scale)), Image.Resampling.NEAREST)
            cell = Image.new('RGBA', row['cell'])
            cell.alpha_composite(frame, (round(row['cell'][0]/2 - anchor*scale), round(row['cell'][1]-5-box[3]*scale)))
            visible = cell.getbbox()
            if not visible or visible[3] - visible[1] < row['height'] * .88:
                raise ValueError(f'Incomplete sprite: {name} frame {i + 1}')
            if not (row['cell'][1] - 7 <= visible[3] <= row['cell'][1] - 3):
                raise ValueError(f'Unstable foot baseline: {name} frame {i + 1}')
            frames.append(cell)
        atlas = Image.new('RGBA', (row['cell'][0]*len(frames), row['cell'][1]))
        for i, frame in enumerate(frames):
            atlas.alpha_composite(frame, (i*row['cell'][0], 0))
        atlas.save(OUT / f'{name}.webp', 'WEBP', lossless=True, method=6)
        manifest[name] = {'frames': len(frames), 'width': row['cell'][0], 'height': row['cell'][1]}
        preview = Image.new('RGB', (row['cell'][0]*len(frames), row['cell'][1]+28), '#77c7f7')
        for i, frame in enumerate(frames):
            preview.paste(frame, (i*row['cell'][0], 24), frame)
        ImageDraw.Draw(preview).text((5, 5), name, fill='#102b49')
        previews.append(preview)
        frames[0].save(QA / f'{name}.gif', save_all=True, append_images=frames[1:], duration=110, loop=0, disposal=2)
    contact = Image.new('RGB', (max(p.width for p in previews), sum(p.height for p in previews)), '#77c7f7')
    top = 0
    for p in previews:
        contact.paste(p, (0, top))
        top += p.height
    contact.save(QA / 'contact-sheet.png')
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    if args.source:
        SOURCE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.source, SOURCE)
    prepare()
