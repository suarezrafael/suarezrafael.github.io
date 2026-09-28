"""Generate the website QR and print-ready, vector business cards."""

from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
URL = "https://suarezrafael.github.io/"
WIDTH = 96 * mm  # 90 x 50 mm trim, plus 3 mm bleed on each side.
HEIGHT = 56 * mm
TRIM_BOX = (3 * mm, 3 * mm, 93 * mm, 53 * mm)

INK = HexColor("#101418")
PAPER = HexColor("#ffffff")
TEAL = HexColor("#00a98f")
LIME = HexColor("#c6ff4a")
CORAL = HexColor("#ff6b5f")
SOFT = HexColor("#b8c6c2")


def top_y(value):
    return HEIGHT - value * mm


def rect(pdf, x, y, width, height, color):
    pdf.setFillColor(color)
    pdf.rect(x * mm, top_y(y + height), width * mm, height * mm, fill=1, stroke=0)


def label(pdf, x, y, value, font="Manrope-Regular", size=8, color=INK):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawString(x * mm, top_y(y), value)


def draw_qr(pdf, qr, x, y, size):
    matrix = qr.get_matrix()
    module = size * mm / len(matrix)
    rect(pdf, x, y, size, size, PAPER)
    pdf.setFillColor(INK)
    for row_index, row in enumerate(matrix):
        for col_index, filled in enumerate(row):
            if filled:
                pdf.rect(
                    x * mm + col_index * module,
                    top_y(y) - (row_index + 1) * module,
                    module,
                    module,
                    fill=1,
                    stroke=0,
                )


def front(pdf, _qr):
    rect(pdf, 0, 0, 96, 56, INK)
    rect(pdf, 7, 7, 8, 8, HexColor("#263033"))
    rect(pdf, 11, 7, 2, 8, TEAL)
    label(pdf, 8, 12.4, "RS", "Manrope-Bold", 8, PAPER)
    label(pdf, 18, 12, "RVS TECNOLOGIA", "Manrope-Bold", 8, PAPER)
    rect(pdf, 82, 0, 2.5, 17, TEAL)
    rect(pdf, 85, 0, 1, 17, LIME)
    rect(pdf, 7, 18, 53, 0.25, HexColor("#3c4749"))

    label(pdf, 7, 30, "Rafael", "Fraunces-Semibold", 26, PAPER)
    label(pdf, 7, 41, "Suarez", "Fraunces-SemiboldItalic", 26, PAPER)
    surname_width = pdfmetrics.stringWidth("Suarez", "Fraunces-SemiboldItalic", 26) / mm
    rect(pdf, 8 + surname_width, 38.5, 1.6, 1.6, CORAL)
    label(pdf, 7, 48, "DESENVOLVIMENTO DE SOFTWARE  /  VENÂNCIO AIRES - RS", "Manrope-Bold", 6.4, SOFT)


def back(pdf, qr):
    rect(pdf, 0, 0, 96, 56, PAPER)
    rect(pdf, 0, 0, 3, 56, TEAL)
    rect(pdf, 3, 0, 0.8, 56, LIME)
    label(pdf, 7, 13, "Vamos conversar.", "Fraunces-SemiboldItalic", 18, INK)
    rect(pdf, 7, 17, 11, 0.8, CORAL)
    label(pdf, 7, 23, "+55 (51) 99123-1245", "Manrope-Bold", 9.2, INK)
    label(pdf, 7, 29, "rafaelv_s@hotmail.com", "Manrope-Regular", 8.1, INK)
    label(pdf, 7, 35, "suarezrafael.github.io", "Manrope-Regular", 8.1, INK)
    label(pdf, 7, 41, "github.com/suarezrafael", "Manrope-Regular", 7.7, INK)
    label(pdf, 7, 49, "RAFAEL SUAREZ  /  RVS TECNOLOGIA", "Manrope-Bold", 6.2, HexColor("#56646b"))
    draw_qr(pdf, qr, 65, 10, 24)
    label(pdf, 66, 38, "ABRA O CARTÃO", "Manrope-Bold", 6.3, INK)


def write_pdf(path, pages, qr):
    pdf = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT), pageCompression=1)
    pdf.setTitle("Cartão Rafael Suarez - arte para impressão")
    pdf.setAuthor("Rafael Suarez / RVS Tecnologia")
    for page in pages:
        pdf.setTrimBox(TRIM_BOX)
        pdf.setBleedBox((0, 0, WIDTH, HEIGHT))
        page(pdf, qr)
        pdf.showPage()
    pdf.save()


def main():
    for name in ("Fraunces-Semibold", "Fraunces-SemiboldItalic", "Manrope-Regular", "Manrope-Bold"):
        pdfmetrics.registerFont(TTFont(name, str(ROOT / "fonts" / f"{name}.ttf")))

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    qr.make_image(image_factory=SvgPathImage).save(ROOT / "assets" / "qr.svg")

    output = ROOT / "print"
    output.mkdir(exist_ok=True)
    write_pdf(output / "cartao-rafael-suarez-frente.pdf", [front], qr)
    write_pdf(output / "cartao-rafael-suarez-verso.pdf", [back], qr)
    write_pdf(output / "cartao-rafael-suarez-frente-verso.pdf", [front, back], qr)


if __name__ == "__main__":
    main()
