import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styles from "./ExploreInsight.module.css";

const ExploreInsight = () => {
  const [feedbackType, setFeedbackType] = useState("intra");
  const [selectedKeywordTab, setSelectedKeywordTab] = useState("Introduction");
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = location;
  const { title, feedbackData } = state || {};

  const keywordTabs = ["Introduction", "Body", "Conclusion", "Foundation", "Framing", "Resolution", "Core"];

  const keywordsMapping = {
    Introduction: feedbackData?.intro_keywords || [],
    Body: feedbackData?.middle_keywords || [],
    Conclusion: feedbackData?.conclusion_keywords || [],
    Foundation: feedbackData?.intro_mid_keywords || [],
    Framing: feedbackData?.intro_conclusion_keywords || [],
    Resolution: feedbackData?.mid_conclusion_keywords || [],
    Core: feedbackData?.intro_mid_conclusion_keywords || [],
  };

  const backend_url = "http://127.0.0.1:8000";

  const renderKeywords = () => {
    const currentKeywords = keywordsMapping[selectedKeywordTab] || [];
    return (
      <div className={styles["keywords-list"]}>
        {currentKeywords.map((keyword, index) => (
          <div key={index} className={styles["keyword-item"]}>
            {keyword}
          </div>
        ))}
      </div>
    );
  };

  const handleInterEssayFeedback = () => {
    setFeedbackType("inter");
    navigate("/essayinsight", {
      state: {
        title,
        feedbackData,
        feedbackType: "inter",
      },
    });
  };

  return (
    <div className={styles["page-wrapper"]}>
      <div className={styles["explore-insight"]}>
        {/* Back Button */}
        <button className={styles["back-button"]} onClick={() => navigate(-1)}>
          Back
        </button>

        <div className={styles.header}>
          <h1 className={styles["main-title"]}>Your Essay Feedback</h1>
          <div className={styles["switch-container"]}>
            <button
              className={`${styles["switch-button"]} ${feedbackType === "intra" ? styles["active"] : ""}`}
              onClick={() => setFeedbackType("intra")}
            >
              Intra-Essay Feedback
            </button>
            <button
              className={`${styles["switch-button"]} ${feedbackType === "inter" ? styles["active"] : ""}`}
              onClick={handleInterEssayFeedback}
            >
              Inter-Essay Feedback
            </button>
          </div>
          <h2 className={styles["section-title"]}>Explore Insights and Feedback</h2>
          <h2 className={styles["essay-title"]}>Essay Title: {title}</h2>
        </div>

        <div className={styles["info-card"]}>
          <p className={styles["info-text"]}>
            Visualize your essay's strengths and areas for growth with detailed insights. Use
            the Venn diagram to see keyword overlap counts for Foundation (Intro → Body),
            Framing (Intro → Conclusion), Core (Intro → Body → Conclusion), and Resolution
            (Body → Conclusion). Explore the specific keywords separately, alongside the word
            cloud, keyword graph, and actionable suggestions to refine your writing.
          </p>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Feedback</h3>
          <div className={styles["section-content"]}>
            <div className={styles["feedback-content"]}>
              {feedbackType === "intra" && (
                <div dangerouslySetInnerHTML={{ __html: feedbackData?.intra_essay_feedback || "" }} />
              )}
            </div>
          </div>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Keywords</h3>
          <div className={styles["section-content"]}>
            <div className={styles["switch-container"]}>
              {keywordTabs.map((tab) => (
                <button
                  key={tab}
                  className={`${styles["switch-button"]} ${selectedKeywordTab === tab ? styles["active"] : ""}`}
                  onClick={() => setSelectedKeywordTab(tab)}
                >
                  {tab}
                </button>
              ))}
            </div>
            {renderKeywords()}
          </div>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Venn Diagram</h3>
          <div className={styles["section-content"]}>
            {feedbackData?.venn_diagram_image ? (
              <img src={`${backend_url}${feedbackData.venn_diagram_image}`} alt="Venn Diagram" />
            ) : (
              <p>Please wait until more submissions are made.</p>
            )}
          </div>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Keyword Graph</h3>
          <div className={styles["section-content"]}>
            <div className={styles["keyword-graph-content"]}>
              {feedbackData.keyword_graph_html ? (
                <iframe
                src={`${backend_url}${feedbackData.keyword_graph_html}`}
                title="Keyword Graph"
                width="100%"
                height="600px"
                ></iframe>
              ) : (
                <p>Please wait until more submissions are made.</p>
              )}
            </div>
          </div>
        </div>

        <div className={styles["section-container"]}>
          <h3 className={styles["section-header"]}>Word Cloud</h3>
          <div className={styles["section-content"]}>
            <div className={styles["word-cloud-content"]}>
              {feedbackData.wordcloud_image ? (
                <img
                  src={`${backend_url}${feedbackData.wordcloud_image}`}
                  alt="Word Cloud"
                />
              ) : (
                <p>Please wait until more submissions are made.</p>
              )}
            </div>
          </div>
        </div>

      </div>
    </div>



    
  );
};

export default ExploreInsight;
