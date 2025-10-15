import React from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import styles from "./StudentDashboard.module.css";
import Sidebar from "../Sidebar/Sidebar";
import Navbar from "../NavBar/Navbar";
import apiClient from '../apiClient'; // Import the Axios instance

export default function StudentDashboard() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { username, dashboard } = state || {};

    const { pending_assignments = [], feedback_history = [], progress_history = [], submission_history = [] } = dashboard || {};

    const handleViewAll = async (apiEndpoint, navigatePath) => {
        try {
            const response = await apiClient.get(apiEndpoint);
            const data = response.data.data;
            navigate(navigatePath, { state: { data } });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleManageEssaySubmit = (id, assignment_name) => {
        navigate('/essaysubmission', { state: { id, name: assignment_name } });
    };

    const handleSubmissionHistorySubmit = async (submission_id) => {
        try {
            const response = await apiClient.get(`/essay/submission_content/${submission_id}/`);
            const submissionData = response.data.data;
            navigate('/submittedessay', { state: { submissionData } });
        } catch (error) {
            console.error('Error fetching submission data:', error);
        }
    };

    const handleFeedbackHistorySubmit = async (feedback_id, title) => {
        try {
            const response = await apiClient.get(`/feedback/feedback_data/${feedback_id}/`);
            const feedbackData = response.data.data;
            navigate('/exploreinsight', { state: { title, feedbackData } });
        } catch (error) {
            console.error('Error fetching feedback data:', error);
        }
    };

    const handleProgressMonitoringSubmit = async (progress_id, title) => {
        try {
            const response = await apiClient.get(`/feedback/progress_data/${progress_id}/`);
            const progressData = response.data.data;
            navigate('/essayevolution', { state: { title, progressData } });
        } catch (error) {
            console.error('Error fetching progress data:', error);
        }
    };

    return (
        <div className={styles["dashboard"]}>
            <div className={styles["navbar"]}>
                <Navbar />
            </div>

            <div className={styles["sidebar"]}>
                <Sidebar />
            </div>

            <div className={styles["page-title"]}>
                <h2>Welcome {username}!</h2>
                <p>Stay updated with your latest essay submissions and feedback. Here's what you've accomplished recently!</p>
            </div>

            <div className={styles["cards-container"]}>
                {/* Manage Essays Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Manage Essays</h3>
                    <div className={styles["card-content"]}>
                        {pending_assignments.length > 0 ? (
                            pending_assignments.map((essay, index) => (
                                <div key={`manage-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.assignment_name}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Class Teacher: {essay.teacher_name}</p>
                                    <p className={styles["info"]}>Deadline: {essay.due_date}</p>
                                    <button className={styles["submit-btn"]} onClick={() => handleManageEssaySubmit(essay.assignment_id, essay.assignment_name)}>
                                        {essay.submission_count > 0 ? 'Resubmit Essay' : 'Submit Essay'}
                                    </button>
                                </div>
                            ))
                        ) : (
                            <p className={styles["msg"]}>You don’t have any pending assignments at the moment. Check back later for new essay topics!</p>
                        )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => handleViewAll('/essay/manage_essay/', '/manageessays')}>view all</button>
                </div>

                {/* Submission History Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Submission History</h3>
                    <div className={styles["card-content"]}>
                        {submission_history.length > 0 ? (
                            submission_history.map((essay, index) => (
                                <div key={`submission-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Class Teacher: {essay.teacher_name}</p>
                                    <p className={styles["info"]}>Submitted: {essay.submitted}</p>
                                    <button className={styles["submit-btn"]} onClick={() => handleSubmissionHistorySubmit(essay.id)}>View Submission</button>
                                </div>
                            ))
                        ) : (
                            <p className={styles["msg"]}>You haven't submitted any essays so far. Start writing and submit your first essay to begin tracking your progress!</p>
                        )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => handleViewAll('/essay/submission_history/', '/submissionhistory')}>view all</button>
                </div>

                {/* Feedback History Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Feedback History</h3>
                    <div className={styles["card-content"]}>
                        {feedback_history.length > 0 ? (
                            feedback_history.map((essay, index) => (
                                <div key={`feedback-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Class Teacher: {essay.teacher_name}</p>
                                    <p className={styles["info"]}>Feedback On: {essay.feedback_on}</p>
                                    <button className={styles["feedback-btn"]} onClick={() => handleFeedbackHistorySubmit(essay.id, essay.title)}>View Feedback</button>
                                </div>
                            ))
                        ) : (
                            <p className={styles["msg"]}>You haven’t received feedback yet. Submit an essay to get personalized insights and suggestions to improve your writing.</p>
                        )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => handleViewAll('/feedback/feedback_history/', '/feedbackhistory')}>view all</button>
                </div>

                {/* Progress Monitoring Card */}
                <div className={styles["card"]}>
                    <h3 className={styles["card-title"]}>Progress Monitoring</h3>
                    <div className={styles["card-content"]}>
                        {progress_history.length > 0 ? (
                            progress_history.map((essay, index) => (
                                <div key={`progress-${index}`} className={styles["essay-item"]}>
                                    <h4 className={styles["subject"]}>{essay.title}</h4>
                                    <p className={styles["info"]}>Class Code: {essay.class_code}</p>
                                    <p className={styles["info"]}>Class Teacher: {essay.teacher_name}</p>
                                    <p className={styles["info"]}>Progress On: {essay.feedback_on}</p>
                                    <button className={styles["feedback-btn"]} onClick={() => handleProgressMonitoringSubmit(essay.id, essay.title)}>View Progress</button>
                                </div>
                            ))
                        ) : (
                            <p className={styles["msg"]}>You need at least two submissions for any essay to monitor progress. Submit another draft to start tracking your improvements.</p>
                        )}
                    </div>
                    <button className={styles["view-all"]} onClick={() => handleViewAll('/feedback/progress_history/', '/progressmonitoring')}>view all</button>
                </div>
            </div>
        </div>
    );
}
