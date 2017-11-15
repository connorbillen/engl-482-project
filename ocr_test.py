try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

print(pytesseract.image_to_string(Image.open('english1.gif')))
# print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
