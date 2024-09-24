from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import base64
import io

app = Flask( __name__ )


# OCR Function to process image from base64 string
def ocr_from_image(image_data):
    image = Image.open( io.BytesIO( image_data ) )
    text = pytesseract.image_to_string( image, lang="kan" )  # Kannada OCR
    return text


# Route for homepage
@app.route( '/' )
def index():
    return render_template( 'index.html' )


# Route to handle the image upload and perform OCR
@app.route( '/process_image', methods=['POST'] )
def process_image():
    try:
        # Get the image from the request
        image_data = request.json['image']

        # Decode the base64 image
        image_data = base64.b64decode( image_data.split( ',' )[1] )

        # Perform OCR on the image
        extracted_text = ocr_from_image( image_data )

        # Return the extracted text
        return jsonify( {"text": extracted_text} )
    except Exception as e:
        return jsonify( {"error": str( e )} )


if __name__ == '__main__':
    app.run( debug=True )
