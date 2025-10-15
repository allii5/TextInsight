import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./FeedbackHistory.module.css";
import Sidebar from "../Sidebar/Sidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance

export default function FeedbackHistory() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (feedbackId, title) => {
        try {
            const response = await apiClient.get(`/feedback/feedback_data/${feedbackId}/`);
            const feedbackData = response.data.data;
            navigate('/exploreinsight', { state: { title, feedbackData } });
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
                <Sidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Feedback History</h2>
                <p>Access your feedback history to see detailed insights. Reflect on each review to improve with every submission.</p>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>Essay Title</div>
                <div className={styles["column"]}>Class Code</div>
                <div className={styles["column"]}>Feedback On</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{essay.title}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.class_code}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.feedback_on}</div>
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
                    <p className={styles["msg"]}>You haven’t received feedback yet. Submit an essay to get personalized insights and suggestions to improve your writing.</p>
                )}
            </div>
        </div>
    );
}
