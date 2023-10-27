from PIL import Image
import pytesseract

path_to_tesseract = r"C:\Program Files\Tesseract-OCR"
image_path = r"screenshot_simulator/itm_done.PNG"


# Opening the image & storing it in an image object
img = Image.open(image_path)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text[:-1])