import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

data = pd.read_csv("test.csv")
lis = data['Name'].tolist()
i = 1
le = len(lis)

for name in lis:
    pdfmetrics.registerFont(TTFont('roboto', 'roboto.ttf'))
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('roboto', 30)
    can.drawCentredString(430, 325, name.upper())
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("template.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(f"./pdfs/FLOSSMeet22 {name.upper()}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    print(f"Generated {i}/{le}...")
    i += 1
print("Done!")
