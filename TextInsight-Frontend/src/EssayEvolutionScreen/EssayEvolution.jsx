import { useLocation, useNavigate } from "react-router-dom";
import styles from "./EssayEvolution.module.css";

const EssayEvolution = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { title, progressData } = location.state || {};
  const backend_url = "http://127.0.0.1:8000";

  return (
    <div className={styles["page-wrapper"]}>
      <div className={styles["essay-insight"]}>
        {/* Back Button */}
        <button className={styles["back-button"]} onClick={() => navigate(-1)}>
          Back
        </button>

        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles["section-title"]}>Your Essay Feedback</h1>
          <h2 className={styles["essay-title"]}>Essay Title: {title || "N/A"}</h2>
        </div>

        {/* Info Card */}
        <div className={styles["info-card"]}>
          <p className={styles["info-text"]}>
            See how this essay has evolved through your submissions. Compare
            versions, review feedback, and measure your progress.
          </p>
        </div>

        {/* Graph Section */}
        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Graph Analysis</h3>
          <div className={styles["section-content"]}>
            <div className={styles["chart-container"]}>
              {progressData.graph_image ? (
                <img
                  src={`${backend_url}${progressData.graph_image}`}
                  alt="Graph Analysis"
                  className={styles["bar-chart-image"]}
                />
              ) : (
                <p>No graph available.</p>
              )}
            </div>
          </div>
        </div>

        {/* Feedback Section */}
        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Feedback Summary</h3>
          <div className={styles["section-content"]}>
            <p className={styles["feedback-content"]}>
              Here’s an analysis of your progress based on the latest submissions:
            </p>
            {progressData.compared_feedback ? (
              <div
                dangerouslySetInnerHTML={{ __html: progressData.compared_feedback }}
              />
            ) : (
              <p>No feedback available.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EssayEvolution;
