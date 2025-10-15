import { useState } from "react";
import styles from "./ManageEssays.module.css";
import { useNavigate, useLocation } from "react-router-dom";
import Sidebar from "../Sidebar/Sidebar";
import Navbar from "../NavBar/Navbar";

const EssayDetails = ({ essay, onHide }) => {
    const navigate = useNavigate(); // Initialize useNavigate

    const handleSubmitClick = () => {
        // Navigate to /essaysubmission with assignment_id and assignment_name
        navigate("/essaysubmission", {
            state: { id: essay.assignment_id, name: essay.assignment_name },
        });
    };

    return (
        <div className={styles["details-container"]}>
            <div className={styles["details"]}>
                <h3>Details</h3>
                <div className={styles["detail-row"]}>
                    <span className={styles["detail-label"]}>Class Code : </span>
                    <span className={styles["detail-value"]}>{essay.class_code}</span>
                </div>
                <div className={styles["detail-row"]}>
                    <span className={styles["detail-label"]}>Class Teacher : </span>
                    <span className={styles["detail-value"]}>{essay.teacher_name}</span>
                </div>
                <div className={styles["detail-row"]}>
                    <span className={styles["detail-label"]}>Deadline : </span>
                    <span className={styles["detail-value"]}>{essay.due_date}</span>
                </div>
                <div className={styles["detail-row"]}>
                    <span className={styles["detail-label"]}>Last Submission : </span>
                    <span className={styles["detail-value"]}>{essay.last_submission || "N/A"}</span>
                </div>
                <div className={styles["detail-row"]}>
                    <span className={styles["detail-label"]}>No # of Submission Left : </span>
                    <span className={styles["detail-value"]}>{essay.submission_count}</span>
                </div>
                <button className={styles["submit-btn"]} onClick={handleSubmitClick}>Submit</button>
            </div>
        </div>
    );
};

export default function ManageEssays() {
    const [expandedEssays, setExpandedEssays] = useState(new Set());
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const toggleEssayDetails = (index) => {
        setExpandedEssays(prev => {
            const newSet = new Set(prev);
            if (newSet.has(index)) {
                newSet.delete(index);
            } else {
                newSet.add(index);
            }
            return newSet;
        });
    };

    return (
        <div className={styles["manage-essays"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <Sidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Manage Essays</h2>
                <p>View and manage your recent essays. Select an essay to edit, submit, or check the current status.</p>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>Essay Title</div>
                <div className={styles["column"]}>Class Code</div>
                <div className={styles["column"]}>Deadline</div>
                <div className={styles["column"]}>Details</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length === 0 ? (
                    <div className={styles["no-assignments"]}>
                        <p className={styles["msg"]}>You don’t have any pending assignments at the moment. Check back later for new essay topics!</p>
                    </div>
                ) : (
                    data.map((essay, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{essay.assignment_name}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{essay.class_code}</div>
                                <div className={`${styles["column"]} ${styles["date"]}`}>{essay.due_date}</div>
                                <div className={styles["column"]}>
                                    <button
                                        className={`${styles["view-btn"]} ${expandedEssays.has(index) ? styles["hide-btn"] : ''}`}
                                        onClick={() => toggleEssayDetails(index)}
                                    >
                                        {expandedEssays.has(index) ? 'Hide' : 'View'}
                                    </button>
                                </div>
                            </div>
                            {expandedEssays.has(index) && <EssayDetails essay={essay} onHide={() => toggleEssayDetails(index)} />}
                        </div>
                    ))
                )}
            </div>

            
        </div>
    );
}
