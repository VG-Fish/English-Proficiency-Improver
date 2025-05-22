from typing import Self
from fpdf import FPDF
from constants import LINE_WIDTH

class PDFGenerator:
    def __init__(self: Self, input_file_name: str, output_file_name: str):
        self.input_file_name: str = input_file_name
        self.output_file_name: str = output_file_name

    def generate_pdf(self: Self):
        with open(self.input_file_name) as f:
            text: str = f.read()

        text = str(text.encode("ascii", errors="ignore")).replace("\\n", " ").replace("\'", "'")
        pdf: FPDF = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.multi_cell(w=LINE_WIDTH, h=10, text=text)
        pdf.output(self.output_file_name)
