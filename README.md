# Screen-OCR

A simple interactive screen capture application to copy text from any window.

**Download** exe for win: https://drive.google.com/file/d/1Virc39asR_F1s4TsY7fuL9rJppLf7nPI/view?usp=drive_link

## Features
- Select any region on screen to extract text
- Supports printed text, handwriting (basic), and Kannada
- Floating window with keyboard shortcut (Ctrl+Shift+S)
- Copy extracted text to clipboard

## Installation Steps

1. **Install Python (3.8+)**

2. **Install Tesseract OCR:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and note the path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)

3. **Install Python libraries:**
```bash
   pip install PyQt5 pyautogui pytesseract Pillow pyperclip opencv-python
```

4. **Update Tesseract path in code (line 13):**
```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Users\YOUR_PATH\Tesseract-OCR\tesseract.exe'
```

5. **Run:**
```bash
   python screen_ocr.py
```

## Usage
- Click "Select Region" or press `Ctrl+Shift+S`
- Drag to select area on screen
- Text appears in window - select and copy

## Build Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed screen_ocr.py
```
Executable will be in `dist/` folder.
