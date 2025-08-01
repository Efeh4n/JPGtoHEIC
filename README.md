# JPG → HEIC Bulk Converter

A simple Python script that:

1. Prompts you for a folder path containing `.jpg` / `.jpeg` images.  
2. Recursively finds all JPEG files under that folder.  
3. Converts each to HEIC format (preserving EXIF metadata).  
4. Saves every `.heic` into a single `heic` folder on your Desktop (handles both standard and OneDrive–redirected Desktops).  
5. Opens the output folder automatically on Windows.

Ideal for reducing JPEG file sizes while maintaining quality, and batch–processing your photo archives in one click.

---

## 📦 Prerequisites

- Python 3.7+  
- `pip install -r requirements.txt`

---

## 🔧 Installation

1. **Clone or download** this repo.  
2. Ensure your virtual environment is active (recommended).  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
