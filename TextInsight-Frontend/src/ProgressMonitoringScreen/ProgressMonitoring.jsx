import { useNavigate, useLocation } from "react-router-dom"; // Import useNavigate
import styles from "./ProgressMonitoring.module.css";
import Sidebar from "../Sidebar/Sidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance

export default function ProgressMonitoring() {
    const navigate = useNavigate(); // Initialize useNavigate
    const location = useLocation();
    const { state } = location;
    const { data = [] } = state || {};

    const handleView = async (title, progressId) => {
        try {
            const response = await apiClient.get(`/feedback/progress_data/${progressId}/`);
            const progressData = response.data.data;
            navigate('/essayevolution', { state: {title, progressData } });
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
                <Sidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Progress Monitoring</h2>
                <p>See how far you've come! Monitor your improvements, compare submissions, and celebrate your growth over time.</p>
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
                                        onClick={() => handleView(essay.title,essay.id)} // Navigate to EssayEvolution page
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
