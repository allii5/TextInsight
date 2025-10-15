import React, { useEffect, useState } from "react";
import styles from "./LoadingAnimation.module.css";

const LoadingAnimation = ({ onCompletion }) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const steps = [
    "Validating emails",
    "Generating credentials",
    "Creating accounts",
    "Sending notifications"
  ];

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        const newProgress = Math.min(prev + 25, 100);
        if (newProgress % 25 === 0) {
          setCurrentStep(prevStep => Math.min(prevStep + 1, steps.length));
        }
        return newProgress;
      });
    }, 2500);

    return () => clearInterval(progressInterval);
  }, []);

  useEffect(() => {
    if (progress === 100) {
      const completionTimer = setTimeout(() => {
        onCompletion?.();
      }, 2000);
      return () => clearTimeout(completionTimer);
    }
  }, [progress, onCompletion]);

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <div className={styles.loaderContainer}>
          <div className={`${styles.spinner} ${progress === 100 ? styles.hidden : ''}`} />
          <svg 
            className={`${styles.checkmark} ${progress === 100 ? styles.visible : ''}`}
            viewBox="0 0 52 52"
          >
            <path
              className={`${styles.checkmarkPath} ${progress === 100 ? styles.animate : ''}`}
              fill="none"
              d="M14.1 27.2l7.1 7.2 16.7-16.8"
            />
          </svg>
        </div>

        <div className={styles.processingText}>
          <h3>{progress === 100 ? "All Set!" : "Creating Accounts..."}</h3>
        </div>

        <div className={styles.progressContainer}>
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{ width: `${progress}%` }}
            />
          </div>
          <span className={styles.progressText}>{progress}%</span>
        </div>

        <div className={styles.statusMessage}>
          <p>Current Progress:</p>
          <ul>
            {steps.map((step, index) => (
              <li
                key={step}
                className={`${styles.stepItem} ${index < currentStep ? styles.completed : ''}`}
              >
                {step}
                {index < currentStep && <span className={styles.stepCheck}>&#10003;</span>}
              </li>
            ))}
          </ul>
          
          {progress === 100 && (
            <p className={styles.completionText}>
              ✓ All student accounts created successfully!
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoadingAnimation;