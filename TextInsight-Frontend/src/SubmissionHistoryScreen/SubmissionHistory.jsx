import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./SubmissionHistory.module.css";
import Sidebar from "../Sidebar/Sidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance

export default function SubmissionHistory() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (submissionId) => {
        try {
            const response = await apiClient.get(`/essay/submission_content/${submissionId}/`);
            const submissionData = response.data.data;
            navigate('/submittedessay', { state: { submissionData } });
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
                <Sidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Submission History</h2>
                <p>Keep track of all your past essay submissions. Review previous work and monitor your progress over time.</p>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>Essay Title</div>
                <div className={styles["column"]}>Class Code</div>
                <div className={styles["column"]}>Submitted On</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{essay.title}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.class_code}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.submitted}</div>
                                <div className={styles["column"]}>
                                    <button className={styles["view-btn"]} onClick={() => handleView(essay.id)}>View</button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>You haven't submitted any essays so far. Start writing and submit your first essay to begin tracking your progress!</p>
                )}
            </div>
        </div>
    );
}
