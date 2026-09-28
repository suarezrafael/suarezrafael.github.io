"""Make fixed-weight TTFs for the PDF and compact WOFF2s for the website."""

from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
INSTANCES = (
    ("Fraunces-variable.ttf", "Fraunces-Semibold", {"opsz": 48, "wght": 600, "SOFT": 20, "WONK": 0}),
    ("Fraunces-Italic-variable.ttf", "Fraunces-SemiboldItalic", {"opsz": 48, "wght": 600, "SOFT": 20, "WONK": 0}),
    ("Manrope-variable.ttf", "Manrope-Regular", {"wght": 400}),
    ("Manrope-variable.ttf", "Manrope-Bold", {"wght": 700}),
)


def main():
    for source, name, axes in INSTANCES:
        font = instantiateVariableFont(TTFont(FONTS / "source" / source), axes, inplace=False)
        font.save(FONTS / f"{name}.ttf")
        font.flavor = "woff2"
        font.save(FONTS / f"{name}.woff2")
        font.close()


if __name__ == "__main__":
    main()
