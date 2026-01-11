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

    # Read base PDF
    base_pdf = pdfrw.PdfReader(blank_pdf_path)
    if not base_pdf.pages:
        return HttpResponse('Base PDF has no pages', status=400)

    first_page = base_pdf.pages[0]
    # Determine page size from MediaBox
    try:
        mbox = [float(v) for v in first_page.MediaBox]
        page_width = mbox[2] - mbox[0]
        page_height = mbox[3] - mbox[1]
    except Exception:
        page_width, page_height = A4  # fallback

    # Create overlay PDF with the image using ReportLab
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Helpers: convert top-left coordinates to ReportLab bottom-left
    def inches(val: float) -> float:
        return val * inch

    def top_left_to_bottom_left_y(page_h_pts: float, top_y_in: float, h_in: float) -> float:
        return page_h_pts - inches(top_y_in) - inches(h_in)

    # Exact bounding box (top-left reference)
    x_start = 2.763
    x_end = 3.481
    y_start = 2.874
    y_end = 3.739

    # Calculate position and dimensions
    x_in = x_start
    y_top_in = y_start
    width_in = x_end - x_start
    height_in = y_end - y_start

    x_pts = inches(x_in)
    y_pts = top_left_to_bottom_left_y(page_height, y_top_in, height_in)
    width_pts = inches(width_in)
    height_pts = inches(height_in)

    # Read image and draw resized at target rectangle
    img_reader = ImageReader(img_path)
    c.drawImage(img_reader, x_pts, y_pts, width=width_pts, height=height_pts, mask='auto')

    # Register fonts with absolute paths
    from pathlib import Path
    import logging
    logger = logging.getLogger(__name__)
    
    fonts_dir = settings.BASE_DIR / 'static' / 'fonts'
    noto_sans_deva_path = fonts_dir / 'NotoSansDevanagari-Regular.ttf'
    noto_serif_path = fonts_dir / 'NotoSerif-Regular.ttf'
    ibm_plex_path = fonts_dir / 'IBMPlexSansCondensed-Regular.ttf'

    hindi_font = 'Helvetica'
    english_font = 'Helvetica'
    noto_serif_font = 'Helvetica'

    # Log font paths
    print(f"\n=== FONT REGISTRATION ===")
    print(f"Fonts directory: {fonts_dir}")
    print(f"NotoSansDevanagari path: {noto_sans_deva_path} (exists: {noto_sans_deva_path.exists()})")
    print(f"NotoSerif path: {noto_serif_path} (exists: {noto_serif_path.exists()})")
    print(f"IBMPlex path: {ibm_plex_path} (exists: {ibm_plex_path.exists()})")

    # Register NotoSansDevanagari for Hindi
    if noto_sans_deva_path.exists():
        pdfmetrics.registerFont(TTFont('NotoSansDeva', str(noto_sans_deva_path)))
        hindi_font = 'NotoSansDeva'
        print(f"✓ Registered NotoSansDeva for Hindi from: {noto_sans_deva_path}")
    else:
        print(f"✗ NotoSansDevanagari NOT found at: {noto_sans_deva_path}")

    # Register NotoSerif for the 12-digit number
    if noto_serif_path.exists():
        pdfmetrics.registerFont(TTFont('NotoSerif', str(noto_serif_path)))
        noto_serif_font = 'NotoSerif'
        print(f"✓ Registered NotoSerif for numbers from: {noto_serif_path}")
    else:
        print(f"✗ NotoSerif NOT found at: {noto_serif_path}")

    # Register IBM Plex for English
    if ibm_plex_path.exists():
        pdfmetrics.registerFont(TTFont('IBMPlex', str(ibm_plex_path)))
        english_font = 'IBMPlex'
        print(f"✓ Registered IBMPlex for English from: {ibm_plex_path}")
    else:
        print(f"✗ IBMPlex NOT found at: {ibm_plex_path}")
    
    print(f"\nFinal font assignments:")
    print(f"  Hindi: {hindi_font}")
    print(f"  English: {english_font}")
    print(f"  Number: {noto_serif_font}")
    print(f"========================\n")

    font_size = 6.3

    # Helper to detect if text contains Devanagari characters
    def contains_hindi(text):
        return any('\u0900' <= char <= '\u097F' for char in text)

    # Add text: 12-digit number (centered horizontally)
    text_number = "4367 7667 5676"
    text_y = 4.271
    number_font_size = 11

    c.setFont(noto_serif_font, number_font_size)
    # For text, y coordinate is baseline, so we convert top-left to bottom-left with 0 height
    text_y_pts = top_left_to_bottom_left_y(page_height, text_y, 0)
    
    # Center horizontally on page
    text_width = c.stringWidth(text_number, noto_serif_font, number_font_size)
    centered_x = (page_width - text_width) / 2
    c.drawString(centered_x, text_y_pts, text_number)

    # Add personal details at x:3.600in, y:2.960in (multi-line)
    details_x = 3.600
    details_y = 2.980
    line_height = 0.12  # spacing between lines in inches
    
    details_lines = [
        "गुरविन्द्र सिंह",
        "Gurvinder Singh",
        "जन्म तिथि/DOB : 27/07/1999",
        "पुरुष/MALE"
    ]
    
    # Render Hindi text as images to properly support Devanagari
    noto_sans_path_full = finders.find('NotoSans-Regular.ttf')
    ibm_plex_path_full = finders.find('IBMPlexSansCondensed-Regular.ttf')
    
    for i, line in enumerate(details_lines):
        is_hindi = contains_hindi(line)
        
        line_y = details_y + (i * line_height)
        line_y_pts = top_left_to_bottom_left_y(page_height, line_y, 0)
        
        if is_hindi:
            # Render Hindi as image to preserve proper Devanagari shaping
            try:
                pil_font = ImageFont.truetype(str(noto_sans_deva_path), int(font_size * 2.5))
                # Create larger image for better quality
                img = Image.new('RGBA', (600, 40), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                draw.text((0, 0), line, font=pil_font, fill=(0, 0, 0, 255))
                
                # Crop to actual text bounds
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                img_reader = ImageReader(img_bytes)
                # Scale to match font_size
                c.drawImage(img_reader, inches(details_x), line_y_pts - 2, 
                           width=1.5*inch, height=0.15*inch, mask='auto', preserveAspectRatio=True)
            except Exception as e:
                # Fallback to direct text if image rendering fails
                c.setFont(hindi_font, font_size)
                c.drawString(inches(details_x), line_y_pts, line)
        else:
            # English text - direct rendering
            c.setFont(english_font, font_size)
            c.drawString(inches(details_x), line_y_pts, line)

    c.save()

    packet.seek(0)
    overlay_pdf = pdfrw.PdfReader(fdata=packet.read())

    # Merge overlay onto the first page
    from pdfrw import PageMerge, PdfWriter

    output = PdfWriter()
    overlay_page = overlay_pdf.pages[0]
    PageMerge(first_page).add(overlay_page).render()
    output.addpage(first_page)

    # Add remaining pages unchanged, if any
    for p in base_pdf.pages[1:]:
        output.addpage(p)

    result_stream = io.BytesIO()
    output.write(result_stream)
    result_stream.seek(0)

    response = HttpResponse(result_stream.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="generated.pdf"'
    return response
