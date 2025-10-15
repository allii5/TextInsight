import { useNavigate, useLocation } from "react-router-dom"; // Import useNavigate
import styles from "./TeacherProgressMonitoring.module.css";
import TeacherSidebar from "../TeacherSidebar/TeacherSidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance

export default function TeacherProgressMonitoring() {
    const navigate = useNavigate(); // Initialize useNavigate
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (title, assignment_id) => {
        try {
            const response = await apiClient.get(`/feedback/progress/details/`, {
                params: {
                    assignment_id
                }
            });
            const data = response.data.progress_details;
            navigate('/teacherprogresshistoryexpand', { state: {title, data } });
        } catch (error) {
            console.error('Error fetching progress data:', error);
        }
    };

    return (
        <div className={styles["progress-history"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <TeacherSidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Progress Monitoring</h2>
                <p>Track student progress over time. Analyze improvements across submissions with detailed visualizations and feedback insights.</p>
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
                                        onClick={() => handleView(essay.title,essay.id)}
                                    >
                                        View
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className={styles["msg"]}>You need at least two submissions for any essay to monitor progress. Submit another draft to start tracking your improvements.</p>
                )}
            </div>
        </div>
    );
}
