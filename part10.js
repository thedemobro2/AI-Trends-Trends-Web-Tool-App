// frontend/src/pages/UploadPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [uploadError, setUploadError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadStatus('');
    setUploadError('');
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setUploadError('Please select a CSV file to upload.');
      return;
    }

    setUploadStatus('Uploading...');
    setUploadError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/upload-csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadStatus(`Upload successful! ${response.data.filename} processed.`);
      setSelectedFile(null); // Clear selected file after successful upload
      // Optionally navigate to dashboard or show a success message then prompt to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('');
      setUploadError(error.response?.data?.detail || 'File upload failed. Please try again.');
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Upload Inventory CSV</h2>
      <div className="mb-4">
        <label htmlFor="csv-upload" className="block text-gray-700 text-sm font-bold mb-2">
          Select CSV File:
        </label>
        <input
          type="file"
          id="csv-upload"
          accept=".csv"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100"
        />
      </div>
      {selectedFile && (
        <p className="text-sm text-gray-600 mb-4">Selected file: <span className="font-semibold">{selectedFile.name}</span></p>
      )}
      <button
        onClick={handleFileUpload}
        disabled={!selectedFile || uploadStatus === 'Uploading...'}
        className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700
          disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
      >
        {uploadStatus === 'Uploading...' ? 'Processing...' : 'Upload & Process'}
      </button>

      {uploadStatus && !uploadError && (
        <p className="mt-4 text-green-600 text-center font-medium">{uploadStatus}</p>
      )}
      {uploadError && (
        <p className="mt-4 text-red-600 text-center font-medium">{uploadError}</p>
      )}
    </div>
  );
}

export default UploadPage;
