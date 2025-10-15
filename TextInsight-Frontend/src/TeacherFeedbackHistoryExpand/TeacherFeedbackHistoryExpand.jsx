import { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import styles from './TeacherFeedbackHistoryExpand.module.css';
import apiClient from '../apiClient'; // Import the Axios instance

function TeacherFeedbackHistoryExpand() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { title, data = [] } = state || {};

    const handleView = async (feedbackId, studentId) => {
        try {
            const response = await apiClient.get('/feedback/specific/details/', {
                params: {
                    feedback_id: feedbackId,
                    student_id: studentId
                }
            });
            const feedbackData = response.data.feedback_details;
            navigate('/teacherexploreinsight', { state: { title, feedbackData } });
        } catch (error) {
            console.error('Error fetching feedback data:', error);
        }
    };

    return (
        <div className={styles["submission-history"]}>
            <div className={styles["page-title"]}>
                <button className={styles["back-button"]} onClick={() => navigate(-1)}>
                    Back
                </button>
                <h2>Feedback History</h2>
                <h2>{title}</h2>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>SR.</div>
                <div className={styles["column"]}>Name</div>
                <div className={styles["column"]}>Feedback On</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{index + 1}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.name}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.feedback_on}</div>
                                <div className={styles["column"]}>
                                    <button
                                        className={styles["view-btn"]}
                                        onClick={() => handleView(essay.feedback_id, essay.id)} // Navigate to TeacherEssayInsight page
                                    >
                                        View
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No feedback available.</p>
                )}
            </div>
        </div>
    );
}

export default TeacherFeedbackHistoryExpand;
