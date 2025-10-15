import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styles from "./UpdateClass.module.css";
import apiClient from '../apiClient';

function UpdateClass() {
  const navigate = useNavigate();
  const [classNameInput, setClassNameInput] = useState("");
  const [searchStudentInput, setSearchStudentInput] = useState("");
  const [studentsList, setStudentsList] = useState([]);
  const [recommendedStudents, setRecommendedStudents] = useState([]);
  const [studentLimit, setStudentLimit] = useState(50);
  const [errors, setErrors] = useState({});
  const [searchClassInput, setSearchClassInput] = useState("");
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [classDetails, setClassDetails] = useState(null);
  const location = useLocation();
  const { classId } = location.state || {};

  useEffect(() => {
        const fetchClassDetails = async () => {
            if (!classId) {
                navigate(-1);
                return;
            }

            try {
                const response = await apiClient.get(`/classes/${classId}/details/`);
                setClassDetails(response.data);
                setClassNameInput(response.data.class_name);
                setStudentsList(response.data.current_students);
            } catch (error) {
                console.error('Error fetching class details:', error);
                setErrors(prev => ({
                    ...prev,
                    submit: 'Failed to load class details'
                }));
            } finally {
                setIsLoading(false);
            }
        };

        fetchClassDetails();
  }, [classId, navigate]);

  const allStudents = [
    "Alice Johnson", "Amanda Rodriguez", "Andrew Smith", "Anna Davis", "Benjamin Lee",
    "Brandon White", "Brian Martinez", "Catherine Kim", "Charles Brown", "Christina Lopez"
  ];

  const allClasses = [
    "Mathematics", "English", "Science", "History", "Geography",
    "Physics", "Chemistry", "Biology", "Computer Science", "Economics"
  ];

  const validateForm = () => {
    let newErrors = {};
    if (!classNameInput.trim()) newErrors.className = "Class name is required.";
    if (studentsList.length === 0) newErrors.students = "At least one student must be added.";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
        try {
            const response = await apiClient.post('/classes/update-class/', {
                class_id: classId,
                class_name: classNameInput,
                added_usernames: studentsList // Send the updated student list
            });

            if (response.status === 200) {
                navigate(-1);
            }
        } catch (error) {
            console.error('Error updating class:', error);
            setErrors(prev => ({
                ...prev,
                submit: error.response?.data?.message || 'Failed to update class'
            }));
        }
    }
  };

  const handleClassNameChange = (e) => {
    const value = e.target.value;
    setClassNameInput(value);
    setSearchClassInput(value);

    if (!value.trim()) {
      setRecommendedClasses([]);
    } else {
      setRecommendedClasses(
        allClasses.filter(classItem => classItem.toLowerCase().startsWith(value.toLowerCase()))
      );
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
      <div className={styles["form-main"]}>
        <h1>Update Class</h1>
        <div className={styles["bottom-line"]}></div>
        <form onSubmit={handleSubmit}>
          <div className={styles["input1"]}>
            <label>Class Name</label>
            <input
              type="text"
              placeholder="Enter or select class name"
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

          <div className={styles["input5"]}>
            <label>Search Student</label>
            <input
              type="text"
              placeholder="Search student"
              value={searchStudentInput}
              onChange={handleSearchStudentChange}
            />
            {recommendedStudents.length > 0 && (
                <div className={styles["recommendations-dropdown"]}>
                    {recommendedStudents.map((student, index) => (
                        <div key={index} onClick={() => handleSelectStudent(student)}>
                            {student.name} ({student.username})  {/* Display name and username */}
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
                        {typeof student === 'string' ? student : student.username}  {/* Handle both string and object cases */}
                        <button 
                            className={styles["delete-btn"]} 
                            type="button" 
                            onClick={() => handleDeleteStudent(index)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
            {errors.students && <p className={styles["error-message"]}>{errors.students}</p>}
          </div>
          
          <div className={styles["input4"]}>
            <button type="button" className={styles["input-btn1"]} onClick={handleCancel}>Cancel</button>
            <button type="submit" className={styles["input-btn2"]}>Submit</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default UpdateClass;