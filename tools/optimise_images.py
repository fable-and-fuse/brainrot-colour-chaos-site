"""One-off image optimiser for the Brainrot Colour Chaos site.

Reads the untouched originals from the supplied asset bundle and writes
web-sized WebP/PNG/JPEG derivatives into site/assets/img. Originals are
never modified. Requires Pillow (`pip install pillow`).

Usage:
    python tools/optimise_images.py [path-to-source-assets]
"""
import sys
from pathlib import Path

from PIL import Image

DEFAULT_SRC = Path.home() / "Downloads" / "Brainrot_Colour_Chaos_Website_Claude_Code_Bundle" / "website_package" / "assets"
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
OUT = Path(__file__).resolve().parent.parent / "site" / "assets" / "img"
NAVY = (9, 17, 38)

# source file -> (output stem, [widths], webp quality)
JOBS = {
    "07_Hardcover_Digital_Mockup.png": ("hardcover-mockup", [640, 1100], 86),
    "01_Brainrot_Front_Cover.png": ("front-cover", [600, 1000], 84),
    "02_Ruotino_Spometti_115.png": ("page-115-ruotino-spompetti", [640, 1400], 82),
    "03_Bombardiro_Crocodillo_114.png": ("page-114-bombardiro-crocodillo", [640, 1400], 82),
    "04_Capuchino_Assassino_149.png": ("page-149-capuchino-assassino", [640, 1400], 82),
    "05_Character_Checklist.png": ("character-checklist", [720, 1400], 82),
    "06_Ruotino_Full_Colour_Artwork.png": ("ruotino-colour-inspiration", [800, 1600], 84),
    "Fable_and_Fuse_Studios_Final_Master_Logo_2.png": ("fable-and-fuse-logo", [240, 480], 88),
}


def resize(im: Image.Image, width: int) -> Image.Image:
    if im.width <= width:
        return im.copy()
    height = round(im.height * width / im.width)
    return im.resize((width, height), Image.LANCZOS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (stem, widths, quality) in JOBS.items():
        with Image.open(SRC / name) as im:
            im.load()
            if im.mode == "RGBA":
                # Trim fully transparent margins only; artwork pixels are untouched.
                im = im.crop(im.getchannel("A").getbbox())
            for w in widths:
                dst = OUT / f"{stem}-{w}.webp"
                resize(im, w).save(dst, "WEBP", quality=quality, method=6)
                print(f"{dst.name:48} {dst.stat().st_size // 1024:>5} KB")

    # QR code: keep the original 1-bit PNG pixel-perfect (it is ~1 KB).
    with Image.open(SRC / "Brainrot_Colour_Chaos_Amazon_QR_Code.png") as qr:
        qr.save(OUT / "amazon-au-qr.png", optimize=True)

    # Open Graph image: real front cover centred on the ink-navy brand colour.
    with Image.open(SRC / "01_Brainrot_Front_Cover.png") as cover:
        cover = cover.convert("RGB")
        canvas = Image.new("RGB", (1200, 630), NAVY)
        fitted = resize(cover, round(cover.width * 590 / cover.height))
        canvas.paste(fitted, ((1200 - fitted.width) // 2, 20))
        canvas.save(OUT.parent / "og-image.jpg", "JPEG", quality=86, optimize=True, progressive=True)

    # Favicons from the studio logo.
    with Image.open(SRC / "Fable_and_Fuse_Studios_Final_Master_Logo_2.png") as logo:
        logo = logo.convert("RGBA")
        logo.resize((180, 180), Image.LANCZOS).save(OUT.parent / "apple-touch-icon.png", optimize=True)
        logo.resize((64, 64), Image.LANCZOS).save(OUT.parent / "favicon.png", optimize=True)


if __name__ == "__main__":
    main()
