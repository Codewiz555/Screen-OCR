# Screen-OCR
A simple interactive screen capture application use to copy text form any window. 


**steps **
1.Install Python (3.8+)
2.Install Tesseract OCR:

Download from: https://github.com/UB-Mannheim/tesseract/wiki
3. Install, note the path (e.g., C:\Program Files\Tesseract-OCR\tesseract.exe)
4. Install Python libraries:
pip install PyQt5 mss pytesseract Pillow pyperclip
5. Set Tesseract path in code:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
