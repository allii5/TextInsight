import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import apiClient from '../apiClient';
import styles from './UpdatePassword.module.css';
import showIcon from '../assets/show.png';
import hideIcon from '../assets/hide.png';

export default function UpdatePassword() {
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [passwordMatch, setPasswordMatch] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const navigate = useNavigate();
    const location = useLocation();
    
    // Get uid and token from navigation state
    const { uid, token } = location.state || {};

    useEffect(() => {
        // Redirect if uid or token is missing
        if (!uid || !token) {
            navigate('/');
        }
    }, [uid, token, navigate]);

    const togglePasswordVisibility = () => setShowPassword((prev) => !prev);
    const toggleConfirmPasswordVisibility = () => setShowConfirmPassword((prev) => !prev);

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        setPasswordMatch(e.target.value === confirmPassword);
    };

    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
        setPasswordMatch(e.target.value === password);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!passwordMatch || !password || !confirmPassword) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response = await apiClient.post('/auth/api/reset-password/', {
                uid,
                token,
                new_password: password,
                confirm_password: confirmPassword
            });

            if (response.data) {
                navigate('/', {
                    state: { message: 'Password updated successfully. Please login with your new password.' }
                });
            }
        } catch (error) {
            setError(error.response?.data?.error || "Failed to update password. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles['updatePassword-container']}>
            <div className={styles['title']}>
                <h2>textinsight</h2>
            </div>

            <div className={styles['updatePassword-form']}>
                <h2 className={styles['form-title']}>Update Password</h2>

                {error && <p className={styles['error-message']}>{error}</p>}

                <form className={styles['updatePassword-section']} onSubmit={handleSubmit}>
                    <div className={styles['password-container']}>
                        <input
                            type={showPassword ? 'text' : 'password'}
                            placeholder="Password"
                            className={styles['input-field']}
                            value={password}
                            onChange={handlePasswordChange}
                            required
                        />
                        <img
                            onClick={togglePasswordVisibility}
                            src={showPassword ? hideIcon : showIcon}
                            alt={showPassword ? 'Hide password' : 'Show password'}
                            className={styles['icon-image1']}
                        />
                    </div>

                    <div className={styles['password-container']}>
                        <input
                            type={showConfirmPassword ? 'text' : 'password'}
                            placeholder="Confirm Password"
                            className={styles['input-field']}
                            value={confirmPassword}
                            onChange={handleConfirmPasswordChange}
                            required
                        />
                        <img
                            onClick={toggleConfirmPasswordVisibility}
                            src={showConfirmPassword ? hideIcon : showIcon}
                            alt={showConfirmPassword ? 'Hide password' : 'Show password'}
                            className={styles['icon-image2']}
                        />
                    </div>

                    {!passwordMatch && <p className={styles['password-error']}>Passwords do not match!</p>}

                    <button 
                        type="submit" 
                        className={styles['submit-button']} 
                        disabled={!passwordMatch || loading}
                    >
                        {loading ? "Updating..." : "Update Password"}
                    </button>
                </form>
            </div>
        </div>
    );
}