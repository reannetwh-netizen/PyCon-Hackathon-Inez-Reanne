Project Title : Skill Gap Course Finder

What is it? : An AI-powered tool that identifies skill gaps between a user's current job and a target job, then recommends SkillsFuture courses to bridge those gaps.

Problem Statement: How might we help middle-aged workers who confront the challenge of remaining competitive in a rapidly evolving labour market, as they face the threats of professional irrelevance, age bias, and perceptions of being “overqualified”. 

The solution is an app that:

1. Use Open AI to analyze a user's current skills and required skills based on the user's current job and dream job
2. Compares the two sets of skills
3. Identifies missing skills.
4. Recommends relevant SkillsFuture courses based on user's budget. 
5. Uses OpenAI to explain why each course can help the user as well as the potential limitations of the course.

DEMO URL = 

Tech stack:
IDE --> VS Code
Backend and Frontend --> Streamlit
Version control and sharing --> GitHub

Our Datasets used and rationale: 
1. Jobsandskills dataset from SkillsFuture (jobsandskills-skillsfuture-skills-framework-dataset.xlsx) This dataset provides a wide range of jobs and the corresponding skills required. It also provides well written descriptions for the jobs, which works well when we generate embeddings. The dataset is also reliable, as it is sourced from SkillsFuture, a trusted Singapore government-supported platform. 
2. MySkillsFuture Course Directory (https://data.gov.sg/datasets/d_b5802b76f409764c16dde4bf2feb19cd/view?utm_source=chatgpt.com ) This dataset is highly relevant, as it contains the list of MySkillsFuture courses from the MySkilsFuture website. There are many courses, with varied course topics, giving us a good data set to work with. There were also details on course fees etc, which will help us better tailor to the needs and budgets of our user. The dataset is also reliable, as it is sourced from MySkillsFuture, a trusted Singapore government-supported platform. 




