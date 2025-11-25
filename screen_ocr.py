import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QTextEdit, QVBoxLayout, QWidget, QLabel, QShortcut)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QKeySequence
import pyautogui
import pytesseract
from PIL import Image
import pyperclip

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\AQUA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class SelectionOverlay(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        self.setMouseTracking(True)
        
        self.start_pos = None
        self.end_pos = None
        self.drawing = False
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.drawing = True
            
    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_pos = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.end_pos = event.pos()
            self.drawing = False
            self.capture_region()
            self.close()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.fillRect(rect, QColor(255, 255, 255, 0))
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(rect)
            
    def capture_region(self):
        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos).normalized()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            
            if w > 0 and h > 0:
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                self.parent.process_image(screenshot)

class ScreenOCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Screen OCR Text Extractor')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.dragging = False
        self.offset = QPoint()
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        self.label = QLabel('Click "Select Region" or press Ctrl+Shift+S to capture')
        layout.addWidget(self.label)
        
        self.capture_btn = QPushButton('Select Region to Capture')
        self.capture_btn.clicked.connect(self.start_selection)
        layout.addWidget(self.capture_btn)
        
        # Add global shortcut
        self.shortcut = QShortcut(QKeySequence('Ctrl+Shift+S'), self)
        self.shortcut.activated.connect(self.start_selection)
        
        # Close button
        self.close_btn = QPushButton('X')
        self.close_btn.setMaximumWidth(30)
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(False)
        layout.addWidget(self.text_area)
        
        self.copy_btn = QPushButton('Copy Selected Text')
        self.copy_btn.clicked.connect(self.copy_text)
        layout.addWidget(self.copy_btn)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
    def start_selection(self):
        self.hide()
        self.overlay = SelectionOverlay(self)
        self.overlay.show()
        
    def process_image(self, img):
        self.show()
        self.label.setText('Processing...')
        QApplication.processEvents()
        
        try:
            text = pytesseract.image_to_string(img)
            self.text_area.setText(text)
            self.label.setText('Text extracted! Select and copy what you need.')
        except Exception as e:
            self.label.setText(f'Error: {str(e)}')
            self.text_area.setText(f'Error: {str(e)}')
    
    def copy_text(self):
        selected = self.text_area.textCursor().selectedText()
        if selected:
            pyperclip.copy(selected)
            self.label.setText('Copied to clipboard!')
        else:
            self.label.setText('No text selected. Select text first.')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenOCRApp()
    window.show()
    sys.exit(app.exec_())