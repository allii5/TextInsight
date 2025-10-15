import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import styles from './TeacherSubmissionHistoryExpand.module.css';
import apiClient from '../apiClient'; // Import the Axios instance

function TeacherSubmissionHistoryExpand() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { title, data = [] } = state || {};

    const handleView = async (submissionId, studentId) => {
        try {
            const response = await apiClient.get('/essay/submissions/specific/', {
                params: {
                    submission_id: submissionId,
                    student_id: studentId
                }
            });
            const submissionData = response.data.submission;
            navigate('/teachersubmittedessaydetails', { state: { submissionData } });
        } catch (error) {
            console.error('Error fetching submission content:', error);
        }
    };

    return (
        <div className={styles["submission-history"]}>
            <div className={styles["page-title"]}>
                <button className={styles["back-button"]} onClick={() => navigate(-1)}>
                    Back
                </button>
                <h2>Submission History</h2>
                <h2>{title}</h2>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>SR.</div>
                <div className={styles["column"]}>Name</div>
                <div className={styles["column"]}>Submitted On</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{index + 1}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.name}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.submission_on}</div>
                                <div className={styles["column"]}>
                                    <button className={styles["view-btn"]} onClick={() => handleView(essay.submission_id, essay.id)}>View</button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No submissions available.</p>
                )}
            </div>
        </div>
    );
}

export default TeacherSubmissionHistoryExpand;
