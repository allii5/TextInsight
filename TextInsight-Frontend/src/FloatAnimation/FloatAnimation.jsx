import React, { useEffect, useState } from "react";
import styles from "./FloatAnimation.module.css";

const FloatAnimation = ({ onClose }) => {
  const [progress, setProgress] = useState(0);
  const [words] = useState(() => 
    Array(15).fill("TextInsight").map((_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      rotate: Math.random() * 60 - 30,
      scale: 0.8 + Math.random() * 1.2
    }))
  );

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress(prev => Math.min(prev + 2, 100));
    }, 1100);

    return () => clearInterval(progressInterval);
  }, []);

  return (
    <div className={styles.overlay} onClick={onClose}>
      {/* Floating words background */}
      <div className={styles.titleContainer}>
        {words.map(({ id, left, top, rotate, scale }) => (
          <div 
            key={id}
            className={styles.titleWord}
            style={{
              left: `${left}%`,
              top: `${top}%`,
              transform: `rotate(${rotate}deg) scale(${scale})`,
              animationDelay: `${id * 0.2}s`,
              fontSize: `${1.8 + scale * 0.5}rem`
            }}
          >
            TextInsight
          </div>
        ))}
      </div>

      {/* Main content */}
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        {/* Centered circular progress */}
        <div className={styles.circleWrapper}>
          <div className={styles.circleProgress}>
            <div 
              className={styles.progress}
              style={{
                background: `conic-gradient(#06aff0 ${progress * 3.6}deg, #e0f7fa 0)`
              }}
            />
            <div className={styles.innerCircle}>
              <span className={styles.percentage}>{progress}%</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default FloatAnimation;