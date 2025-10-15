import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateEssay.module.css";
import apiClient from "../apiClient";

function CreateEssay({
  initialData = {},
  onSubmit,
  // classes = [
  //   { id: "1", name: "English Literature" },
  //   { id: "2", name: "Environmental Science" },
  //   { id: "3", name: "Economics" },
  //   { id: "4", name: "History" },
  //   { id: "5", name: "Mathematics" },
  //   { id: "6", name: "Physics" },
  //   { id: "7", name: "Geography" },
  //   { id: "8", name: "Biology" },
   

  // ],
  maxKeywords = 30,
  minKeywords = 25,
  maxDays = 30
}) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    essayName: "",
    essayDescription: "",
    selectedClass: "",
    deadline: "",
    keywords: "",
    ...initialData
  });

  const [errors, setErrors] = useState({});
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [selectedMonth, setSelectedMonth] = useState(new Date());
  const datePickerRef = useRef(null);
  const formRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (datePickerRef.current && !datePickerRef.current.contains(event.target)) {
        setShowDatePicker(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const [classes, setClasses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchClasses = async () => {
        try {
            const response = await apiClient.get('/classes/fetch-classes/');
            setClasses(response.data.data || []);
        } catch (error) {
            console.error("Error fetching classes:", error);
            setErrors(prev => ({
                ...prev,
                submit: "Failed to load classes"
            }));
            setClasses([]);
        } finally {
            setIsLoading(false);
        }
    };

    fetchClasses();
  }, []);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.essayName.trim()) {
        newErrors.essayName = "Essay name is required";
    } else if (formData.essayName.length > 255) {
        newErrors.essayName = "Essay name must be less than 255 characters";
    }
    
    if (!formData.selectedClass) {
        newErrors.selectedClass = "Class selection is required";
    }
    
    if (!formData.deadline) {
        newErrors.deadline = "Deadline is required";
    } else {
        // Check if date is in the future
        const selectedDate = new Date(formData.deadline);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (selectedDate <= today) {
            newErrors.deadline = "Deadline must be in the future";
        }
    }
    
    if (!formData.essayDescription.trim()) {
        newErrors.essayDescription = "Description is required";
    }
    
    const keywords = formData.keywords
        .split(',')
        .map(k => k.trim())
        .filter(k => k.length > 0);

    if (keywords.length < minKeywords || keywords.length > maxKeywords) {
        newErrors.keywords = `Please enter between ${minKeywords} and ${maxKeywords} keywords`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const days = [];
    
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i));
    }
    
    return days;
  };

  const generateCalendarDays = () => {
    const days = getDaysInMonth(selectedMonth);
    const firstDay = new Date(selectedMonth.getFullYear(), selectedMonth.getMonth(), 1);
    const prefixDays = Array(firstDay.getDay()).fill(null);
    
    return [...prefixDays, ...days];
  };

  const handlePrevMonth = () => {
    setSelectedMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1));
  };

  const handleNextMonth = () => {
    setSelectedMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1));
  };

  const handleDateSelect = (date) => {
    if (date) {
      setFormData(prev => ({ 
        ...prev, 
        deadline: date.toISOString().split('T')[0]
      }));
      setShowDatePicker(false);
      setErrors(prev => ({ ...prev, deadline: undefined }));
    }
  };

  const handleClassChange = (e) => {
    const selectedClass = e.target.value;
    setFormData(prev => ({ ...prev, selectedClass }));
    setErrors(prev => ({ ...prev, selectedClass: undefined }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: undefined }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
        try {
            // Format the data according to serializer requirements
            const assignmentData = {
                title: formData.essayName,
                description: formData.essayDescription,
                class_id: parseInt(formData.selectedClass), // Ensure it's an integer
                due_date: formData.deadline,
                expected_keywords: formData.keywords
                    .split(',')
                    .map(keyword => keyword.trim())
                    .filter(keyword => keyword.length > 0) // Remove empty strings
            };


            const response = await apiClient.post('/essay/create_assignment/', assignmentData);

            if (response.status === 201) {
                navigate(-1);
            }
        } catch (error) {
            console.error("Submission error:", error);
            // Handle validation errors from the backend
            if (error.response?.data?.errors) {
                const backendErrors = error.response.data.errors;
                setErrors(prev => ({
                    ...prev,
                    // Map backend error fields to your form fields
                    essayName: backendErrors.title,
                    essayDescription: backendErrors.description,
                    selectedClass: backendErrors.class_id,
                    deadline: backendErrors.due_date,
                    keywords: backendErrors.expected_keywords,
                    // If there's a general error
                    submit: Array.isArray(backendErrors) 
                        ? backendErrors.join(', ')
                        : typeof backendErrors === 'object'
                        ? Object.values(backendErrors).flat().join(', ')
                        : 'Failed to create essay'
                }));
            } else {
                setErrors(prev => ({
                    ...prev,
                    submit: "Failed to create essay"
                }));
            }
        }
    }
  };

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  
  const weekDays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

  return (
    <div className={styles.formContainer}>
      <div className={styles.formMain} ref={formRef}>
        <h1>Create Essay</h1>
        <div className={styles.bottomLine}></div>
        
        <form onSubmit={handleSubmit} className={styles.responsiveForm}>
          <div className={styles.formGrid}>
            <div className={`${styles.formGroup} ${errors.essayName ? styles.error : ''}`}>
              <label htmlFor="essayName">Essay Name</label>
              <input
                id="essayName"
                name="essayName"
                type="text"
                placeholder="Enter essay name"
                value={formData.essayName}
                onChange={handleChange}
                className={styles.formInput}
              />
              {errors.essayName && <span className={styles.errorMessage}>{errors.essayName}</span>}
              <p className={styles.formHelper}>Provide a clear and descriptive name for the essay.
              Keep it concise but meaningful for easy identification.</p>
            </div>

            <div className={`${styles.formGroup} ${errors.selectedClass ? styles.error : ''}`}>
              <label htmlFor="selectedClass">Assign to Class</label>
              <select
                id="selectedClass"
                name="selectedClass"
                value={formData.selectedClass}
                onChange={handleClassChange}
                className={styles.formSelect}
                disabled={isLoading}
              >
                <option value="">Select a class</option>
                {Array.isArray(classes) && classes.map(cls => (
                  <option key={cls.id} value={cls.id}>
                    {cls.class_name} ({cls.class_code})
                  </option>
                ))}
              </select>
              {errors.selectedClass && <span className={styles.errorMessage}>{errors.selectedClass}</span>}
              <p className={styles.formHelper}>Ensure the selected class is active and has enrolled students.</p>
            </div>

            <div className={`${styles.formGroup} ${errors.deadline ? styles.error : ''}`}>
              <label>Deadline for Submission</label>
              <div className={styles.datePickerContainer} ref={datePickerRef}>
                <input
                  type="text"
                  className={styles.formInput}
                  placeholder="Select date"
                  value={formData.deadline ? new Date(formData.deadline).toLocaleDateString() : ''}
                  onClick={() => setShowDatePicker(!showDatePicker)}
                  readOnly
                />
                {showDatePicker && (
                  <div className={styles.datePickerDropdown}>
                    <div className={styles.datePickerHeader}>
                      <button type="button" onClick={handlePrevMonth}>&lt;</button>
                      <span>{monthNames[selectedMonth.getMonth()]} {selectedMonth.getFullYear()}</span>
                      <button type="button" onClick={handleNextMonth}>&gt;</button>
                    </div>
                    <div className={styles.weekDays}>
                      {weekDays.map(day => (
                        <div key={day} className={styles.weekDay}>{day}</div>
                      ))}
                    </div>
                    <div className={styles.calendarDays}>
                      {generateCalendarDays().map((date, index) => (
                        <div
                          key={index}
                          className={`${styles.calendarDay} ${
                            date ? styles.active : ''
                          } ${
                            formData.deadline === date?.toISOString().split('T')[0] 
                              ? styles.selected 
                              : ''
                          }`}
                          onClick={() => date && handleDateSelect(date)}
                        >
                          {date ? date.getDate() : ''}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              {errors.deadline && <span className={styles.errorMessage}>{errors.deadline}</span>}
              <p className={styles.formHelper}>Choose a realistic deadline for students to submit their essays.
                Make sure the date is in the future to allow sufficient preparation time.</p>
            </div>
          </div>

          {/* Rest of the form remains unchanged */}
          <div className={`${styles.formGroup} ${errors.essayDescription ? styles.error : ''}`}>
            <label htmlFor="essayDescription">Essay Description</label>
            <textarea
              id="essayDescription"
              name="essayDescription"
              placeholder="Write a short overview of the essay's purpose"
              value={formData.essayDescription}
              onChange={handleChange}
              className={styles.formTextarea}
            />
            {errors.essayDescription && <span className={styles.errorMessage}>{errors.essayDescription}</span>}
            <p className={styles.formHelper}>(Keep it brief and informative (2-3 sentences recommended))</p>
          </div>

          <div className={`${styles.formGroup} ${errors.keywords ? styles.error : ''}`}>
            <label htmlFor="keywords">Expected Keywords</label>
            <textarea
              id="keywords"
              name="keywords"
              placeholder="Enter keywords separated by commas"
              value={formData.keywords}
              onChange={handleChange}
              className={`${styles.formTextarea} ${styles.keywordsTextarea}`}
            />
            {errors.keywords && <span className={styles.errorMessage}>{errors.keywords}</span>}
            <p className={styles.formHelper}>(Enter 25 to 30 keywords that you expect students to include in their essays.
              Use a comma-separated format (e.g., keyword1, keyword2, keyword3).)</p>
          </div>

          <div className={styles.formActions}>
            <button type="button" className={styles.btnCancel} onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button type="submit" className={styles.btnSubmit}>
              Submit
            </button>
          </div>

          {errors.submit && (
            <div className={styles.submitError}>
              {errors.submit}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default CreateEssay;