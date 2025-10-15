import { React, useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import styles from "./TeacherDashboard.module.css";
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import Axios for API calls

export default function TeacherDashboard() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { username, dashboard } = state || {};
    const { manage_classes, manage_essays, submission_history, feedback_history, progress_monitoring } = dashboard || {};

    // New section: Quick Actions
    const [quickActions, setQuickActions] = useState({
        createAccount: false,
        addClass: false,
        addEssay: false
    });

    const fetchDataAndNavigate = async (apiEndpoint, navigatePath) => {
        try {
            const response = await apiClient.get(apiEndpoint);
            const data = response.data.data;
            navigate(navigatePath, { state: { data } });
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleViewSubmission = async (assignmentId, title) => {
        try {
            const response = await apiClient.get(`/essay/assignment-submission/${assignmentId}/`);
            const data = response.data.submissions;
            navigate('/teachersubmissionhistoryexpand', { state: { title, data } });
        } catch (error) {
            console.error('Error fetching submission data:', error);
        }
    };

    const handleViewFeedback = async (assignmentId, title) => {
        try {
            const response = await apiClient.get('/feedback/details/', {
                params: {
                    assignment_id: assignmentId
                }
            });
            const data = response.data.feedback_details;
            navigate('/teacherfeedbackhistoryexpand', { state: { title, data } });
        } catch (error) {
            console.error('Error fetching feedback data:', error);
        }
    };

    const handleViewProgress = async (assignmentId, title) => {
        try {
            const response = await apiClient.get('/feedback/progress/details/', {
                params: {
                    assignment_id: assignmentId
                }
            });
            const data = response.data.progress_details;
            navigate('/teacherprogresshistoryexpand', { state: { title, data } });
        } catch (error) {
            console.error('Error fetching progress data:', error);
        }
    };

    return (
        <div className={styles["dashboard"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <TeacherSidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Welcome {username}!</h2>
                <p>Track student progress, manage assignments, and gain insights into class performance. Empower your students with personalized feedback and analytics.</p>
            </div>

            {/* New section: Quick Actions */}
            <div className={styles["quick-actions"]}>
                <h2>Quick Actions</h2>
                <button
                    className={styles["quick-action-btn"]}
                    onClick={() => navigate('/accountcreation')}
                >
                    + Create Account
                </button>
                <button
                    className={styles["quick-action-btn"]}
                    onClick={() => navigate('/createclass')}
                >
                    + Add Class
                </button>
                <button
                    className={styles["quick-action-btn"]}
                    onClick={() => navigate('/createessay')}
                >
                    + Add Essay
                </button>
            </div>

            <div className={styles["cards-container"]}>
                {/* Manage Classes Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Manage Classes</h3>
                    <div className={styles["card-content"]}>
                        {manage_classes.length > 0 ? (
                            manage_classes.map((classItem, index) => (
                                <div key={`manage-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{classItem.class_code}</h4>
                                    <p className={styles["info"]}>Class Strength: {classItem.student_count}/{classItem.student_limit}</p>
                                    <p className={styles["info"]}>Created: {classItem.created}</p>
                                    <button 
                                        className={styles["submit-btn"]} 
                                        onClick={() => navigate("/updateclass", {
                                            state: { 
                                                classId: classItem.id,
                                                classCode: classItem.class_code
                                            }
                                        })}
                                    >
                                        {'Update Class'}
                                    </button>
                                </div>
                            ))
                        ) : (
                            <p className={styles["msg"]}>You haven't created any classes yet. Create your first class to start managing your students!</p>
                        )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => fetchDataAndNavigate("/classes/fetch-classes/", "/teachermanageclasses")}>view all</button>
                </div>

                {/* Manage Essays Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Manage Essays</h3>
                    <div className={styles["card-content"]}>
                        {manage_essays.length > 0 ? (
                            manage_essays.map((essay, index) => (
                                <div key={`manage-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Deadline: {essay.deadline}</p>
                                    <button 
                                        className={styles["submit-btn"]} 
                                        onClick={() => navigate("/updateessay", { 
                                            state: { 
                                            assignmentId: essay.id // Pass assignment ID
                                            }
                                        })}
                                    >
                                        {'Update Submission'}
                                    </button>
                                </div>
                            )) ) : (
                                <p className={styles["msg"]}>No essays have been created yet. Create your first essay assignment to begin!</p>
                            )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => fetchDataAndNavigate("/essay/teacher-assignment/", "/teachermanageessays")}>view all</button>
                </div>

                {/* Submission History Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Submission History</h3>
                    <div className={styles["card-content"]}>
                        {submission_history.length > 0 ? (
                            submission_history.map((essay, index) => (
                                <div key={`submission-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Deadline: {essay.deadline}</p>
                                    <button className={styles["submit-btn"]} onClick={() => handleViewSubmission(essay.id, essay.title)}>View Submission</button>
                                </div>
                            ))) : (
                                <p className={styles["msg"]}>No essay submissions yet. Submissions will appear here once students start submitting their essays.</p>
                            )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => fetchDataAndNavigate("/essay/teacher-assignment/", "/teachersubmissionhistory")}>view all</button>
                </div>

                {/* Feedback History Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Feedback History</h3>
                    <div className={styles["card-content"]}>
                        {feedback_history.length > 0 ? (
                            feedback_history.map((essay, index) => (
                                <div key={`feedback-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Deadline: {essay.deadline}</p>
                                    <button className={styles["feedback-btn"]} onClick={() => handleViewFeedback(essay.id, essay.title)}>View Feedback</button>
                                </div>
                            ))) : (
                                <p className={styles["msg"]}>No feedback history available yet. Once you provide feedback on submissions, it will be displayed here.</p>
                            )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => fetchDataAndNavigate("/essay/teacher-assignment/", "/teacherfeedbackhistory")}>view all</button>
                </div>

                {/* Progress Monitoring Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Progress Monitoring</h3>
                    <div className={styles["card-content"]}>
                        {progress_monitoring.length > 0 ? (
                            progress_monitoring.map((essay, index) => (
                                <div key={`progress-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Deadline: {essay.deadline}</p>
                                    <button className={styles["feedback-btn"]} onClick={() => handleViewProgress(essay.id, essay.title)}>View Progress</button>
                                </div>
                            ))) : (
                                <p className={styles["msg"]}>No progress data available yet. Student progress will be displayed here once they start working on essays.</p>
                            )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => fetchDataAndNavigate("/essay/teacher-assignment/", "/teacherprogressmonitoring")}>view all</button>
                </div>
            </div>
        </div>
    );
}
