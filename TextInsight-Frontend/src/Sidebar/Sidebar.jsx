import React from "react";
import { NavLink, useNavigate } from "react-router-dom"; // Import NavLink for active styling
import styles from "./sidebar.module.css";
import apiClient from '../apiClient'; // Import the Axios instance

export default function Sidebar() {
  const navigate = useNavigate();

  const menuItems = [
    { name: "Dashboard", path: "/studentdashboard", api: "/essay/dashboard/" },
    { name: "Manage Essays", path: "/manageessays", api: "/essay/manage_essay/" },
    { name: "Submission History", path: "/submissionhistory", api: "/essay/submission_history/" },
    { name: "Feedback History", path: "/feedbackhistory", api: "/feedback/feedback_history/" },
    { name: "Progress Monitoring", path: "/progressmonitoring", api: "/feedback/progress_history/" },
  ];

  const handleNavigation = async (path, api) => {
    try {
        const response = await apiClient.get(api);
        const data = response.data.data;

        if (path === "/studentdashboard") {
            navigate(path, {
                state: {
                    username: data.name,
                    dashboard: data.dashboard,
                },
            });
        } else {
            navigate(path, { state: { data } });
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
  };


  return (
    <div className={styles["sidebar"]}>
      <h2 className={styles["logo"]}>textinsight</h2>
      <div className={styles["menu"]}>
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) => (isActive ? styles.active : "")}
            onClick={(e) => {
              e.preventDefault();
              handleNavigation(item.path, item.api);
            }}
          >
            {item.name}
          </NavLink>
        ))}
      </div>
    </div>
  );
}
