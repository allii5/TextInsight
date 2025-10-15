import { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import styles from './Notifications.module.css';

const Notifications = () => {
  const navigate = useNavigate(); // Initialize useNavigate
  const location = useLocation();
  const { state } = location;
  const { data } = state || { data: [] };

  return (
    <div className={styles["notifications-wrapper"]}>
      <div className={styles["main-div"]}>
        <div className={styles["page-title"]}>
          <button className={styles["back-button"]} onClick={() => navigate(-1)}>
            Back
          </button>
          <h2>Notifications</h2>
        </div>

        <div className={styles["notifications-container"]}>
          {data.length > 0 ? (
            data.map((notification) => (
              <div key={notification.id} className={styles["notification-card"]}>
                <div className={styles["notification-text"]}>
                  {notification.message}
                </div>
              </div>
            ))
          ) : (
            <div className={styles["no-notifications"]}>
              There are no notifications at this time.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Notifications;


// import { useState } from 'react';
// import { useNavigate, useLocation } from "react-router-dom";
// import styles from './Notifications.module.css';

// const Notifications = () => {
//   const navigate = useNavigate();
//   const location = useLocation();
//   const { state } = location;
//   const data = state?.data || []; // Ensure data is always an array

//   return (
//     <div className={styles["notifications-wrapper"]}>
//       <div className={styles["main-div"]}>
//         <div className={styles["page-title"]}>
//           <button className={styles["back-button"]} onClick={() => navigate(-1)}>
//             Back
//           </button>
//           <h2>Notifications</h2>
//         </div>

//         <div className={styles["notifications-container"]}>
//           {data.length > 0 ? (
//             data.map((notification) => (
//               <div key={notification.id} className={styles["notification-card"]}>
//                 <div className={styles["notification-text"]}>
//                   {notification.message}
//                 </div>
//               </div>
//             ))
//           ) : (
//             <div className={styles["no-notifications"]}>
//               There are no notifications at this time.
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Notifications;




