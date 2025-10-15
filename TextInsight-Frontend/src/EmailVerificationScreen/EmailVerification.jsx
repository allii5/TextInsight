import { useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import apiClient from '../apiClient';
import styles from "./EmailVerification.module.css";

export default function EmailVerification() {
    const navigate = useNavigate();
    const location = useLocation();
    const [message, setMessage] = useState('');
    
    // Get username and action from router state
    const { username, action } = location.state || {};


    const handleResendEmail = async (e) => {
    e.preventDefault();
    setMessage(null);
    
    try {
        const response = await apiClient.post('/auth/resend-verification-email/', {
                username,
                action
            });
        setMessage({
            type: 'success',
            text: 'Verification email has been resent successfully.'
        });
    } catch (error) {
        setMessage({
            type: 'error',
            text: error.response?.data?.message || 'Failed to resend verification email.'
        });
    }
    };


    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const uid = queryParams.get('uid');
        const token = queryParams.get('token');
        const action = queryParams.get('action');

        if (uid && token && action) {
            apiClient.get(`/auth/api/verify-email/`, {
                params: { uid, token, action }
            })
            .then(response => {
                if (response.status === 200) {
                    setMessage(response.data.message);
                    if (action === 'create_account') {
                        navigate('/');
                    } else if (action === 'reset_password') {
                        navigate('/updatepassword', { state: { uid, token } });
                    }
                }
            })
            .catch(error => {
                setMessage('Verification failed. Please try again.');
            });
        } else {
            setMessage('Missing required parameters.');
        }
    }, [location, navigate]);

return (
   <div className={styles['emailVerification-container']}>
       <div className={styles['title']}>
           <h2>textinsight</h2>
       </div>
       <div className={styles['emailVerification-form']}>
           <h2 className={styles['form-title']}>Email Verification</h2>
           <p className={styles['text']}>
               A verification email has been sent to your registered email address. Please check your email and follow the instructions to complete the verification process.             
           </p>
           {message && (
               <div className={`${styles.message} ${styles[message.type]}`}>
                   {message.text}
               </div>
           )}
           <form className={styles['email-section']} onSubmit={handleResendEmail}>
               <button type="submit" className={styles['submit-button']}>
                   Resend Email
               </button>
           </form>
       </div>
   </div>
);
}
