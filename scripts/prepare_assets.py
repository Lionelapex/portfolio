"""Create web assets from the supplied packs without modifying the originals."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json
from collections import deque

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public' / 'assets'
OUT.mkdir(parents=True, exist_ok=True)

def webp(image, name):
    image.save(OUT / name, 'WEBP', lossless=True, method=6)

base = Image.open(ROOT / 'landing_precise_overlay_animations/UNCHANGED_BASE_BACKGROUND.png')
base.save(OUT / 'landscape.webp', 'WEBP', quality=94, method=6)
avatar = Image.open(ROOT / 'lionel_landing_page_avatar_assets/lionel_front_avatar.png')
avatar.thumbnail((112, 128), Image.Resampling.NEAREST)
webp(avatar, 'avatar.webp')

# Use only the original resting pose: landing-page companions are static.
source = ROOT / 'landing_character_dog_idle_wave_pack/landing_character_dog_idle_wave_pack/frames'
im = Image.open(source / 'landing_wave_frame_01.png').convert('RGBA')
im = im.crop(im.getbbox())
im = im.resize((round(im.width * 645 / im.height), 645), Image.Resampling.NEAREST)
resting = Image.new('RGBA', (524, 681))
resting.alpha_composite(im, (18, 18))
webp(resting, 'companions-idle.webp')

def align_waterfalls(image):
    """Align the source highlights to the two falls in this exact base image.

    Coordinates remain in the base's native 2166 x 726 space. The two source
    strips sit to the left of the actual water, and need separate offsets.
    Masks prevent highlights spilling onto the banks and rock face.
    """
    result = Image.new('RGBA', image.size)
    falls = [
        ((1480, 335, 1560, 515), (41, 4), [(1544, 345), (1574, 345), (1570, 360), (1571, 485), (1581, 500), (1590, 507), (1575, 516), (1524, 512), (1520, 500), (1533, 486), (1535, 363)]),
        ((1580, 335, 1660, 515), (43, 6), [(1649, 349), (1685, 349), (1686, 481), (1698, 499), (1696, 515), (1635, 519), (1628, 501), (1641, 480), (1641, 364)]),
    ]
    for box, (dx, dy), polygon in falls:
        moved = Image.new('RGBA', image.size)
        moved.alpha_composite(image.crop(box), (box[0] + dx, box[1] + dy))
        mask = Image.new('L', image.size)
        ImageDraw.Draw(mask).polygon(polygon, fill=255)
        moved.putalpha(ImageChops.multiply(moved.getchannel('A'), mask))
        result.alpha_composite(moved)
    return result

# Crop the blank sign from the RGB atlas using its exterior silhouette.
# The checkerboard is baked into the source; never render it as transparency.
atlas = Image.open(ROOT / 'explore_my_world_sign_sprite_pack/explore_my_world_sign_sprite_pack/explore_my_world_sign_sprite_sheet.png').convert('RGBA')
sign = atlas.crop((705, 32, 1282, 591))
mask = Image.new('L', sign.size)
ImageDraw.Draw(mask).polygon([(242, 0), (298, 0), (321, 10), (333, 22), (333, 65), (552, 65), (572, 78), (572, 363), (560, 383), (334, 383), (334, 511), (321, 536), (295, 553), (267, 553), (242, 537), (230, 520), (230, 383), (18, 383), (3, 373), (3, 87), (17, 66), (242, 66)], fill=255)
sign.putalpha(mask)
# Remove exterior checker pixels just inside the polygon, without touching
# enclosed metal bolts or other low-saturation details in the illustration.
pixels = sign.load()
visited = set()
queue = deque([(x, 0) for x in range(sign.width)] + [(x, sign.height - 1) for x in range(sign.width)] + [(0, y) for y in range(sign.height)] + [(sign.width - 1, y) for y in range(sign.height)])
while queue:
    x, y = queue.popleft()
    if (x, y) in visited or not (0 <= x < sign.width and 0 <= y < sign.height):
        continue
    visited.add((x, y))
    r, g, b, a = pixels[x, y]
    if a == 0 or (min(r, g, b) > 125 and max(r, g, b) - min(r, g, b) < 24):
        pixels[x, y] = (r, g, b, 0)
        queue.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
webp(sign, 'sign.webp')

# Crop aligned animation layers to the UNION of their nontransparent bounds.
# A single horizontal atlas per layer keeps requests and DOM updates small.
layers = {}
for category in ('waterfall',):
    images = [Image.open(p).convert('RGBA') for p in sorted((ROOT / 'landing_precise_overlay_animations' / category).glob('*.png'))]
    if category == 'waterfall':
        images = [align_waterfalls(image) for image in images]
    bounds = [im.getbbox() for im in images]
    box = (min(b[0] for b in bounds), min(b[1] for b in bounds), max(b[2] for b in bounds), max(b[3] for b in bounds))
    w, h = box[2] - box[0], box[3] - box[1]
    atlas = Image.new('RGBA', (w * len(images), h))
    for i, im in enumerate(images):
        atlas.alpha_composite(im.crop(box), (i * w, 0))
    webp(atlas, f'{category}.webp')
    layers[category] = {'left': box[0] / 2166 * 100, 'top': box[1] / 726 * 100, 'width': w / 2166 * 100, 'height': h / 726 * 100}
(OUT / 'layers.json').write_text(json.dumps(layers, indent=2))

def sprite_components(image):
    """Find separate supplied sprites, preserving their original pixels."""
    alpha = image.getchannel('A')
    bounds = alpha.getbbox()
    crop = alpha.crop(bounds)
    width, height = crop.size
    pixels = crop.tobytes()
    remaining = {i for i, value in enumerate(pixels) if value}
    components = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        queue = [seed]
        component = []
        while queue:
            index = queue.pop()
            component.append(index)
            x, y = index % width, index // width
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    neighbor = ny * width + nx
                    if 0 <= nx < width and 0 <= ny < height and neighbor in remaining:
                        remaining.remove(neighbor)
                        queue.append(neighbor)
        if len(component) >= 8:
            xs = [index % width + bounds[0] for index in component]
            ys = [index // width + bounds[1] for index in component]
            components.append((min(xs), min(ys), max(xs)+1, max(ys)+1))
    return sorted(components)

# Individual leaves travel across the actual viewport, rather than cycling
# full-canvas frames that jump back to their starting positions.
leaf_source = Image.open(ROOT / 'landing_precise_overlay_animations/leaves/leaves_01.png').convert('RGBA')
leaf_boxes = sprite_components(leaf_source)
for index, box in enumerate(leaf_boxes[:5]):
    leaf = leaf_source.crop(box)
    webp(leaf, f'leaf-{index+1}.webp')

# Keep wing motion from the supplied bird frames, but remove their baked-in
# translation. Continuous CSS motion handles the full horizontal crossing.
bird_frames = []
for path in sorted((ROOT / 'landing_precise_overlay_animations/birds').glob('*.png')):
    image = Image.open(path).convert('RGBA')
    boxes = sprite_components(image)
    bird = image.crop(boxes[0])
    if bird.width > 36 or bird.height > 28:
        raise ValueError(f'Unexpected bird bounds in {path.name}: {bird.size}')
    frame = Image.new('RGBA', (36, 28))
    frame.alpha_composite(bird, ((36-bird.width)//2, (28-bird.height)//2))
    bird_frames.append(frame)
bird_atlas = Image.new('RGBA', (36*len(bird_frames), 28))
for index, frame in enumerate(bird_frames):
    bird_atlas.alpha_composite(frame, (36*index, 0))
webp(bird_atlas, 'bird-wings.webp')
print(f'Prepared static companions, aligned waterfall, {len(leaf_boxes[:5])} leaf sprites, and {len(bird_frames)} bird wing frames. No flag animation.')
