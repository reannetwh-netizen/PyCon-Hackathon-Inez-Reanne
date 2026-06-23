from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re

#take in user's dream job and current job
#sector of dream job and current job is needed as well as helps shorten the run time of the program
sector1 = input("Input your current job sector:")
current_job = input("Input your current job:")
sector2 = input("Input your dream job sector:")
dream_job = input("Input your dream job:")


client = OpenAI(
    api_key="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"
)

#returns a dictionary where key is the skill and value is a list of information regarding the skill
def get_dict(sector):
    data = pd.read_excel(r"C:\Users\reann\OneDrive\PyCon\copyofjobsandskills-skillsfuture-skills-framework-dataset.xlsx", sheet_name = 'Job Role_TCS_CCS')
    data = data.drop(columns= ['TSC_CCS Type','Proficiency Level', 'TSC_CCS Code'])
    df = data[data["Sector"] == sector]
    df = df.drop(columns = ['Sector', 'Track'])
    result = {}

    for _, row in df.iterrows():
        key = row["TSC_CCS Title"]
        result.setdefault(key, []).extend(row.tolist())
    for key in result:
        result[key] = list(set(result[key]))
    return result

#generate embeddings on a list
def embed(text_list, batch_size=100):
    all_embeddings = []

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )

        batch_embeddings = [np.array(d.embedding) for d in response.data]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


#return the skills where score is greater than 0.5
def detect_skills(job, sector):
    text_list = [job]
    index_map = []
    for skill, terms in get_dict(sector).items():
        for t in terms:
            text_list.append(t)
            index_map.append(skill)

    embeddings = embed(text_list)
    job_vec    = embeddings[0]
    skill_vecs  = embeddings[1:]


    sims = cosine_similarity([job_vec], skill_vecs)[0]

    best_per_skill = {}
    for sim, (skill) in zip(sims, index_map):
        best_per_skill[skill] = max(best_per_skill.get(skill, 0), sim)


    matches = [
        (skill, score)
        for skill, score in best_per_skill.items()
        if score >= 0.5 #0.5 is the threshold
    ]
    return sorted(matches, key=lambda x: x[1], reverse=True)


current_skills = detect_skills(current_job, sector1)
dream_skills = detect_skills(dream_job, sector2)


print("Current Skills:")
for skill, score in current_skills:
    print(f"{skill:20s}  {score:.2f}")
print("Required Skills:")
for skill, score in dream_skills:
    print(f"\n{skill:20s}  {score:.2f}")

#before the next line of code, allow user to verify their current_skills, then update current_skills
current_skills = {skill for skill, _ in current_skills}
dream_skills = {skill for skill, _ in dream_skills}

missing_skills= list(dream_skills- current_skills)
print("The following are your missing skills:")
print(missing_skills)
#before the next line of code, allow user to verify their missing_skills, then update missing_skills


df2 = pd.read_excel(r"C:\Users\reann\OneDrive\PyCon\copyofMySkillsFutureCourseDirectory.xlsx")


#drop columns such that df2 has 4 columns: 'coursetitle', 'about_this_course', 'course_fee_after_subsidies','what_you_learn'
df2 = df2.drop(columns= ['coursereferencenumber', 'trainingprovideruen',
       'trainingprovideralias', 'courseratings_value', 'courseratings_stars',
       'courseratings_noofrespondents', 'jobcareer_impact_value',
       'jobcareer_impact_stars', 'jobcareer_impact_noofrespondents',
       'attendancecount', 'full_course_fee',
       'number_of_hours', 'training_commitment', 'conducted_in', 'minimum_entry_requirement'])

budget = int(input("What is your budget?"))

#filter courses by budget and skills to be learnt
def get_course(skill):
    courses = []
    for course, fees, about, learn in df2.itertuples(index=False):
        if re.search(rf"\b{skill}\b", str(about), re.IGNORECASE) and fees <= budget:
            courses.append(course)
        elif re.search(rf"\b{skill}\b", str(learn), re.IGNORECASE) and fees <= budget:
            courses.append(course)
    return courses

for skill in missing_skills:
    print(get_course(skill))


#allow user to choose a course to explore more
course_chosen = input("Which course would you like to find out more about?")

df2 = pd.read_excel(r"C:\Users\reann\OneDrive\PyCon\copyofMySkillsFutureCourseDirectory.xlsx")


# collate all information about the course 
course_info = "\n".join(
    f"{col}={val}"
    for col, val in df2[df2["coursetitle"] == course_chosen].iloc[0].items()
)

print(course_info)

# AI course recommendation explainer
def explain_course(
    current_skills,
    current_job,
    missing_skills,
    dream_job,
    course_info
):
    prompt = f"""
You are a course recommendation explainer.

User profile:
Current job: {current_job}
Current skills: {current_skills}
Dream job: {dream_job}
Missing skills: {missing_skills}

Course information:{course_info}

Explain why this course can help the user in 5 lines. Include:
1. Which missing skills the course helps with
2. How it helps the user move from current job to dream job
3. Any limitations of the course
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

print(explain_course(current_skills, current_job, missing_skills, dream_job, course_info))
