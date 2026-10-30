"""Renders the loader wordmark: the site's SM mark on its violet tile, then the pack
name in Pixelify Sans (SIL OFL, see OFL.txt). Run after changing either; the output
is committed so the mod build needs neither Pillow nor the font."""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MARK = os.path.join(ROOT, "site", "assets", "images", "logo-mark-128.png")
OUT = os.path.join(ROOT, "loader", "resources", "assets", "streamline_loader", "loader", "logo.png")
TILE, INK = (0x5B, 0x45, 0xB4, 255), (0xE9, 0xE7, 0xF5, 255)
SIZE, GAP, TEXT_PX = 128, 36, 76

font = ImageFont.truetype(os.path.join(HERE, "PixelifySans.ttf"), TEXT_PX)
try:
    font.set_variation_by_axes([600])
except (OSError, AttributeError):
    pass
text = "Streamline Master"
left, top, right, bottom = font.getbbox(text)
width = SIZE + GAP + (right - left)
img = Image.new("RGBA", (width, SIZE), (0, 0, 0, 0))
img.paste(Image.new("RGBA", (SIZE, SIZE), TILE), (0, 0))
mark = Image.open(MARK).convert("RGBA").resize((SIZE, SIZE), Image.NEAREST)
img.alpha_composite(mark)
draw = ImageDraw.Draw(img)
draw.text((SIZE + GAP - left, (SIZE - (bottom - top)) // 2 - top), text, font=font, fill=INK)
img.save(OUT, optimize=True)
print(OUT, img.size)
