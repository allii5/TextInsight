import { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import styles from './TeacherProgressMonitoringExpand.module.css';
import apiClient from '../apiClient'; // Import the Axios instance

function TeacherProgressHistoryExpand() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { title, data = [] } = state || {};

    const handleView = async (progressId, studentId) => {
        try {
            const response = await apiClient.get('/feedback/specific/progress/details/', {
                params: {
                    progress_id: progressId,
                    student_id: studentId
                }
            });
            const progressData = response.data.progress_details;
            navigate('/teacheressayevolution', { state: { title, progressData } });
        } catch (error) {
            console.error('Error fetching progress data:', error);
        }
    };

    return (
        <div className={styles["submission-history"]}>
            <div className={styles["page-title"]}>
                <button className={styles["back-button"]} onClick={() => navigate(-1)}>
                    Back
                </button>
                <h2>Progress History</h2>
                <h2>{title}</h2>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>SR.</div>
                <div className={styles["column"]}>Name</div>
                <div className={styles["column"]}>Progress On</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{index + 1}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.name}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.progress_on}</div>
                                <div className={styles["column"]}>
                                    <button
                                        className={styles["view-btn"]}
                                        onClick={() => handleView(essay.progress_id, essay.id)} // Navigate to TeacherEssayEvolution page
                                    >
                                        View
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No progress available.</p>
                )}
            </div>
        </div>
    );
}

export default TeacherProgressHistoryExpand;
