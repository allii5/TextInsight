import { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from '../apiClient';
import styles from "./FirstLogin.module.css";

export default function FirstLogin() {
    const [email, setEmail] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleForgotPassword = async (e) => {
        e.preventDefault();
        setErrorMessage('');
        setSuccessMessage('');

        try {
            // Call the forgot password API
            const response = await apiClient.post('/auth/api/forgot-password/', {
                email,
            });

            // Show success message and navigate
            if (response.data.message === "Password reset email sent successfully") {
                setSuccessMessage("Email sent! Redirecting...");
                setTimeout(() => {
                    navigate('/emailverification');
                }, 2000); // Redirect after 2 seconds
            }
        } catch (error) {
            // Handle error and show error message
            if (error.response && error.response.data && error.response.data.message) {
                setErrorMessage(error.response.data.message);
            } else {
                setErrorMessage("Something went wrong. Please try again.");
            }
        }
    };

    return (
        <div className={styles['firstLogin-container']}>

            <div className={styles['title']}>
                <h2>textinsight</h2>
            </div>

            <div className={styles['firstLogin-form']}>
                <h2 className={styles['form-title']}>Forgot Password</h2>
                <p className={styles['text']}>
                    Please enter your email for verification. Check your email for the verification link to complete the process.
                </p>

                <form className={styles['email-section']} onSubmit={handleForgotPassword}>
                    <input
                        type="text"
                        className={styles['input-field']}
                        placeholder="Email Address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <button type="submit" className={styles['submit-button']}>Send Email</button>
                </form>

                {/* Show success or error message */}
                {successMessage && <p className={styles['success-message']}>{successMessage}</p>}
                {errorMessage && <p className={styles['error-message']}>{errorMessage}</p>}
            </div>
        </div>
    );
}
