# Model description (1 page)

System name: "Resume Radar" - resume screening and scoring system
Purpose: extract skills and experience from submitted resumes, output a 1-100 score and a ranking for hiring managers to use; directly involved in hiring decisions.
Model: large language model (hosted via a third-party API); no self-trained foundation model; uses historical resumes for fine-tuning / prompt engineering.
Data: candidate resume text (including personal information such as names and phone numbers); training data includes roughly 200K historical resumes.
Output: score and ranking, with a brief reason statement.
Users: hiring managers (internal, ~300-person company).
Affected persons: job applicants.
Deployment: cloud API; European data stored in a Frankfurt data center.
Self-assessed risk: high (employment domain).
