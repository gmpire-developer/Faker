from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import io
import pdfrw
from django.contrib.staticfiles import finders
from fpdf import FPDF
import qrcode

# Create your views here.
def home(request):
    return render(request, 'home.html')


def generate(request):
    # If GET request without form submission, show the form
    if request.method == 'GET':
        return render(request, 'generate.html')
    
    # Handle POST request with form data
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)
    
    # Extract form data
    photo = request.FILES.get('photo')
    name_hindi = request.POST.get('name_hindi', '')
    name_english = request.POST.get('name_english', '')
    dob = request.POST.get('dob', '')
    
    # Handle gender dropdown selection
    gender_selection = request.POST.get('gender', '')
    if gender_selection == 'male':
        gender_hindi = 'पुरुष'
        gender_english = 'MALE'
    elif gender_selection == 'female':
        gender_hindi = 'महिला'
        gender_english = 'FEMALE'
    else:
        gender_hindi = ''
        gender_english = ''
    
    # Relation field
    relation = request.POST.get('relation', '')
    
    # Guardian names
    guardian_hindi = request.POST.get('guardian_hindi', '')
    guardian_english = request.POST.get('guardian_english', '')

    
    aadhaar_number = request.POST.get('aadhaar_number', '')
    vid_number = request.POST.get('vid_number', '')
    issue_date = request.POST.get('issue_date', '')
    details_date = request.POST.get('details_date', '')
    
    # Location fields
    village_town_hindi = request.POST.get('village_town_hindi', '')
    village_town_english = request.POST.get('village_town_english', '')
    po_hindi = request.POST.get('po_hindi', '')
    po_english = request.POST.get('po_english', '')
    dist_hindi = request.POST.get('dist_hindi', '')
    dist_english = request.POST.get('dist_english', '')
    state_english = request.POST.get('state', '')
    state_hindi = request.POST.get('state_hindi', '')
    pincode = request.POST.get('pincode', '')
    
    if not photo:
        return HttpResponse('Photo is required', status=400)

    # Locate static files
    blank_pdf_path = finders.find('blank.pdf')

    if not blank_pdf_path:
        return HttpResponse('Static file blank.pdf not found', status=404)

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
    liberation_sans_bold_path = fonts_dir / 'LiberationSans-Bold.ttf'

    # Add fonts to fpdf2 with text shaping enabled
    if noto_sans_deva_path.exists():
        pdf.add_font('NotoSansDeva', style='', fname=str(noto_sans_deva_path))
    if noto_serif_path.exists():
        pdf.add_font('NotoSerif', style='', fname=str(noto_serif_path))
    if ibm_plex_path.exists():
        pdf.add_font('IBMPlex', style='', fname=str(ibm_plex_path))
    if liberation_sans_bold_path.exists():
        pdf.add_font('LiberationSansBold', style='', fname=str(liberation_sans_bold_path))

    # Enable text shaping for proper Devanagari ligatures when available
    if hasattr(pdf, 'set_text_shaping'):
        pdf.set_text_shaping(True)

    # Helper to convert inches to mm
    def in_to_mm(inches):
        return inches * 25.4

    # Add vertical text "Details as on: DD/MM/YYYY"
    details_text = f"Details as on: {details_date}"
    details_x_mm = in_to_mm(2.584)
    details_y_mm = in_to_mm(7.613)
    details_font_size = 5.3
    
    if liberation_sans_bold_path.exists():
        pdf.set_font('LiberationSansBold', size=details_font_size)
        # Use text rotation to display vertically (90 degrees rotation)
        # fpdf2 rotation parameter rotates the text
        pdf.set_xy(details_x_mm, details_y_mm)
        # Rotate text 90 degrees counterclockwise
        with pdf.rotation(90, x=details_x_mm, y=details_y_mm):
            pdf.cell(0, 0, details_text)

    # Add vertical text "Aadhaar no. issued: DD/MM/YYYY"
    aadhaar_issued_text = f"Aadhaar no. issued: {issue_date}"
    aadhaar_x_mm = in_to_mm(2.595)
    aadhaar_y_mm = in_to_mm(3.928)
    
    if liberation_sans_bold_path.exists():
        pdf.set_font('LiberationSansBold', size=details_font_size)
        pdf.set_xy(aadhaar_x_mm, aadhaar_y_mm)
        with pdf.rotation(90, x=aadhaar_x_mm, y=aadhaar_y_mm):
            pdf.cell(0, 0, aadhaar_issued_text)

    # Add uploaded image at specified position
    x_start_mm = in_to_mm(2.763)
    y_start_mm = in_to_mm(2.874)
    width_mm = in_to_mm(3.481 - 2.763)
    height_mm = in_to_mm(3.739 - 2.874)
    
    # Save uploaded photo temporarily
    photo_bytes = io.BytesIO(photo.read())
    pdf.image(photo_bytes, x=x_start_mm, y=y_start_mm, w=width_mm, h=height_mm)

    # Add 12-digit number (centered, NotoSerif, 11pt)
    pdf.set_font('NotoSerif', size=11)
    text_number = aadhaar_number
    text_y_mm = in_to_mm(4.241)
    
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
        (name_hindi, True),
        (name_english, False),
        (f"जन्म तिथि/DOB : {dob}", True),
        (f"{gender_hindi}/{gender_english}", True)
    ]
    
    for i, (line, is_hindi) in enumerate(details_lines):
        y_pos = details_y_mm + (i * line_height_mm)
        
        if is_hindi:
            pdf.set_font('NotoSansDeva', size=font_size)
        else:
            pdf.set_font('IBMPlex', size=font_size)
        
        pdf.set_xy(details_x_mm, y_pos)
        pdf.cell(0, 0, line)

    # Add address section
    addr_x_mm = in_to_mm(2.645)
    addr_y_mm = in_to_mm(6.524)
    addr_max_width_mm = in_to_mm(4.450 - 2.645)
    addr_line_height_mm = in_to_mm(0.10)
    
    address_lines = [
        ("पता:", True),
        ("द्वारा: " + guardian_hindi + (", ") + village_town_hindi + (", ") + po_hindi + (", ") + dist_hindi, True),
        (state_hindi + " - " + pincode, True),
        ("", False),  # Empty line for gap
        ("Address:", False),
        (relation + "/O: " + guardian_english + (", ") + village_town_english + (", PO: ") + po_english + (",DIST: ") + dist_english, False),
        (state_english + (" - ") + pincode, False) 
    ]
    
    for i, (line, is_hindi) in enumerate(address_lines):
        if not line:  # Empty line for gap
            addr_y_mm += addr_line_height_mm
            continue
            
        if is_hindi:
            pdf.set_font('NotoSansDeva', size=font_size)
        else:
            pdf.set_font('IBMPlex', size=font_size)
        
        pdf.set_xy(addr_x_mm, addr_y_mm)
        pdf.multi_cell(addr_max_width_mm, addr_line_height_mm, line, align='L')
        
        # Update Y position to current position after multi_cell
        addr_y_mm = pdf.get_y()

    # Generate QR code
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=0,
    )
    qr.add_data(text_number)  # Use 12-digit number as QR data
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR to temporary bytes
    qr_bytes = io.BytesIO()
    qr_img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)
    
    # Place QR code at specified position
    qr_x_start_mm = in_to_mm(5.132)
    qr_y_start_mm = in_to_mm(3.416)
    qr_width_mm = in_to_mm(5.723 - 5.132)
    qr_height_mm = in_to_mm(3.997 - 3.416)
    
    pdf.image(qr_bytes, x=qr_x_start_mm, y=qr_y_start_mm, w=qr_width_mm, h=qr_height_mm)

    # Place second QR code (back) at specified position
    qr_x_start_back_mm = in_to_mm(4.617)
    qr_y_start_back_mm = in_to_mm(6.506)
    qr_width_back_mm = in_to_mm(5.884 - 4.617)
    qr_height_back_mm = in_to_mm(7.769 - 6.506)
    
    pdf.image(qr_bytes, x=qr_x_start_back_mm, y=qr_y_start_back_mm, w=qr_width_back_mm, h=qr_height_back_mm)

    # Add 12-digit number at bottom (centered, NotoSerif, 11pt)
    pdf.set_font('NotoSerif', size=11)
    text_y_bottom_mm = in_to_mm(7.877)
    
    # Center text
    text_width_bottom = pdf.get_string_width(text_number)
    centered_x_bottom = (page_width_mm - text_width_bottom) / 2
    pdf.set_xy(centered_x_bottom, text_y_bottom_mm)
    pdf.cell(text_width_bottom, 0, text_number, align='C')

    # Add VID line with mixed fonts
    vid_y_mm = in_to_mm(8.037)
    vid_font_size = 7.3
    
    # Start with IBM font for "VID :"
    pdf.set_font('IBMPlex', size=vid_font_size)
    vid_label = "VID : "
    vid_x_start = (page_width_mm - pdf.get_string_width(vid_label + vid_number)) / 2
    pdf.set_xy(vid_x_start, vid_y_mm)
    pdf.cell(pdf.get_string_width(vid_label), 0, vid_label)
    
    # Continue with NotoSerif for numbers
    pdf.set_font('NotoSerif', size=vid_font_size)
    pdf.cell(pdf.get_string_width(vid_number), 0, vid_number)
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
