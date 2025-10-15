import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../apiClient'; // Import Axios for API calls
import styles from './LoginPage.module.css';
import showIcon from '../assets/show.png';
import hideIcon from '../assets/hide.png';

export default function LoginPage() {
    const [showPassword, setShowPassword] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const togglePasswordVisibility = () => {
        setShowPassword((prevState) => !prevState);
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setErrorMessage(''); // Clear previous errors

        try {
            // Step 1: Login API call
            const response = await apiClient.post('/auth/api/login/', {
                username,
                password,
            });

            const data = response.data;

            if (data.message === 'Login successful') {
                // Save tokens to local storage or cookie
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);

                if (data.role === 'teacher') {
                    const dashboardResponse = await apiClient.get('/essay/teacher-dashboard/');

                    const dashboardData = dashboardResponse.data;
                    console.log(dashboardData)

                    // Navigate to teacher dashboard
                    navigate('/teacherdashboard', {
                        state: { 
                            username: dashboardData.data.name,
                            dashboard: dashboardData.data.dashboard,
                        }   
                    });

                } else if (data.role === 'student') {
                    
                    // Step 2: Fetch student dashboard data
                    const dashboardResponse = await apiClient.get('/essay/dashboard/');

                    const dashboardData = dashboardResponse.data;

                    // Navigate to student dashboard with dashboard data
                    navigate('/studentdashboard', {
                        state: {
                            username: dashboardData.data.name,
                            dashboard: dashboardData.data.dashboard,
                        },
                    });
                }
            } else if (data.message === 'Verification email sent. Please verify your email to complete the login.') {
                navigate('/emailverification', {
                    state: {
                        username: username,
                        action: 'create_account' // or whatever action is appropriate
                    }
                });
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data.message) {
                setErrorMessage(error.response.data.message);
            } else {
                setErrorMessage('Something went wrong. Please try again.');
            }
        }
    };

    return (
        <div className={styles['login-container']}>
            <div className={styles['text-section']}>
                <h2 className={styles['title']}>textinsight</h2>
                <div className={styles['subtitle-container']}>
                    <div className={styles['subtitle-first-line']}>Unlock the power of words,</div>
                    <div className={styles['subtitle-second-line']}>together</div>
                </div>
            </div>

            <div className={styles['Login-form']}>
                <form className={styles['Login-section']} onSubmit={handleLogin}>
                    <input
                        type="text"
                        placeholder="Username"
                        className={styles['input-field']}
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <div className={styles['password-container']}>
                        <input
                            type={showPassword ? 'text' : 'password'}
                            placeholder="Password"
                            className={styles['input-field']}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <img
                            onClick={togglePasswordVisibility}
                            src={showPassword ? hideIcon : showIcon}
                            alt={showPassword ? 'Hide password' : 'Show password'}
                            className={styles['icon-image']}
                        />
                    </div>

                    {errorMessage && <p className={styles['error-message']}>{errorMessage}</p>}

                    <button type="submit" className={styles['submit-button']}>Login</button>
                </form>

                <a
                    className={styles['forgot-password']}
                    onClick={(e) => {
                        e.preventDefault();
                        navigate('/firstLogin');
                    }}
                >
                    Forgotten Password?
                </a>

                <div className={styles['signup-text']}>
                    <p>For Teachers: Don't have an account? <a onClick={() => navigate('/signup')}>Sign Up</a></p>
                    <p>For Students: Need an account? Contact your teacher</p>
                </div>
            </div>
        </div>
    );
}
