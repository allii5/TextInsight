import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateClass.module.css";
import apiClient from '../apiClient';
import FloatAnimation from '../FloatAnimation/FloatAnimation'; 

function CreateClass() {
  const navigate = useNavigate();
  const [classNameInput, setClassNameInput] = useState("");
  const [searchStudentInput, setSearchStudentInput] = useState("");
  const [studentsList, setStudentsList] = useState([]);
  const [recommendedStudents, setRecommendedStudents] = useState([]);
  const [studentLimit] = useState(50);
  const [errors, setErrors] = useState({});
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);

  // Drag & Drop handlers
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
    if (droppedFile?.type === "text/csv") {
      setFile(droppedFile);
      setErrors(prev => ({ ...prev, csv: "" }));
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile?.type === "text/csv") {
      setFile(selectedFile);
      setErrors(prev => ({ ...prev, csv: "" }));
    }
  };

  const downloadSample = async () => {
    try {
        const response = await apiClient.get('/classes/download-sample-csv/', {
            responseType: 'blob'
        });
        
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'class_students_template.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        setErrors(prev => ({
            ...prev,
            csv: 'Error downloading sample file'
        }));
    }
  };

  const validateForm = () => {
    let newErrors = {};
    
    if (!classNameInput.trim()) {
        newErrors.className = "Class name is required.";
    }
    
    // Check for minimum 7 students requirement
    const totalStudents = studentsList.length + (file ? 1 : 0); // We don't know exact CSV count yet
    if (totalStudents < 7) {
        newErrors.students = "At least 7 students required (add manually or upload CSV).";
    }

    // Check for maximum 50 students (though backend will handle this too)
    if (studentsList.length > 50) {
        newErrors.students = "Maximum of 50 students allowed.";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
        try {
            setIsLoading(true); // Show animation when submitting
            
            const formData = new FormData();
            formData.append('class_name', classNameInput);
            
            studentsList.forEach(username => {
                formData.append('selected_usernames', username);
            });
            
            if (file) {
                formData.append('csv_file', file);
            }

            const response = await apiClient.post('/classes/create-class/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            });

            if (response.status === 201) {
                // Wait for animation to complete before navigating
                setTimeout(() => {
                    setIsLoading(false);
                    navigate(-1);
                }, 2000);
            }
        } catch (error) {
            setIsLoading(false);
            const errorMessages = error.response?.data?.errors;
            setErrors(prev => ({
                ...prev,
                submit: Array.isArray(errorMessages) 
                    ? errorMessages.join('\n') 
                    : 'Error creating class'
            }));
        }
    }
};

  const handleClassNameChange = (e) => {
    const value = e.target.value;
    setClassNameInput(value);


    if (!value.trim()) {
      setRecommendedClasses([]);
    }

    if (errors.className) setErrors({ ...errors, className: "" });
  };

  const handleSelectClass = (classItem) => {
    setClassNameInput(classItem);
    setSearchClassInput("");
    setRecommendedClasses([]);
  };

  const handleSearchStudentChange = async (e) => {
    const value = e.target.value.trim();
    setSearchStudentInput(value);

    if (!value) {
        setRecommendedStudents([]);
        return;
    }

    try {
        const response = await apiClient.get('/classes/students/search/', {
            params: {
                q: value
            }
        });
        
        const students = response.data.students || [];
        const filteredStudents = students.filter(student => 
            !studentsList.includes(student.username)
        );
        setRecommendedStudents(filteredStudents);
    } catch (error) {
        console.error('Search error:', error);
    }
};

  const handleSelectStudent = (student) => {
    if (studentsList.length < studentLimit) {
        setStudentsList([...studentsList, student.username]);
        setSearchStudentInput("");
        setRecommendedStudents([]);
        if (errors.students) setErrors({ ...errors, students: "" });
    }
  };

  const handleDeleteStudent = (index) => {
    setStudentsList(studentsList.filter((_, i) => i !== index));
  };

  const handleCancel = () => {
    navigate(-1);
  };


  return (
    <div className={styles["form-container"]}>
      {isLoading && (
        <FloatAnimation 
          onClose={() => {
            setIsLoading(false);
            navigate(-1);
          }}
        />
      )}
      <div className={styles["form-main"]}>
        <h1>Create Class</h1>
        <div className={styles["bottom-line"]}></div>
        <form onSubmit={handleSubmit}>
          <div className={styles.input1}>
            <label>Class Name</label>
            <input
              type="text"
              placeholder="Enter the subject or class name (e.g., English)"
              value={classNameInput}
              onChange={handleClassNameChange}
            />
            {recommendedClasses.length > 0 && (
              <div className={styles["recommendations-dropdown"]}>
                {recommendedClasses.map((classItem, index) => (
                  <div key={index} onClick={() => handleSelectClass(classItem)}>
                    {classItem}
                  </div>
                ))}
              </div>
            )}
            {errors.className && <p className={styles["error-message"]}>{errors.className}</p>}
          </div>

          <div className={styles.header}>
            <label className={styles["section-label"]}>Add Students</label>
          </div>

          <p className={styles.description}>
            Total Students: Between 7 and 50.<br />
            By Search (Recommended): Add valid students one by one to avoid duplicates.<br />
            By CSV (Bulk Upload): Upload a CSV file with student usernames.<br />
            Combine Both Methods: Mix search and CSV upload, but only the first 50 valid students will be added.<br />
            Validation: If total students are less than 7, the class won't be created.<br />
            
          </p>

          <div className={styles.input5}>
            <label>Search Student</label>
            <input
              type="text"
              placeholder="Search student by username"
              value={searchStudentInput}
              onChange={handleSearchStudentChange}
            />
            {recommendedStudents.length > 0 && (
              <div className={styles["recommendations-dropdown"]}>
                {recommendedStudents.map((student, index) => (
                  <div 
                  key={index} 
                  onClick={() => handleSelectStudent(student)}
                  className={styles["recommendation-item"]}
                  >
                      {student.name} ({student.username})
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className={styles["student-list-container"]}>
            <div className={styles["student-limit"]}>{studentsList.length}/{studentLimit}</div>
            <div className={styles["student-list"]}>
              {studentsList.map((student, index) => (
                <div key={index} className={styles["student-item"]}>
                  {student}
                  <button className={styles["delete-btn"]} type="button" onClick={() => handleDeleteStudent(index)}>Delete</button>
                </div>
              ))}
            </div>
            {errors.students && <p className={styles["error-message"]}>{errors.students}</p>}
          </div>

          <div className={styles.section}>
            <div className={styles.header}>
              <label className={styles["section-label"]}>Upload CSV File</label>
              <button
                type="button"
                onClick={downloadSample}
                className={styles["sample-button"]}
              >
                Sample File
              </button>
            </div>

            <p className={styles.description}>
              Upload a CSV file containing a column named 'username'.
              Use the sample file as a guide. If the total student count exceeds 50,
              only the first 50 students will be added. Duplicate or invalid usernames will be skipped.
            </p>

            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`${styles.dropzone} ${isDragging ? styles.dragging : ""
                } ${file ? styles["has-file"] : ""}`}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                accept=".csv"
                className={styles.hidden}
              />
              <p className={styles["dropzone-text"]}>
                {file ? file.name : "Click here to upload your file or drag and drop."}
              </p>
              <p className={styles["format-text"]}>
                Supported Format (Only CSV)
              </p>
            </div>
            {errors.csv && <p className={styles["error-message"]}>{errors.csv}</p>}
          </div>



          <div className={styles.input4}>
            <button type="button" className={styles["input-btn1"]} onClick={handleCancel}>Cancel</button>
            <button type="submit" className={styles["input-btn2"]}>Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateClass;