import { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import styles from "./EssaySubmission.module.css";
import apiClient from '../apiClient';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function EssaySubmission() {
    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const { id, name } = state || {};

    const WORD_LIMITS = {
        introduction: 300,
        body: 500,
        conclusion: 200
    };

    const [formData, setFormData] = useState({
        introduction: '',
        body: '',
        conclusion: ''
    });

    const [errors, setErrors] = useState({
        introduction: false,
        body: false,
        conclusion: false
    });

    const [wordCounts, setWordCounts] = useState({
        introduction: 0,
        body: 0,
        conclusion: 0
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        const wordCount = value.trim().split(/\s+/).filter(word => word !== '').length;

        if (wordCount <= WORD_LIMITS[name]) {
            setFormData(prev => ({
                ...prev,
                [name]: value
            }));
            setWordCounts(prev => ({
                ...prev,
                [name]: wordCount
            }));
        }

        if (value.trim() !== '') {
            setErrors(prev => ({
                ...prev,
                [name]: false
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const newErrors = {
            introduction: formData.introduction === '',
            body: formData.body === '',
            conclusion: formData.conclusion === ''
        };

        setErrors(newErrors);

        if (!Object.values(newErrors).includes(true)) {
            setLoading(true);
            try {
                const response = await apiClient.post('/essay/submit_essay/', {
                    assignment_id: id,
                    introduction: formData.introduction,
                    middle: formData.body,
                    conclusion: formData.conclusion
                });

                if (response.status === 200) {
                    const feedbackResponse = await apiClient.get('/feedback/feedback_history/');
                    if (feedbackResponse.status === 200) {
                        navigate('/feedbackhistory', { state: { data: feedbackResponse.data.data } });
                    }
                }
            } catch (error) {
                const errorMessage = error.response?.data?.message || 'An error occurred while submitting the essay. Please try again.';
                toast.error(errorMessage);
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div className={styles["essay-submission"]}>
            <div className={styles["page-title"]}>
                <button className={styles["back-button"]} onClick={() => navigate(-1)}>
                    Back
                </button>
                <h2>Essay Submission</h2>
            </div>

            <div className={styles["essay-title"]}>
                <h2>Essay Title : {name}</h2>
            </div>

            <div className={styles["essay-instructions"]}>
                <ul>
                    <h4>Instructions for Essay Submission</h4>
                    <li>Your essay should follow these word limits:</li>
                    <ul>
                        <li>Introduction: Maximum {WORD_LIMITS.introduction} words</li>
                        <li>Body: Maximum {WORD_LIMITS.body} words</li>
                        <li>Conclusion: Maximum {WORD_LIMITS.conclusion} words</li>
                    </ul>
                    <li>Make sure your essay addresses the assigned topic by incorporating the relevant keywords where appropriate.</li>
                    <li>Use clear, concise language. Avoid excessive jargon or overly technical terms.</li>
                    <li>Proofread your essay for spelling and grammar before submitting.</li>
                    <li>Double-check your work before submission, as changes may not be possible afterward.</li>
                </ul>
            </div>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="introduction">Introduction</label>
                    {errors.introduction &&
                        <span className={styles["error-message"]}>Please fill out the introduction section</span>
                    }
                    <div className={styles["textarea-container"]}>
                        <textarea
                            id="introduction"
                            name="introduction"
                            value={formData.introduction}
                            onChange={handleChange}
                            placeholder='Type the introduction of essay here...'
                            className={errors.introduction ? styles["error-textarea"] : ""}
                        />
                        <span className={styles["word-count"]}>{wordCounts.introduction}/{WORD_LIMITS.introduction} words</span>
                    </div>
                </div>

                <div>
                    <label htmlFor="body">Body</label>
                    {errors.body &&
                        <span className={styles["error-message"]}>Please fill out the body section</span>
                    }
                    <div className={styles["textarea-container"]}>
                        <textarea
                            id="body"
                            name="body"
                            value={formData.body}
                            onChange={handleChange}
                            placeholder="Type the body of essay here..."
                            className={errors.body ? styles["error-textarea"] : ""}
                        />
                        <span className={styles["word-count"]}>{wordCounts.body}/{WORD_LIMITS.body} words</span>
                    </div>
                </div>

                <div>
                    <label htmlFor="conclusion">Conclusion</label>
                    {errors.conclusion &&
                        <span className={styles["error-message"]}>Please fill out the conclusion section</span>
                    }
                    <div className={styles["textarea-container"]}>
                        <textarea
                            id="conclusion"
                            name="conclusion"
                            value={formData.conclusion}
                            onChange={handleChange}
                            placeholder="Type the conclusion of essay here..."
                            className={errors.conclusion ? styles["error-textarea"] : ""}
                        />
                        <span className={styles["word-count"]}>{wordCounts.conclusion}/{WORD_LIMITS.conclusion} words</span>
                    </div>
                </div>

                {/* Toast container added here */}
                <div className={styles["toast-container"]}>
                    <ToastContainer
                        position="top-center"
                        autoClose={5000}
                        hideProgressBar={false}
                        newestOnTop={false}
                        closeOnClick
                        rtl={false}
                        pauseOnFocusLoss
                        draggable
                        pauseOnHover
                        theme="light"
                    />
                </div>

                <button type="submit" className={styles["submit-button"]} disabled={loading}>
                    {loading ? 'Please wait while processing...' : 'Submit Essay'}
                </button>
            </form>
        </div>
    );
}
