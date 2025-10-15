import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./TeacherManageEssays.module.css";
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";
import Navbar from "../NavBar/Navbar";

export default function TeacherManageEssays() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleAddEssay = () => {
        navigate('/createessay'); // Navigates to the create essay page
    };

    const handleViewEssay = (essayId) => {
        navigate("/updateessay", { 
            state: { 
            assignmentId: essayId // Pass assignment ID
            }
        })
    };

    return (
        <div className={styles["manage-essays"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <TeacherSidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Manage Essays</h2>
                <p>Easily create, view, and update assignments, ensuring students are aligned with clear objectives and deadlines.</p>
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
                                        onClick={() => handleViewEssay(essay.id)} // Navigates to the essay details page
                                    >
                                        Update
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No essays available.</p>
                )}
            </div>

            <button
                className={styles["add-essay-button"]}
                onClick={handleAddEssay} // Calls function that uses navigate
            >
                <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        d="M12 4V20M4 12H20"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                </svg>
                <span>Add Essay</span>
            </button>
        </div>
    );
}
