from tensorflow.keras.models import load_model
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import io  # Import io to handle byte streams

# Load the model once when the script is imported or run
model = load_model('biohack-model.keras')

def predict_tumor(file_stream):
    classes = ['glioma', 'meningioma', 'notumor', 'pituitary']
    #for Img path
    #img = Image.open(img_path).resize((299, 299))
    img = Image.open(file_stream).resize((299, 299))
    
    # Prepare image for prediction
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make prediction
    pred = model.predict(img_array)
    prob = list(pred[0])
    
    # Create plot
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    axs[0].imshow(img)
    axs[0].axis('off')
    bars = axs[1].barh(classes, prob)
    axs[1].set_xlabel('Probability')
    axs[1].bar_label(bars, fmt='%.2f')
    
    # Save plot to a bytes buffer instead of showing it
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)  # Rewind the buffer to the start
    
    return buf

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        image_buf = predict_tumor(img_path)
        # Example of how to use the buffer to save to a file
        # with open("output_plot.png", "wb") as f:
        #     f.write(image_buf.read())
    else:
        print("Please provide an image path.")
