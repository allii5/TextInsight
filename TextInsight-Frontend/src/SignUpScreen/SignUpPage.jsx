import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../apiClient'; // Import Axios for API calls
import styles from './SignUpPage.module.css';
import showIcon from '../assets/show.png';
import hideIcon from '../assets/hide.png';
import arrowIcon from '../assets/down-arrow.png';

export default function SignUp() {
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [passwordMatch, setPasswordMatch] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const togglePasswordVisibility = () => setShowPassword((prev) => !prev);
    const toggleConfirmPasswordVisibility = () => setShowConfirmPassword((prev) => !prev);

    const handlePasswordChange = (e) => setPassword(e.target.value);
    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
        setPasswordMatch(e.target.value === password);
    };

    const handleSignUp = async (e) => {
        e.preventDefault();
        setErrorMessage(''); // Clear previous error messages

        if (!passwordMatch) {
            setErrorMessage('Passwords do not match!');
            return;
        }

        try {
            const response = await apiClient.post('/auth/api/signup-teacher/', {
                name,
                email,
                username,
                password,
                education_level: educationLevel,
            });

            if (response.status === 201) {
                // Redirect to login page on successful signup
                navigate('/');
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data.message) {
                setErrorMessage(error.response.data.message); // Show server error message
            } else {
                setErrorMessage('Something went wrong. Please try again.');
            }
        }
    };

    return (
        <div className={styles['signUp-container']}>
            <div className={styles['title']}>
                <h2>textinsight</h2>
            </div>

            <div className={styles['signUp-form']}>
                <h2 className={styles['form-title']}>Create Account</h2>

                <form className={styles['signUp-section']} onSubmit={handleSignUp}>
                    <input
                        type="text"
                        placeholder="Full Name"
                        className={styles['input-field']}
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />

                    <input
                        type="text"
                        placeholder="Email Address"
                        className={styles['input-field']}
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
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
                            className={styles['icon-image1']}
                        />
                    </div>

                    <div className={styles['dropdown-container']}>
                        <select
                            value={educationLevel}
                            onChange={(e) => setEducationLevel(e.target.value)}
                            className={styles.dropdown}
                            required
                        >
                            <option value="" disabled>
                                Education Level
                            </option>
                            <option value="Intermediate">Intermediate</option>
                            <option value="O/A Levels">O/A Levels</option>
                            <option value="Bachelors">Bachelors</option>
                            <option value="Masters">Masters</option>
                            <option value="PhD">PhD</option>
                        </select>
                        <img src={arrowIcon} alt="arrow down" className={styles['dropdown-icon']} />
                    </div>

                    {!passwordMatch && <p className={styles['password-error']}>Passwords do not match!</p>}
                    {errorMessage && <p className={styles['error-message']}>{errorMessage}</p>}

                    <button type="submit" className={styles['submit-button']} disabled={!passwordMatch}>
                        Sign Up
                    </button>
                </form>

                <div>
                    <p>
                        Already have an account?{' '}
                        <a
                            onClick={() => navigate('/')} // Navigate back to login page
                            className={styles['login-link']}
                        >
                            Login
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
}
