# 🎫 Aadhaar Faker - PDF Generator

A simple, user-friendly application to generate realistic **fake Aadhaar PDF cards** for testing and development purposes. Perfect for QA teams, developers, and testing scenarios where sample Aadhaar data is needed.

---

## 🌟 Features

### ✨ Easy-to-Use Form
Fill in a simple form with all Aadhaar details and generate a professional PDF instantly.

### 🌐 Bilingual Support (English & Hindi)
- **English fields** for typing
- **Hindi fields** with **automatic English-to-Hindi transliteration**
- Type in English → automatically converts to Hindi on blur
- **Edit mode**: Click the Hindi field again to see English and edit

### 🖼️ Photo Upload
- Upload your photo in JPG or PNG format
- Photo is automatically embedded in the generated PDF
- Max file size: 5MB

### 📋 Complete Aadhaar Information
- **Personal Information**: Name, Date of Birth, Gender, Guardian Details
- **Location Data**: Village/Town, Post Office, District, State, PIN Code
- **Aadhaar Details**: Aadhaar Number, VID Number, Issue Date
- **Professional PDF Output**: A4 format with proper formatting

### 🎯 Smart Features
- **Date Pickers**: Easy date selection for DOB and issue dates
- **Auto-formatting**: Aadhaar and VID numbers format automatically
- **PIN Code Validation**: Only accepts 6-digit PIN codes
- **Real-time Validation**: Form validates data before submission
- **QR Codes**: Automatically generates QR codes on the PDF
- **Download/Preview**: Preview the PDF before downloading

---

## 🚀 How to Use

### 1. **Navigate to Generate Page**
   - Open the application and click **"Generate Now"** button
   - Or go to the **Generate** menu option

### 2. **Upload a Photo**
   - Click the photo upload area or **"Click to upload photo"**
   - Select a JPG or PNG image from your device
   - Confirm the filename appears below the upload box

### 3. **Fill in Personal Information**
   - **Name (English)**: Type your name in English
   - **Name (Hindi)**: Type in English → press Tab/blur → auto-converts to Hindi
   - **Date of Birth**: Click the date field and select from the calendar
   - **Gender**: Select Male or Female from the dropdown
   - **Guardian Name (English)**: Type guardian's name
   - **Guardian Name (Hindi)**: Type in English → auto-converts to Hindi
   - **Relation**: Select Child or Wife

### 4. **Enter Aadhaar & VID Details**
   - **Aadhaar Number**: Enter 12 digits (formats as XXXX XXXX XXXX automatically)
   - **VID Number**: Enter 16 digits (formats as XXXX XXXX XXXX XXXX automatically)
   - **Aadhaar Issue Date**: Click and select from calendar
   - **Details As On Date**: Click and select from calendar

### 5. **Enter Location Information**
   - **Village/Town (English & Hindi)**: Your village/town name
   - **Post Office (English & Hindi)**: Your post office name
   - **District (English & Hindi)**: Your district name
   - **State**: Select from the dropdown → Hindi automatically updates
   - **PIN Code**: Enter 6-digit PIN code (formats automatically)

### 6. **Generate PDF**
   - Click the **"✨ Generate Aadhaar PDF"** button
   - Wait for processing (shows loading spinner)
   - Success message appears with two options:
     - **👁️ Preview PDF**: View the PDF in your browser
     - **💾 Download PDF**: Download to your device

---

## 💡 Pro Tips

### **Editing Hindi Text**
- After typing English and it converts to Hindi, **click on the Hindi field again**
- The original English text appears for editing
- Make changes and it will re-transliterate to Hindi on blur
- This works automatically with the stored English version

### **Auto-Translation**
- **Does NOT require internet** - Has offline fallback transliteration
- **Smart conversion** - Transliterates standard English spellings to Hindi
- **Examples**:
  - "Pargat" → "प्रगत"
  - "Singh" → "सिंह"
  - "Rajasthan" → "राजस्थान"

### **Keyboard Shortcuts**
- Use **Tab key** to move to the next field and trigger Hindi conversion
- Use **Enter key** in date fields to confirm selection

### **Browser Tips**
- **Chrome/Edge**: Best performance and compatibility
- **Mobile**: Responsive design works on tablets and phones
- **Dark Mode**: Works with system dark mode (displays normally)

---

## 📝 Field Descriptions

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| Photo | ✅ | JPG, PNG (≤5MB) | portrait.jpg |
| Name (English) | ✅ | Text | Pargat Singh |
| Name (Hindi) | ✅ | Auto from English | प्रगत सिंह |
| DOB | ✅ | DD/MM/YYYY | 15/06/1990 |
| Gender | ✅ | Dropdown | Male/Female |
| Guardian (English) | ✅ | Text | Sukhdeep Singh |
| Guardian (Hindi) | ✅ | Auto from English | सुखदीप सिंह |
| Relation | ✅ | Dropdown | Child/Wife |
| Aadhaar Number | ✅ | 12 digits | 4367 7667 5676 |
| VID Number | ✅ | 16 digits | 7746 7469 2816 3571 |
| Issue Date | ✅ | DD/MM/YYYY | 01/01/2020 |
| Details As On | ✅ | DD/MM/YYYY | 01/01/2025 |
| Village/Town | ✅ | Text | Muklawa |
| Post Office | ✅ | Text | Raisinghnagar |
| District | ✅ | Text | Sri Ganganagar |
| State | ✅ | Dropdown | Rajasthan |
| PIN Code | ✅ | 6 digits | 335039 |

---

## ❓ Frequently Asked Questions

### **Q: Is this for creating real Aadhaar cards?**
A: **No.** This is for testing and development purposes only. Generated PDFs contain fake data and are not valid government documents.

### **Q: Does the transliteration work without internet?**
A: **Yes!** The app has two translation modes:
1. **Online** (preferred) - Uses Google Input Tools API for accurate translation
2. **Offline** (automatic fallback) - Built-in transliteration if API is unavailable

### **Q: Can I edit the PDF after downloading?**
A: The generated PDF is a completed image-based document. To make changes, return to the form, update the fields, and generate a new PDF.

### **Q: What happens if I refresh the page?**
A: The form clears (by design). You'll need to refill all fields and regenerate. The generated PDF link remains available in the current session.

### **Q: Can I generate multiple PDFs?**
A: Yes! Generate as many as you need. Each submission creates a new PDF.

### **Q: Why doesn't the Hindi field show my text?**
A: This is intentional. The Hindi field displays the Hindi translation of your English input. Click the field again to see and edit the English version.

### **Q: Can I use special characters?**
A: Yes, the form supports standard English and Hindi text. Avoid excessive special characters or emojis for best results.

### **Q: What if the photo doesn't appear in the PDF?**
A: Ensure:
- File is in JPG or PNG format
- File size is under 5MB
- File uploads successfully (filename appears below upload box)
- Try a different image if it still fails

### **Q: How accurate is the translation?**
A: The Google Input Tools API provides accurate transliteration for standard Hindi names and words. The offline fallback handles common patterns but may not be perfect for complex words.

---

## 🛠️ Technical Details

### **Technologies Used**
- **Backend**: Django 6.0 (Python)
- **Frontend**: Tailwind CSS, Flatpickr date picker
- **PDF Generation**: fpdf2 with custom fonts
- **QR Code**: qrcode library
- **Transliteration**: Google Input Tools API + offline fallback

### **Supported Fonts**
- Devanagari (Hindi): Noto Sans Devanagari
- English: IBM Plex Sans, Liberation Sans, Noto Serif

### **Browser Requirements**
- Modern browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Supports mobile/tablet browsers

---

## 📧 Disclaimer

⚠️ **For Testing Purposes Only**

This application generates fake Aadhaar PDF samples for:
- Software testing and QA
- Development and integration testing
- UI/UX testing
- Education and demonstration

**NOT for:**
- Creating forged government documents
- Deceptive purposes
- Fraud or illegal activities

All generated documents are clearly fake and should only be used in authorized testing environments.

---

## 🎯 Getting Started

1. **Visit the Application**
   - Open your browser and navigate to the application URL

2. **Click "Generate Now"**
   - Go to the Generate page from the navigation menu

3. **Fill the Form**
   - Complete all required fields marked with red asterisk (*)

4. **Generate**
   - Click "✨ Generate Aadhaar PDF" button

5. **Download or Preview**
   - Download the PDF or preview it in your browser

---

## 💬 Tips for Best Results

✅ **Do:**
- Use realistic names and locations
- Provide valid date formats
- Ensure photos are clear and properly formatted
- Test with various Indian states and districts

❌ **Don't:**
- Use extremely long names
- Upload corrupted image files
- Use invalid date combinations
- Share generated PDFs as real documents

---

## 📞 Support

If you encounter any issues:
1. **Refresh the page** and try again
2. **Check your internet connection** (for Google API transliteration)
3. **Clear browser cache** if styling looks off
4. **Ensure JavaScript is enabled** in your browser settings
5. **Try a different browser** if issues persist

---

**Version**: 1.0  
**Status**: Active & Maintained

---

*Generated Aadhaar PDFs are for authorized testing use only.*
