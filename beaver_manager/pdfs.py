from xhtml2pdf import pisa
from StringIO import StringIO


def create_pdf(pdf_data):
    """
    Creates a PDF using the data given.

    Args:
        pdf_data: html data to be converted into a PDF

    Returns:
        pdf: a PDF file
    """
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data), pdf)
    return pdf
