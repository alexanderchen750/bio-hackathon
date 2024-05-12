import requests

url = 'http://127.0.0.1:8000/predict'
files = {'file': open('/Users/alexanderchen/CS-Projects/Bio-Hack/CNN-Brain-Tumor-MRI-Classification/backend/test.jpg', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('output_image.png', 'wb') as f:
        f.write(response.content)
    print("Image saved successfully.")
else:
    print("Failed to get prediction.")
