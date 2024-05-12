import React, { useState } from 'react';
import './imageUpload.css';

function ImageUploadComponent() {
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file && (file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif' || file.type === 'image/bmp')) {
            setImage(file);
            setPreviewUrl(URL.createObjectURL(file));
            setUploadedImageUrl(null);  // Reset the uploaded image URL for new uploads
        } else {
            alert('Please upload a JPG image.');
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (image) {
            const formData = new FormData();
            formData.append('file', image);
    
            try {
                const response = await fetch('http://localhost:8000/predict', {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setUploadedImageUrl(url);
                setImage(null);  // Clear the current image
                setPreviewUrl(null);  // Clear the preview
            } catch (error) {
                console.error('Error submitting image:', error);
                alert('Failed to upload image.');
            }
        }
    };

    return (
        <div>
            <div className="container">
                <h3 className='processedText'>Upload Image:</h3>
                <p>Supported Image Formats: jpeg, png, gif, bmp</p>
                <form onSubmit={handleSubmit} className="form">
                    <input type="file" accept="image/jpeg, image/png, image/gif, image/bmp" onChange={handleFileChange} className="inputFile" />

                    {previewUrl && <img src={previewUrl} alt="Preview" className="previewImage" />}
                    <button type="submit" className="submitButton" disabled={!image}>Upload Image</button>
                </form>
                {uploadedImageUrl && (
                    <div>
                        <h3 className='processedText'>Model Reuslts:</h3>
                        <img src={uploadedImageUrl} alt="Processed" className="processedImage" />
                    </div>
                )}
            </div>
        </div>
       
    );
}

export default ImageUploadComponent;
