"""Render PNG profile and app-icon exports from the SoulCont brand system."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img" / "soulcont"
NAVY = "#071B2E"
GOLD = "#C7A15A"
CREAM = "#F7F4EE"


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    face = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / face, size=size)


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, font_size: int, color: str, spacing: int = 0) -> None:
    face = font(font_size)
    if not spacing:
        box = draw.textbbox((0, 0), text, font=face)
        canvas_width = draw.im.size[0]
        draw.text(((canvas_width - (box[2] - box[0])) / 2, y), text, font=face, fill=color)
        return

    widths = [draw.textlength(letter, font=face) for letter in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (draw.im.size[0] - total) / 2
    for letter, width in zip(text, widths):
        draw.text((x, y), letter, font=face, fill=color)
        x += width + spacing


def draw_mark(size: int, background: str, label: bool) -> Image.Image:
    image = Image.new("RGB", (size, size), background)
    draw = ImageDraw.Draw(image)
    pad = int(size * 0.085)
    center = size // 2
    diameter = size - (pad * 2)
    draw.ellipse((pad, pad, pad + diameter, pad + diameter), outline=GOLD, width=max(3, int(size * 0.022)))
    centered(draw, "S", int(size * (0.19 if label else 0.235)), int(size * (0.49 if label else 0.55)), GOLD)
    dot = int(size * 0.052)
    draw.ellipse((int(size * 0.69), int(size * 0.22), int(size * 0.69) + dot, int(size * 0.22) + dot), fill=CREAM)
    if label:
        centered(draw, "SOULCONT", int(size * 0.88), int(size * 0.043), CREAM if background == NAVY else NAVY, spacing=int(size * 0.011))
    return image


def main() -> None:
    favicon = draw_mark(512, NAVY, False)
    favicon.save(OUT / "favicon-512.png", optimize=True)
    favicon.resize((192, 192), Image.Resampling.LANCZOS).save(OUT / "icon-192.png", optimize=True)
    favicon.resize((180, 180), Image.Resampling.LANCZOS).save(OUT / "apple-touch-icon.png", optimize=True)
    favicon.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    draw_mark(1080, CREAM, False).save(OUT / "instagram-profile-1080.png", optimize=True)
    draw_mark(1080, NAVY, False).save(OUT / "whatsapp-profile-1080.png", optimize=True)


if __name__ == "__main__":
    main()
