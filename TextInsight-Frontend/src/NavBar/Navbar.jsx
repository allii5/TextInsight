import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import styles from "./Navbar.module.css";
import bellIcon from "../assets/bell.png";
import profileIcon from "../assets/profile.png";
import apiClient from '../apiClient'; // Assuming you have an apiClient for making API calls

export default function Navbar() {
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const navigate = useNavigate();

    const handleProfileClick = () => {
        setShowProfileMenu(!showProfileMenu);
    };

    const handleOptionClick = (option) => {
        setShowProfileMenu(false);
        if (option === 'logout') {
            navigate('/'); // Redirect to login page
        } else if (option === 'updatePassword') {
            navigate('/updatepassword'); // Redirect to update password page
        }
    };

    const handleBellClick = async () => {
        try {
            const response = await apiClient.get('/essay/notification_history/');
            if (response.status === 200) {
                navigate('/notifications', { state: { data: response.data.data } });
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
            // Handle error (e.g., show a toast notification)
        }
    };

    return (
        <div className={styles["navbar"]}>
            <div className={styles["navbar-header"]}>
                <div className={styles["icons-container"]}>
                    <div className={styles["bell-icon-wrapper"]} onClick={handleBellClick}>
                        <div className={styles["tooltip-container"]}>
                            <img src={bellIcon} alt="Notification Bell" className={styles["bell-icon"]} />
                            <span className={styles["tooltip"]} >Notifications</span>
                        </div>
                    </div>

                    <div className={styles["profile-container"]}>
                        <div className={styles["profile-icon-wrapper"]}>
                            <div
                                className={`${styles["tooltip-container"]} ${showProfileMenu ? styles["hide-tooltip"] : ""}`}
                                onClick={handleProfileClick}
                            >
                                <img src={profileIcon} alt="Profile Icon" className={styles["profile-icon"]} />
                                <span className={styles["tooltip"]}>Profile</span>
                            </div>
                        </div>

                        {showProfileMenu && (
                            <div className={styles["profile-dropdown"]}>
                                <button
                                    className={styles["dropdown-option"]}
                                    onClick={() => handleOptionClick('updatePassword')}
                                >
                                    Update Password
                                </button>
                                <button
                                    className={styles["dropdown-option"]}
                                    onClick={() => handleOptionClick('logout')}
                                >
                                    Logout
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
