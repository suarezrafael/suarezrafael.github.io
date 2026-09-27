"""Generate the website QR and print-ready, vector business cards."""

from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
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


def label(pdf, x, y, value, font="Helvetica", size=8, color=INK):
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
    pdf.setStrokeColor(HexColor("#263033"))
    pdf.setLineWidth(0.25)
    for x in range(0, 97, 5):
        pdf.line(x * mm, 0, x * mm, HEIGHT)
    for y in range(0, 57, 5):
        pdf.line(0, y * mm, WIDTH, y * mm)

    rect(pdf, 7, 7, 8, 8, HexColor("#263033"))
    rect(pdf, 11, 7, 2, 8, TEAL)
    label(pdf, 8, 12.4, "RS", "Helvetica-Bold", 9, PAPER)
    label(pdf, 18, 12, "RVS TECNOLOGIA", "Helvetica-Bold", 8.2, PAPER)
    rect(pdf, 82, 0, 2.5, 17, TEAL)
    rect(pdf, 85, 0, 1, 17, LIME)

    label(pdf, 7, 29, "RAFAEL", "Helvetica-Bold", 23, PAPER)
    label(pdf, 7, 39, "SUAREZ", "Helvetica-Bold", 23, PAPER)
    rect(pdf, 7, 42, 15, 0.8, CORAL)
    label(pdf, 7, 48, "DESENVOLVIMENTO DE SOFTWARE  /  VENÂNCIO AIRES - RS", "Helvetica-Bold", 6.5, SOFT)


def back(pdf, qr):
    rect(pdf, 0, 0, 96, 56, PAPER)
    rect(pdf, 0, 0, 3, 56, TEAL)
    rect(pdf, 3, 0, 0.8, 56, LIME)
    label(pdf, 7, 13, "Vamos conversar?", "Helvetica-Bold", 16, INK)
    rect(pdf, 7, 17, 11, 0.8, CORAL)
    label(pdf, 7, 23, "+55 (51) 99123-1245", "Helvetica-Bold", 10, INK)
    label(pdf, 7, 29, "rafaelv_s@hotmail.com", "Helvetica", 8.5, INK)
    label(pdf, 7, 35, "suarezrafael.github.io", "Helvetica", 8.5, INK)
    label(pdf, 7, 41, "github.com/suarezrafael", "Helvetica", 8.1, INK)
    label(pdf, 7, 49, "RAFAEL SUAREZ  /  RVS TECNOLOGIA", "Helvetica-Bold", 6.5, HexColor("#56646b"))
    draw_qr(pdf, qr, 65, 10, 24)
    label(pdf, 66, 38, "ABRA O CARTÃO", "Helvetica-Bold", 6.5, INK)


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
