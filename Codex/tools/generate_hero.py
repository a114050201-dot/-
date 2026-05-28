from PIL import Image, ImageDraw, ImageFilter
import math
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "assets" / "sweet-kingdom-hero.png"
W, H = 1800, 1100


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient_bg(draw):
    top = (255, 214, 232)
    mid = (199, 241, 236)
    bot = (255, 246, 188)
    for y in range(H):
        if y < H * 0.58:
            t = y / (H * 0.58)
            c = tuple(lerp(top[i], mid[i], t) for i in range(3))
        else:
            t = (y - H * 0.58) / (H * 0.42)
            c = tuple(lerp(mid[i], bot[i], t) for i in range(3))
        draw.line((0, y, W, y), fill=c)


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def cloud(draw, x, y, scale, fill):
    parts = [
        (x, y + 22 * scale, x + 130 * scale, y + 78 * scale),
        (x + 34 * scale, y, x + 105 * scale, y + 70 * scale),
        (x + 86 * scale, y + 14 * scale, x + 180 * scale, y + 82 * scale),
        (x + 145 * scale, y + 30 * scale, x + 255 * scale, y + 86 * scale),
    ]
    for p in parts:
        ellipse(draw, p, fill)


def draw_castle(draw, ox, oy):
    shadow = (241, 154, 183, 90)
    rounded(draw, (ox + 44, oy + 250, ox + 610, oy + 430), 48, shadow)
    rounded(draw, (ox + 85, oy + 140, ox + 560, oy + 420), 56, (255, 177, 205), (255, 255, 255), 8)
    for tx, th in [(130, 260), (285, 340), (435, 250)]:
        rounded(draw, (ox + tx, oy + 35 + (300 - th), ox + tx + 105, oy + 420), 45, (255, 198, 219), (255, 255, 255), 7)
        cone = [
            (ox + tx - 15, oy + 65 + (300 - th)),
            (ox + tx + 52, oy - 45 + (300 - th)),
            (ox + tx + 120, oy + 65 + (300 - th)),
        ]
        draw.polygon(cone, fill=(250, 112, 161), outline=(255, 255, 255))
        ellipse(draw, (ox + tx + 28, oy - 80 + (300 - th), ox + tx + 78, oy - 32 + (300 - th)), (246, 72, 124))
    for wx in [170, 330, 490]:
        ellipse(draw, (ox + wx, oy + 205, ox + wx + 58, oy + 274), (129, 219, 229), (255, 255, 255), 5)
    rounded(draw, (ox + 295, oy + 292, ox + 390, oy + 420), 42, (154, 95, 72), (255, 255, 255), 5)
    for sx in range(120, 540, 78):
        ellipse(draw, (ox + sx, oy + 132 + (sx % 3) * 9, ox + sx + 32, oy + 164 + (sx % 3) * 9), (255, 247, 255))


def draw_princess(draw, x, y, s=1.0):
    ellipse(draw, (x - 55*s, y + 143*s, x + 125*s, y + 198*s), (225, 105, 138, 120))
    rounded(draw, (x, y + 66*s, x + 72*s, y + 170*s), 34*s, (255, 97, 139), (255, 255, 255), max(2, int(4*s)))
    ellipse(draw, (x + 1*s, y, x + 74*s, y + 76*s), (255, 226, 202), (255, 255, 255), max(2, int(4*s)))
    ellipse(draw, (x - 8*s, y - 5*s, x + 82*s, y + 45*s), (233, 72, 114))
    draw.polygon([(x + 4*s, y - 8*s), (x + 20*s, y - 44*s), (x + 36*s, y - 8*s)], fill=(255, 221, 80), outline=(255, 255, 255))
    draw.polygon([(x + 30*s, y - 8*s), (x + 48*s, y - 48*s), (x + 66*s, y - 8*s)], fill=(255, 221, 80), outline=(255, 255, 255))
    ellipse(draw, (x + 21*s, y + 28*s, x + 29*s, y + 38*s), (90, 71, 84))
    ellipse(draw, (x + 49*s, y + 28*s, x + 57*s, y + 38*s), (90, 71, 84))
    draw.arc((x + 28*s, y + 39*s, x + 54*s, y + 59*s), 8, 172, fill=(184, 74, 96), width=max(1, int(2*s)))
    draw.line((x + 76*s, y + 90*s, x + 140*s, y + 50*s), fill=(255, 255, 255), width=max(3, int(6*s)))
    ellipse(draw, (x + 126*s, y + 30*s, x + 164*s, y + 68*s), (255, 96, 132), (255, 255, 255), max(2, int(4*s)))


def draw_baron(draw, x, y, s=1.0):
    ellipse(draw, (x - 32*s, y + 124*s, x + 120*s, y + 174*s), (78, 125, 91, 95))
    ellipse(draw, (x, y, x + 92*s, y + 137*s), (112, 186, 91), (255, 255, 255), max(2, int(4*s)))
    for vx in [17, 36, 55, 74]:
        draw.arc((x + vx*s, y + 7*s, x + (vx + 25)*s, y + 132*s), 92, 268, fill=(68, 142, 76), width=max(1, int(3*s)))
    draw.pieslice((x - 34*s, y + 34*s, x + 30*s, y + 103*s), 115, 285, fill=(61, 103, 72), outline=(255, 255, 255))
    draw.pieslice((x + 62*s, y + 34*s, x + 126*s, y + 103*s), 255, 65, fill=(61, 103, 72), outline=(255, 255, 255))
    draw.polygon([(x + 19*s, y + 2*s), (x + 32*s, y - 30*s), (x + 45*s, y + 2*s)], fill=(255, 217, 78), outline=(255, 255, 255))
    draw.polygon([(x + 43*s, y + 2*s), (x + 57*s, y - 36*s), (x + 70*s, y + 2*s)], fill=(255, 217, 78), outline=(255, 255, 255))
    ellipse(draw, (x + 24*s, y + 54*s, x + 35*s, y + 66*s), (54, 66, 55))
    ellipse(draw, (x + 59*s, y + 54*s, x + 70*s, y + 66*s), (54, 66, 55))
    draw.arc((x + 34*s, y + 76*s, x + 61*s, y + 99*s), 195, 345, fill=(54, 66, 55), width=max(1, int(3*s)))
    for i in range(4):
        ellipse(draw, (x + (98 + i*23)*s, y + (18 + i*11)*s, x + (126 + i*23)*s, y + (44 + i*11)*s), (212, 255, 196, 180), (255,255,255), max(1, int(2*s)))


def draw_world(draw):
    gradient_bg(draw)
    cloud(draw, 105, 90, 0.78, (255, 255, 255, 180))
    cloud(draw, 1260, 115, 0.92, (255, 255, 255, 172))
    cloud(draw, 870, 72, 0.55, (255, 255, 255, 155))
    for x, y, r, c in [
        (190, 845, 180, (135, 222, 183)), (380, 790, 220, (251, 197, 96)),
        (635, 850, 230, (163, 220, 238)), (940, 790, 245, (248, 174, 201)),
        (1225, 850, 230, (142, 211, 148)), (1510, 795, 245, (166, 132, 219)),
    ]:
        ellipse(draw, (x-r, y-r, x+r, y+r), c, (255,255,255), 8)
    rounded(draw, (0, 780, W, H + 90), 90, (255, 235, 178))
    for x in range(0, W, 110):
        ellipse(draw, (x, 795 + (x % 4) * 5, x + 56, 850 + (x % 4) * 5), (255, 255, 255, 190))
    draw_castle(draw, 130, 340)
    rounded(draw, (950, 660, 1685, 820), 75, (118, 82, 60), (255,255,255), 8)
    for x in range(1005, 1620, 110):
        rounded(draw, (x, 520 + (x % 3) * 25, x + 58, 705), 29, (119, 72, 48), (255, 255, 255), 5)
        ellipse(draw, (x - 15, 490 + (x % 3) * 25, x + 73, 565 + (x % 3) * 25), (84, 56, 42), (255,255,255), 4)
    rounded(draw, (1110, 760, 1620, 855), 48, (102, 60, 45))
    for i in range(8):
        x = 75 + i * 220
        ellipse(draw, (x, 886 + (i % 2) * 20, x + 95, 980 + (i % 2) * 20), (248, 158, 190), (255,255,255), 8)
        ellipse(draw, (x + 31, 916 + (i % 2) * 20, x + 64, 950 + (i % 2) * 20), (255, 235, 178))
    draw_princess(draw, 680, 605, 1.95)
    draw_baron(draw, 1245, 585, 1.95)
    rounded(draw, (745, 832, 1070, 895), 32, (255, 251, 234), (255,255,255), 5)
    rounded(draw, (775, 796, 1045, 850), 24, (255, 162, 103), (255,255,255), 5)
    rounded(draw, (810, 760, 1015, 812), 24, (179, 104, 76), (255,255,255), 5)
    for x in [820, 865, 910, 955, 1000]:
        ellipse(draw, (x, 748, x + 22, 770), (255, 92, 129), (255,255,255), 2)
    for i in range(95):
        x = (i * 137) % W
        y = 55 + ((i * 89) % 760)
        color = [(255, 110, 153), (82, 192, 210), (255, 221, 88), (132, 211, 145)][i % 4]
        if i % 3 == 0:
            ellipse(draw, (x, y, x + 12, y + 12), color)
        elif i % 3 == 1:
            rounded(draw, (x, y, x + 22, y + 10), 5, color)
        else:
            draw.polygon([(x, y + 6), (x + 8, y), (x + 16, y + 6), (x + 8, y + 14)], fill=color)


img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
draw = ImageDraw.Draw(img, "RGBA")
draw_world(draw)

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay, "RGBA")
for x in range(W):
    alpha = int(118 * max(0, 1 - x / (W * 0.72)))
    od.line((x, 0, x, H), fill=(91, 49, 75, alpha))
img = Image.alpha_composite(img, overlay)
img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=105, threshold=3))
OUT.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT, quality=94)
print(OUT)
