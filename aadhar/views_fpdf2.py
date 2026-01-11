from django.http import HttpResponse
from django.shortcuts import render
import os
from django.conf import settings
import io
import pdfrw
from django.contrib.staticfiles import finders
from pathlib import Path
from fpdf import FPDF
from fpdf.enums import TextEmphasis
from PIL import Image

# Create your views here.
def home(request):
    return render(request, 'home.html')


def generate(request):
    # If download query param present, return generated PDF; else show UI
    download = request.GET.get('download')

    if not download:
        return render(request, 'generate.html')

    # Locate static files
    blank_pdf_path = finders.find('blank.pdf')
    img_path = finders.find('img.jpg')

    if not blank_pdf_path:
        return HttpResponse('Static file blank.pdf not found', status=404)
    if not img_path:
        return HttpResponse('Static file img.jpg not found', status=404)

    # Read base PDF to get dimensions
    base_pdf = pdfrw.PdfReader(blank_pdf_path)
    if not base_pdf.pages:
        return HttpResponse('Base PDF has no pages', status=400)

    first_page = base_pdf.pages[0]
    try:
        mbox = [float(v) for v in first_page.MediaBox]
        page_width_pts = mbox[2] - mbox[0]
        page_height_pts = mbox[3] - mbox[1]
        page_width_mm = page_width_pts * 0.352778  # pts to mm
        page_height_mm = page_height_pts * 0.352778
    except Exception:
        page_width_mm, page_height_mm = 210, 297  # A4 fallback

    # Create overlay PDF using fpdf2
    pdf = FPDF(unit='mm', format=(page_width_mm, page_height_mm))
    pdf.add_page()
    
    # Set up fonts directory
    fonts_dir = settings.BASE_DIR / 'static' / 'fonts'
    noto_sans_deva_path = fonts_dir / 'NotoSansDevanagari-Regular.ttf'
    noto_serif_path = fonts_dir / 'NotoSerif-Regular.ttf'
    ibm_plex_path = fonts_dir / 'IBMPlexSansCondensed-Regular.ttf'

    # Add fonts to fpdf2 with text shaping enabled
    if noto_sans_deva_path.exists():
        pdf.add_font('NotoSansDeva', style='', fname=str(noto_sans_deva_path))
    if noto_serif_path.exists():
        pdf.add_font('NotoSerif', style='', fname=str(noto_serif_path))
    if ibm_plex_path.exists():
        pdf.add_font('IBMPlex', style='', fname=str(ibm_plex_path))

    # Helper to convert inches to mm
    def in_to_mm(inches):
        return inches * 25.4

    # Add image at specified position
    x_start_mm = in_to_mm(2.763)
    y_start_mm = in_to_mm(2.874)
    width_mm = in_to_mm(3.481 - 2.763)
    height_mm = in_to_mm(3.739 - 2.874)
    
    pdf.image(img_path, x=x_start_mm, y=y_start_mm, w=width_mm, h=height_mm)

    # Add 12-digit number (centered, NotoSerif, 11pt)
    pdf.set_font('NotoSerif', size=11)
    text_number = "4367 7667 5676"
    text_y_mm = in_to_mm(4.271)
    
    # Center text
    text_width = pdf.get_string_width(text_number)
    centered_x = (page_width_mm - text_width) / 2
    pdf.set_xy(centered_x, text_y_mm)
    pdf.cell(text_width, 0, text_number, align='C')

    # Add personal details
    details_x_mm = in_to_mm(3.600)
    details_y_mm = in_to_mm(2.980)
    line_height_mm = in_to_mm(0.12)
    font_size = 6.3
    
    details_lines = [
        ("गुरविन्द्र सिंह", True),
        ("Gurvinder Singh", False),
        ("जन्म तिथि/DOB : 27/07/1999", True),
        ("पुरुष/MALE", True)
    ]
    
    for i, (line, is_hindi) in enumerate(details_lines):
        y_pos = details_y_mm + (i * line_height_mm)
        
        if is_hindi:
            pdf.set_font('NotoSansDeva', size=font_size)
        else:
            pdf.set_font('IBMPlex', size=font_size)
        
        pdf.set_xy(details_x_mm, y_pos)
        pdf.cell(0, 0, line)

    # Save overlay PDF to bytes
    overlay_bytes = pdf.output()
    overlay_stream = io.BytesIO(overlay_bytes)
    overlay_pdf = pdfrw.PdfReader(fdata=overlay_stream.read())

    # Merge overlay onto base PDF
    from pdfrw import PageMerge, PdfWriter
    
    output = PdfWriter()
    overlay_page = overlay_pdf.pages[0]
    PageMerge(first_page).add(overlay_page).render()
    output.addpage(first_page)

    # Add remaining pages from base PDF
    for p in base_pdf.pages[1:]:
        output.addpage(p)

    # Write result
    result_stream = io.BytesIO()
    output.write(result_stream)
    result_stream.seek(0)

    response = HttpResponse(result_stream.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="generated.pdf"'
    return response
