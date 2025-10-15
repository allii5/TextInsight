import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./TeacherFeedbackHistoryScreen.module.css";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";

export default function TeacherFeedbackHistory() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (assignment_id, title) => {
        try {
            const response = await apiClient.get(`/feedback/details/`, {
                params: {
                    assignment_id
                }
            });
            const data = response.data.feedback_details;
            navigate('/teacherfeedbackhistoryexpand', { state: { title, data } });
        } catch (error) {
            console.error('Error fetching feedback data:', error);
        }
    };

    return (
        <div className={styles["feedback-history"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <TeacherSidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Feedback History</h2>
                <p>Explore all generated feedback. Review feedback for every essay submission and provide additional insights if needed.</p>
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
                                    <button
                                        className={styles["view-btn"]}
                                        onClick={() => handleView(essay.id, essay.title)} // Navigate to ExploreInsight page
                                    >
                                        View
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No Feedback Yet</p>
                )}
            </div>
        </div>
    );
}
