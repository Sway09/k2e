from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import base64
import io
import os
from googletrans import Translator

app = Flask(__name__)

# Set the TESSDATA_PREFIX environment variable dynamically
TESSDATA_PREFIX = os.path.join(os.getcwd(), "tessdata")

# Set the Tesseract binary path based on the environment
if os.path.exists( '/usr/local/bin/tesseract' ):
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # Local path for macOS/Linux
elif os.path.exists( '/usr/bin/tesseract' ):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Path for Render/Linux environments
else:
    raise EnvironmentError( "Tesseract not found. Please install Tesseract and set the correct path." )
# Adjust this if necessary
os.environ['TESSDATA_PREFIX'] = TESSDATA_PREFIX

# Initialize the translator
translator = Translator()

# OCR Function to process image from base64 string
def ocr_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    # Perform OCR with the Kannada language
    text = pytesseract.image_to_string(image, lang="kan")  # Kannada OCR
    return text

# Translation function to translate Kannada text to English
def translate_to_english(text):
    translated = translator.translate(text, src='kn', dest='en')  # 'kn' for Kannada, 'en' for English
    return translated.text

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the image upload and perform OCR
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the image from the request
        image_data = request.json['image']

        # Decode the base64 image
        image_data = base64.b64decode(image_data.split(',')[1])

        # Perform OCR on the image
        extracted_text = ocr_from_image(image_data)

        # Translate the extracted Kannada text to English
        translated_text = translate_to_english(extracted_text)

        # Return the translated text
        return jsonify({"text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
