import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./EssayInsight.module.css";

const EssayInsight = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = location;
  const { title, feedbackData, feedbackType: initialFeedbackType } = state || {};

  const [feedbackType, setFeedbackType] = useState(initialFeedbackType || "inter");

  const handleIntraEssayFeedback = () => {
    setFeedbackType("intra");
    navigate("/exploreinsight", {
      state: {
        title,
        feedbackData,
        feedbackType: "intra",
      },
    });
  };

  return (
    <div className={styles["page-wrapper"]}>
      <div className={styles["essay-insight"]}>
        <button className={styles["back-button"]} onClick={() => navigate(-1)}>
          Back
        </button>

        <div className={styles.header}>
          <h1 className={styles["main-title"]}>Your Essay Feedback</h1>
          <div className={styles["switch-container"]}>
            <button
              className={`${styles["switch-button"]} ${feedbackType === "intra" ? styles["active"] : ""}`}
              onClick={handleIntraEssayFeedback}
            >
              Intra-Essay Feedback
            </button>
            <button
              className={`${styles["switch-button"]} ${feedbackType === "inter" ? styles["active"] : ""}`}
              onClick={() => setFeedbackType("inter")}
            >
              Inter-Essay Feedback
            </button>
          </div>
          <h2 className={styles["section-title"]}>Cross-Essay Insights</h2>
          <h2 className={styles["essay-title"]}>Essay Title: {title}</h2>
        </div>

        {/* Info Card */}
        <div className={styles["info-card"]}>
          <p className={styles["info-text"]}>
            See how this essay has evolved through your submissions. Compare versions,
            review feedback, and measure your progress.
          </p>
        </div>

        {/* Chart Section */}
        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Radar Wheel</h3>
          <div className={styles["section-content"]}>
            <div className={styles["chart-container"]}>
              {feedbackData.radar_wheel_image ? (
                <img src={`${"http://127.0.0.1:8000"}${feedbackData.radar_wheel_image}`} alt="Radar Wheel" className={styles["bar-chart-image"]} />
              ) : (
                <p>Please wait until more submissions are made.</p>
              )}
            </div>
          </div>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Feedback</h3>
          <div className={styles["section-content"]}>
            <div className={styles["feedback-content"]}>
              <div dangerouslySetInnerHTML={{ __html: feedbackData?.inter_essay_feedback || "" }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EssayInsight;
