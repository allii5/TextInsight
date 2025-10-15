import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './AccountCreation.module.css';
import apiClient from '../apiClient';
import LoadingAnimation from '../LoadingAnimation/LoadingAnimation';

const AccountCreation = () => {
  const [studentCount, setStudentCount] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === 'text/csv') {
      setFile(droppedFile);
      setError(null);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile?.type === 'text/csv') {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSliderChange = (e) => {
    setStudentCount(e.target.value);
  };

  const downloadSample = async () => {
    try {
        const response = await apiClient.get('/auth/api/download-sample-csv/', {
            responseType: 'blob'
        });
        
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'sample_student_emails.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        setError('Error downloading sample file. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a CSV file before submitting');
      return;
    }

    setIsLoading(true); // Show loading animation

    try {
      const formData = new FormData();
      formData.append('number_of_accounts', studentCount);
      formData.append('csv_file', file);

      const response = await apiClient.post('/auth/api/create-student-accounts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob'
      });

      // Handle successful response
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'created_student_accounts.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      // Navigate after completion
      setIsLoading(false);
      navigate(-1);
    } catch (error) {
      console.error('Submission error:', error);
      setError('Error creating accounts. Please try again.');
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    navigate(-1); // Update with your cancel path
  };

  return (
    <div className={styles.container}>
      {isLoading && (
        <LoadingAnimation 
          onCompletion={() => {
            setIsLoading(false);
          }}
        />
      )}
      <form className={styles['form-card']} onSubmit={handleSubmit}>
        <h2 className={styles.title}>Create Account for Students</h2>

        <div className={styles.line}></div>

        <div className={styles.section}>
          <label className={styles['section-label']}>
            Number of Accounts
          </label>
          <p className={styles.description}>
            Use the slider to select how many student accounts you want to create (1-50).
            Each selected account will require a valid email provided in the uploaded CSV file.
          </p>
          
          <div className={styles['slider-container']}>
            <div className={styles['slider-value']}>
              {studentCount} Student{studentCount > 1 ? 's' : ''}
            </div>
            <input
              type="range"
              min="1"
              max="50"
              value={studentCount}
              onChange={handleSliderChange}
              className={styles.slider}
            />
          </div>
        </div>

        <div className={styles.section}>
          <div className={styles.header}>
            <label className={styles['section-label']}>Upload CSV File</label>
            <button
              type="button"
              onClick={downloadSample}
              className={styles['sample-button']}
            >
              Sample File
            </button>
          </div>
          
          <p className={styles.description}>
            Download the Sample CSV Template to format your data correctly.
            Ensure each row in the CSV file contains a valid email address.
            The system will create accounts for each email and send login details 
            to the provided email addresses.
          </p>

          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`${styles.dropzone} ${
              isDragging ? styles.dragging : ''
            } ${file ? styles['has-file'] : ''}`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileSelect}
              accept=".csv"
              className={styles.hidden}
            />
            <p className={styles['dropzone-text']}>
              {file ? file.name : 'Click here to upload your file or drag and drop.'}
            </p>
            <p className={styles['format-text']}>
              Supported Format (Only CSV)
            </p>
          </div>
          {error && <p className={styles['error-message']}>{error}</p>}
        </div>

        <div className={styles['button-container']}>
          <button 
            type="button"
            onClick={handleCancel}
            className={styles['cancel-button']}
          >
            Cancel
          </button>
          <button 
            type="submit"
            className={styles['submit-button']}
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default AccountCreation;