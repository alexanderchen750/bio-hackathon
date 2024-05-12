from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import predict  # Assuming predict.py has been renamed to predictor.py

app = Flask(__name__)
CORS(app)


@app.route('/predict', methods=['POST'])
def predict_tumor():
    if 'file' not in request.files:
        return "No file provided", 400
    
    file = request.files['file']
    if file:
        try:
            # Open the image file and convert it to RGB (necessary for JPEG)
            image = Image.open(file.stream).convert('RGB')
            
            # Create a BytesIO object to save the converted image
            jpg_buffer = io.BytesIO()
            
            # Save the image as JPEG to the buffer
            image.save(jpg_buffer, 'JPEG', quality=90)  # Adjust quality as needed
            jpg_buffer.seek(0)  # Rewind the buffer to the start

            # Pass the JPEG buffer to the prediction function
            # Assumption: predict.predict_tumor accepts a bytes buffer and returns a PNG image buffer
            image_buffer = predict.predict_tumor(jpg_buffer)
            image_buffer.seek(0)  # Ensure the buffer's read pointer is at the start
            
            # Return the PNG image as a downloadable file
            return send_file(image_buffer, mimetype='image/png', as_attachment=True, download_name="prediction.png")
        except Exception as e:
            print(e)  # Print the error to the console or log it as appropriate
            return "Failed to process the image", 500
    return "No file content", 400



if __name__ == '__main__':
    app.run(port=8000)
