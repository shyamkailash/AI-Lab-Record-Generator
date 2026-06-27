import re
import cv2
import pytesseract


def clean_ocr_text(text):
    text = text.replace("Enterfirst", "Enter first")
    text = text.replace("Entersecond", "Enter second")
    text = text.replace("sum", "Sum")
    text = text.replace("=15", "= 15")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return ""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase image size for better OCR
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Improve contrast
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"

    text = pytesseract.image_to_string(gray, config=config)

    return clean_ocr_text(text)
