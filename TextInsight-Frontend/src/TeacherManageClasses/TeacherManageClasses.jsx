import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./TeacherManageClasses.module.css";
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";
import Navbar from "../NavBar/Navbar";

export default function TeacherManageClasses() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleAddClass = () => {
        navigate("/createclass"); // Navigates to the create class page
    };

    const handleViewClass = (classId, class_code) => {
        navigate("/updateclass", {
            state: { 
                classId: classId,  // Assuming each classItem has an id
                classCode: class_code // Optionally pass other data
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
                <h2>Manage Classes</h2>
                <p>Efficiently create, update, and organize classes to streamline student management and assignment distribution.</p>
            </div>

            <div className={styles["essay-title"]}>
                <div className={styles["column"]}>Class Name</div>
                <div className={styles["column"]}>Class Code</div>
                <div className={styles["column"]}>Strength</div>
                <div className={styles["column"]}>Action</div>
            </div>

            <div className={styles["essays-container"]}>
                {data.length > 0 ? (
                    data.map((cls, index) => (
                        <div key={index} className={styles["essay-wrapper"]}>
                            <div className={styles["essay-details"]}>
                                <div className={styles["column"]}>{cls.class_name}</div>
                                <div className={`${styles["column"]} ${styles["class-code"]}`}>{cls.class_code}</div>
                                <div className={`${styles["column"]} ${styles["strength"]}`}>
                                    {cls.student_count} / {cls.student_limit}
                                </div>
                                <div className={styles["column"]}>
                                    <button
                                        className={styles["view-btn"]}
                                        onClick={() => handleViewClass(cls.id, cls.class_code)} // Navigates to the class details page
                                    >
                                        Update
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>No classes available.</p>
                )}
            </div>

            <button
                className={styles["add-essay-button"]}
                onClick={handleAddClass} // Calls function that uses navigate
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
                <span>Add Class</span>
            </button>
        </div>
    );
}
