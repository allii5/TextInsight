import React from "react";
import { NavLink, useNavigate } from "react-router-dom"; // Import NavLink for active styling
import styles from "./TeacherSidebar.module.css";
import apiClient from '../apiClient'; // Import the Axios instance

export default function TeacherSidebar() {
  const navigate = useNavigate();

  const menuItems = [
    { name: "Dashboard", path: "/teacherdashboard", api: "/essay/teacher-dashboard/" },
    { name: "Manage Classes", path: "/teachermanageclasses", api: "/classes/fetch-classes/" },
    { name: "Manage Essays", path: "/teachermanageessays", api: "/essay/teacher-assignment/" },
    { name: "Submission History", path: "/teachersubmissionhistory", api: "/essay/teacher-assignment/" },
    { name: "Feedback History", path: "/teacherfeedbackhistory", api: "/essay/teacher-assignment/" },
    { name: "Progress Monitoring", path: "/teacherprogressmonitoring", api: "/essay/teacher-assignment/" },
  ];

  const handleNavigation = async (path, api) => {
    try {
        const response = await apiClient.get(api);
        const data = response.data.data;

        if (path === "/teacherdashboard") {
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
