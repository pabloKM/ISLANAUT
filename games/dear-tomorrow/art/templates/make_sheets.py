"""Draw-over reference sheets for Dear Tomorrow art (spoiler-free).
Letter landscape at 300 dpi: 3300 x 2550 px. Light-blue guides, labeled boxes, faint ghosts of Pablo's Waker."""
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 3300, 2550
M = 110
BLUE = (110, 165, 220)
BLUE_L = (196, 222, 245)
TXT = (45, 75, 115)
RED = (225, 70, 70)
F = '/usr/share/fonts/truetype/dejavu/'
def font(sz, bold=False): return ImageFont.truetype(F + ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'), sz)
FT, FS, FL, FN = font(64, True), font(34), font(36, True), font(27)

FRONT = Image.open('/home/claude/dt-poc/waker-front.png').convert('RGBA')
SIDE = Image.open('/home/claude/dt-poc/waker-side.png').convert('RGBA')
# proportions measured on the front view (fraction of full height, top = 0)
GUIDES = [(0.0, 'top of hood loop'), (0.10, 'top of hood'), (0.31, 'bill edge'), (0.47, 'collar'), (0.79, 'coat hem'), (1.0, 'ground')]

def new_sheet(n, total, title, note):
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    d.text((M, 70), f'Dear Tomorrow  ·  Sheet {n} of {total}', font=FS, fill=TXT)
    d.text((M, 115), title, font=FT, fill=TXT)
    d.text((M, 200), note, font=FS, fill=TXT)
    d.line([(M, 255), (W - M, 255)], fill=BLUE, width=3)
    d.text((M, H - 80), 'Blue = guides. Hide or delete this layer when you are done. Put each labeled part on its own layer. Any line weight is fine.',
           font=FN, fill=TXT)
    return im, d

def ghost(im, src, box_xy, height, alpha=0.16, flip=False):
    s = src.transpose(Image.FLIP_LEFT_RIGHT) if flip else src
    w = round(s.width * height / s.height); s = s.resize((w, height), Image.LANCZOS)
    a = s.split()[3].point(lambda v: int(v * alpha))
    tint = Image.new('RGBA', s.size, BLUE + (0,)); tint.putalpha(a)
    x, y = box_xy; im.paste(tint, (int(x - w / 2), int(y - height)), tint)

def dashed(d, p0, p1, dash=18, gap=12, w=2, fill=BLUE_L):
    (x0, y0), (x1, y1) = p0, p1; L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    if L == 0: return
    k = 0.0
    while k < L:
        a, b = k / L, min(L, k + dash) / L
        d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=fill, width=w)
        k += dash + gap

def box(d, x, y, w, h, label, sub=None, ground=0.9, center=True):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, outline=BLUE, width=3)
    d.text((x + 18, y + 12), label, font=FL, fill=TXT)
    if sub: d.text((x + 18, y + 56), sub, font=FN, fill=TXT)
    gy = None
    if ground is not None:
        gy = y + h * ground; d.line([(x + 14, gy), (x + w - 14, gy)], fill=BLUE, width=3)
    if center: dashed(d, (x + w / 2, y + 100), (x + w / 2, y + h - 14))
    return gy

def pivot(d, x, y, r=22):
    d.line([(x - r, y), (x + r, y)], fill=RED, width=5); d.line([(x, y - r), (x, y + r)], fill=RED, width=5)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=RED, width=3)

def height_guides(d, x0, x1, gy, hpx, labels=True):
    for f, name in GUIDES:
        y = gy - hpx * (1 - f)
        dashed(d, (x0, y), (x1, y), w=2)
        if labels: d.text((x1 + 10, y - 16), name, font=FN, fill=TXT)

def scale_ref(im, d, x, gy, hpx, text='Waker, for scale'):
    ghost(im, FRONT, (x, gy), hpx, alpha=0.22)
    d.text((x - 90, gy + 8), text, font=FN, fill=TXT)

sheets = []
TOTAL = 9

# 1 · Waker turnaround -------------------------------------------------------
im, d = new_sheet(1, TOTAL, 'The Waker: turnaround', 'Front, side and back at the same height. Your existing drawings are ghosted in to trace or redraw.')
top, bot = 300, H - 150; bw = 900; gap = 40; x = M
hpx = 1250
for i, (lab, sub) in enumerate([('Front', 'redraw or trace your v1'), ('Side (facing right)', 'redraw or trace your v1'), ('Back', 'new: please draw this one')]):
    bx = x + i * (bw + gap)
    gy = box(d, bx, top, bw, bot - top, lab, sub, ground=0.93)
    if i == 0: ghost(im, FRONT, (bx + bw / 2, gy), hpx)
    if i == 1: ghost(im, SIDE, (bx + bw / 2, gy), hpx)
    if i == 2: ghost(im, FRONT, (bx + bw / 2, gy), hpx, alpha=0.06)
height_guides(d, M + 14, M + 3 * bw + 2 * gap - 14, gy, hpx)
d.text((M + 3 * bw + 2 * gap + 10, top + 130), 'Optional:\n3/4 view\n(if you like)', font=FN, fill=TXT)
sheets.append(im)

# 2 · Waker parts for rigging ------------------------------------------------
im, d = new_sheet(2, TOTAL, 'The Waker: parts on separate layers', 'So I can animate in code. Draw each part whole, including bits normally hidden. The red + is where the part attaches.')
cols, rows = 6, 3; gx, gy0 = M, 290; cw = (W - 2 * M - (cols - 1) * 40) / cols; ch = (H - gy0 - 140 - (rows - 1) * 40) / rows
parts = [
    ('Hood + bill', 'front', (0.5, 0.86)), ('Hood + bill', 'side', (0.45, 0.86)), ('Hood', 'back', (0.5, 0.86)),
    ('Face eye', 'open', None), ('Face eye', 'half shut', None), ('Face eye', 'shut (blink)', None),
    ('Coat + collar', 'front', (0.5, 0.2)), ('Coat + collar', 'side', (0.5, 0.2)), ('Coat + collar', 'back', (0.5, 0.2)),
    ('Collar clip', 'front + side', None), ('Mitten', 'left', (0.5, 0.35)), ('Mitten', 'right', (0.5, 0.35)),
    ('Chalk stick', 'whole', (0.5, 0.5)), ('Leg + flip-flop', 'front, left & right', (0.5, 0.18)), ('Leg + flip-flop', 'side, near & far', (0.5, 0.18)),
    ('Leg + flip-flop', 'back, left & right', (0.5, 0.18)), ('Shadow face', 'inside the hood', (0.5, 0.5)), ('Anything else', 'you think moves', None),
]
for i, (lab, sub, pv) in enumerate(parts):
    c, r = i % cols, i // cols; bx, by = gx + c * (cw + 40), gy0 + r * (ch + 40)
    box(d, bx, by, cw, ch, lab, sub, ground=None, center=False)
    if pv: pivot(d, bx + cw * pv[0], by + 110 + (ch - 130) * pv[1])
d.text((W - M - 980, 205), 'Tip: a layer per part in one file is perfect.', font=FS, fill=RED)
sheets.append(im)

# 3 · Waker poses ------------------------------------------------------------
im, d = new_sheet(3, TOTAL, 'The Waker: special poses', 'Poses the puppet can\'t make on its own. The walk row is optional: I can animate walking in code.')
bw, bh, y0 = (W - 2 * M - 4 * 40) / 5, 1080, 290
hp = 720
poses = [('Writing on the Board', 'side, chalk raised high'), ('Asleep in the hammock', 'lying down, curled'), ('Waking up', 'front, big stretch'),
         ('Holding a note', 'front, card in both mittens'), ('Surprised', 'front, eye wide, hop')]
for i, (lab, sub) in enumerate(poses):
    bx = M + i * (bw + 40); g = box(d, bx, y0, bw, bh, lab, sub, ground=0.93)
    ghost(im, SIDE if i == 0 else FRONT, (bx + bw / 2, g), hp, alpha=0.07)
y1 = y0 + bh + 60; bw2 = (W - 2 * M - 3 * 40) / 4; bh2 = H - y1 - 140
for i, lab in enumerate(['Walk 1 · contact', 'Walk 2 · down', 'Walk 3 · passing', 'Walk 4 · up']):
    bx = M + i * (bw2 + 40); g = box(d, bx, y1, bw2, bh2, lab, 'side, optional', ground=0.9)
    ghost(im, SIDE, (bx + bw2 / 2, g), int(bh2 * 0.7), alpha=0.07)
sheets.append(im)

# 4 · Tortoise ---------------------------------------------------------------
im, d = new_sheet(4, TOTAL, 'An old tortoise', 'Very old, slow and kind. Mossy shell, patient eyes. Mostly still: a slow blink and a head turn.')
y0 = 290; bigw = 1900; bh = 1250
g = box(d, M, y0, bigw, bh, 'Side view (body + shell)', 'about twice the Waker\'s length, a bit taller', ground=0.93)
scale_ref(im, d, M + bigw - 200, g, 520)
bx = M + bigw + 50; sw = W - M - bx
g2 = box(d, bx, y0, sw, bh, 'Head + neck, separate', 'side; the red + is where it meets the shell', ground=None)
pivot(d, bx + 120, y0 + bh * 0.62)
y1 = y0 + bh + 50; bh2 = H - y1 - 140; w3 = (W - 2 * M - 3 * 40) / 4
for i, (lab, sub) in enumerate([('Front view', 'facing you'), ('Head turned', 'toward the camera'), ('Eyes', 'open / half / shut'), ('Moss & details', 'patches, tufts, cracks')]):
    xb = M + i * (w3 + 40); box(d, xb, y1, w3, bh2, lab, sub, ground=0.9 if i < 2 else None)
sheets.append(im)

# 5 · Hermit crab ------------------------------------------------------------
im, d = new_sheet(5, TOTAL, 'A hermit crab with a mailbox shell', 'Busy, skittery and proud of itself. About half the Waker\'s height, mailbox included.')
y0 = 290; bw = (W - 2 * M - 3 * 40) / 4; bh = 1050
for i, (lab, sub) in enumerate([('Side view', 'whole crab + shell'), ('Front view', 'claws, eyes on stalks'), ('Mailbox shell alone', 'flag DOWN'), ('Mailbox shell alone', 'flag UP')]):
    xb = M + i * (bw + 40); g = box(d, xb, y0, bw, bh, lab, sub, ground=0.92)
    if i == 0: scale_ref(im, d, xb + bw - 120, g, 560)
    if i >= 2: pivot(d, xb + bw / 2, y0 + bh * 0.8)
y1 = y0 + bh + 50; bh2 = H - y1 - 140
for i, (lab, sub) in enumerate([('Body without shell', 'side; + = where shell sits'), ('Scuttle A', 'legs one way'), ('Scuttle B', 'legs the other way'), ('Salute / proud pose', 'one claw up')]):
    xb = M + i * (bw + 40); box(d, xb, y1, bw, bh2, lab, sub, ground=0.9)
    if i == 0: pivot(d, xb + bw / 2, y1 + bh2 * 0.45)
sheets.append(im)

# 6 · Gulls ------------------------------------------------------------------
im, d = new_sheet(6, TOTAL, 'Gulls', 'Cheeky nuisances, not villains. A bit over half the Waker\'s height standing. Readable as a little group.')
y0 = 290; bw = (W - 2 * M - 3 * 40) / 4; bh = 1050
for i, (lab, sub) in enumerate([('Standing', 'side'), ('Hop', 'side, feet up'), ('Peck', 'side, head down'), ('Squawk', 'side, beak open')]):
    xb = M + i * (bw + 40); g = box(d, xb, y0, bw, bh, lab, sub, ground=0.92)
    if i == 0: scale_ref(im, d, xb + bw - 110, g, 520)
y1 = y0 + bh + 50; bh2 = H - y1 - 140
for i, (lab, sub) in enumerate([('Flying 1', 'wings UP, side'), ('Flying 2', 'wings DOWN, side'), ('Flying, from above', 'seen from the sky'), ('A little flock', '3 together, any poses')]):
    xb = M + i * (bw + 40); box(d, xb, y1, bw, bh2, lab, sub, ground=None)
sheets.append(im)

# 7 · Props ------------------------------------------------------------------
im, d = new_sheet(7, TOTAL, 'Props', 'Each prop on its own layer. Scale doesn\'t need to be exact: the Waker ghost is just a guide.')
y0 = 290; bh = 1180
specs = [('Palm tree: trunk', 'separate from leaves', 520), ('Palm tree: leaves', '+ = top of trunk', 620), ('Hammock', 'empty, hanging', 900), ('The Board', 'corkboard on a post', 740)]
x = M
for i, (lab, sub, w) in enumerate(specs):
    g = box(d, x, y0, w, bh, lab, sub, ground=0.93 if i != 1 else None)
    if i == 0: scale_ref(im, d, x + w - 110, g, 380)
    if i == 1: pivot(d, x + w / 2, y0 + bh * 0.62)
    if i == 3:
        d.rectangle([x + 110, y0 + 230, x + w - 110, y0 + 640], outline=BLUE_L, width=3)
        d.text((x + 130, y0 + 245), 'cork area (notes get pinned here)', font=FN, fill=TXT)
    x += w + 40
y1 = y0 + bh + 50; bh2 = H - y1 - 140; bw = (W - 2 * M - 4 * 40) / 5
for i, (lab, sub) in enumerate([('Blank note + pin', 'square card, empty'), ('Chalk stub', 'small, on its own'), ('Rocks', '2 or 3 sizes'), ('Little extras', 'shells, driftwood...'), ('Island coastline', 'any shape you like')]):
    xb = M + i * (bw + 40); box(d, xb, y1, bw, bh2, lab, sub, ground=None)
    if i == 0: d.rectangle([xb + bw / 2 - 170, y1 + 200, xb + bw / 2 + 170, y1 + 540], outline=BLUE_L, width=3)
sheets.append(im)

# 8 & 9 · Glyphs -------------------------------------------------------------
def glyph_sheet(n, title, note, labels):
    im, d = new_sheet(n, TOTAL, title, note)
    cols, rows = 3, 2; y0 = 300; cw = (W - 2 * M - 2 * 60) / cols; ch = (H - y0 - 150 - 60) / rows
    for i, lab in enumerate(labels):
        c, r = i % cols, i // cols; bx, by = M + c * (cw + 60), y0 + r * (ch + 60)
        d.rounded_rectangle([bx, by, bx + cw, by + ch], radius=18, outline=BLUE, width=3)
        d.text((bx + 18, by + 12), lab, font=FL, fill=TXT)
        s = min(cw, ch) - 220; cx, cy = bx + cw / 2, by + ch / 2 + 30
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=BLUE_L, width=3)
        dashed(d, (cx - s / 2, cy), (cx + s / 2, cy)); dashed(d, (cx, cy - s / 2), (cx, cy + s / 2))
    return im
sheets.append(glyph_sheet(8, 'Glyphs: in your hand', 'One glyph per square, black on white, drawn simply and quickly, the way you would scribble a note. Fill most of the square.',
                          ['Arrow', 'Wave', 'Sun', 'Moon', 'Key', 'Question mark']))
sheets.append(glyph_sheet(9, 'Glyphs: for a friend to draw', 'Give this sheet to a friend. Draw each one in your own style, quickly, black on white. Please don\'t look at anyone else\'s version first.',
                          ['Arrow', 'Wave', 'Sun', 'Moon', 'Key', 'Question mark']))

names = ['1-waker-turnaround', '2-waker-parts', '3-waker-poses', '4-tortoise', '5-hermit-crab', '6-gulls', '7-props', '8-glyphs-yours', '9-glyphs-friend']
out = '/home/claude/sheets/out'
import os; os.makedirs(out, exist_ok=True)
for im, n in zip(sheets, names): im.save(f'{out}/dear-tomorrow-sheet-{n}.png', dpi=(300, 300), optimize=True)
sheets[0].save(f'{out}/dear-tomorrow-reference-sheets.pdf', save_all=True, append_images=sheets[1:], resolution=300)
print('ok', len(sheets))
