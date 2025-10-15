import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./TeacherSubmissionHistory.module.css";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";

export default function TeacherSubmissionHistory() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (title, submissionId) => {
        try {
            const response = await apiClient.get(`/essay/assignment-submission/${submissionId}/`);
            const data = response.data.submissions;
            navigate('/teachersubmissionhistoryexpand', { state: {title, data } });
        } catch (error) {
            console.error('Error fetching submission content:', error);
        }
    };

    return (
        <div className={styles["submission-history"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <TeacherSidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Submission History</h2>
                <p>Track all essay submissions with ease. View, review, and manage submissions from every student and class in one place.</p>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>Essay Title</div>
                <div className={styles["column"]}>Class Code</div>
                <div className={styles["column"]}>Deadline</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{essay.title}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.class_code}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.deadline}</div>
                                <div className={styles["column"]}>
                                    <button className={styles["view-btn"]} onClick={() => handleView(essay.title, essay.id)}>View</button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>You haven't created any assignment so far!</p>
                )}
            </div>
        </div>
    );
}
