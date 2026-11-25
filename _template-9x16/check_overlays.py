"""Simulate how a 1080x1920 Reel frame looks in the full-screen Reels viewer on a tall phone
(iPhone 19.5:9, image fills the height, sides cropped), with the app's overlays measured from
Sarah's Facebook screenshot of 26 Nov 2026. Usage: overlay.py in.png out.png [label]"""
import sys
from PIL import Image, ImageDraw, ImageFont
src = Image.open(sys.argv[1]).convert("RGB")
label = sys.argv[3] if len(sys.argv) > 3 else ""
# visible region in image pixels (screen 828x1792 at 0.9333 px per image px)
VX0, VX1 = 96, 984
ZONES = [  # (x0, y0, x1, y1) in image pixels
    (0, 0, 1080, 190, "status bar + back/search"),
    (885, 1090, 1080, 1590, "like / comment / share / save"),
    (0, 1520, 1080, 1920, "name, caption, audio, comment box"),
]
im = src.copy().convert("RGBA")
ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for x0, y0, x1, y1, _ in ZONES:
    d.rectangle((x0, y0, x1, y1), fill=(230, 40, 40, 90), outline=(230, 40, 40, 255), width=4)
im = Image.alpha_composite(im, ov).crop((VX0, 0, VX1, 1920)).convert("RGB")
if label:
    D = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 44)
    D.rectangle((0, 1830, im.width, 1920), fill=(255, 255, 255))
    D.text((20, 1845), label, font=f, fill=(0, 0, 0))
im.save(sys.argv[2])
