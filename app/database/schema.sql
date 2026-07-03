CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_history (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    resume_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(180) NOT NULL,
    match_score INT NOT NULL,
    ats_score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_analysis_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
);

CREATE TABLE reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    analysis_id INT NOT NULL,
    matching_skills JSON NOT NULL,
    missing_skills JSON NOT NULL,
    resume_summary TEXT NOT NULL,
    suggestions JSON NOT NULL,
    CONSTRAINT fk_report_analysis
        FOREIGN KEY (analysis_id) REFERENCES analysis_history(analysis_id)
        ON DELETE CASCADE
);
