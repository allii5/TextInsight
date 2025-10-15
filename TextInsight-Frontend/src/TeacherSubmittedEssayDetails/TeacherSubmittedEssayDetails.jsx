import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./TeacherSubmittedEssayDetails.module.css";

export default function TeacherSubmittedEssay() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { submissionData } = state || {};

    return (
        <div className={styles["submitted-essay-details"]}>
            <div className={styles["page-title"]}>
                <button className={styles["back-button"]} onClick={() => navigate(-1)}>
                    Back
                </button>
                <h2>Submitted Essay Details</h2>
            </div>

            <div className={styles["essay-title"]}>
                <h2>Essay Title: {submissionData.title}</h2>
            </div>

            <div className={styles["instruction"]}>
                <h4>Review student submissions in detail. Access submitted essays for evaluation and provide personalized feedback.</h4>
            </div>

            <div>
                <div className={styles["label-group"]}>
                    <label htmlFor="your-essay">Student's Essay</label>
                </div>
                <textarea
                    id="your-essay"
                    name="your-essay"
                    value={submissionData.content}
                    readOnly
                />
            </div>
        </div>
    );
}
