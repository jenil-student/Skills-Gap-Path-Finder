# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Step 1: Load and preprocess the dataset
data = pd.read_csv('indeed_job_dataset.csv')
data = data.dropna(subset=['Job_Title', 'Description'])
print("Sample Jobs:\n", data[['Job_Title', 'Company']].head())

# Step 2: User input
print("\nEnter your current skills (e.g., Python, SQL, teamwork) separated by commas:")
user_skills = set(input().lower().split(', '))
print("Enter your target job type (e.g., Data Scientist, Software Engineer, IT Specialist):")
target_job = input().lower()

# Step 3: Filter jobs and extract skills with Pandas
target_jobs = data[data['Job_Title'].str.lower().str.contains(target_job, na=False)]
all_descriptions = ' '.join(target_jobs['Description'].str.lower())

# Common technical skills to look for (expandable list)
tech_skills = ['python', 'sql', 'java', 'javascript', 'machine learning', 'data analysis', 
               'cloud', 'aws', 'git', 'linux', 'networking', 'cybersecurity', 'excel', 
               'teamwork', 'communication', 'problem solving']

# Count skill mentions
skill_counts = Counter({skill: all_descriptions.count(skill) for skill in tech_skills})
top_skills = dict(skill_counts.most_common(10))  # Top 10 skills
print(f"\nTop Skills for {target_job}:\n", top_skills)

# Step 4: Identify skill gaps with NumPy
user_skill_set = set(user_skills)
job_skill_set = set(top_skills.keys())
missing_skills = job_skill_set - user_skill_set
gap_scores = {skill: top_skills[skill] for skill in missing_skills}
print("\nYour Skill Gaps:\n", gap_scores)

# Step 5: Visualization 1 - Skill Galaxy Heatmap
skill_freq = np.array([top_skills.get(skill, 0) for skill in tech_skills])
heatmap_data = skill_freq.reshape(4, 4)  # Reshape for a 4x4 grid
plt.figure(figsize=(10, 8))
plt.imshow(heatmap_data, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Skill Demand (Mentions)')
plt.xticks(np.arange(len(tech_skills[::4])), tech_skills[::4], rotation=45, ha='right')
plt.yticks(np.arange(len(tech_skills[::4])), tech_skills[::4])
plt.title(f'Skill Galaxy for {target_job}', fontsize=14)
plt.tight_layout()
plt.savefig('skill_galaxy.png')
plt.show()

# Step 6: Visualization 2 - Skill Gap Bar Chart
plt.figure(figsize=(10, 6))
if gap_scores:
    plt.bar(gap_scores.keys(), gap_scores.values(), color='salmon')
    plt.title('Your Skill Gaps to Bridge', fontsize=14)
    plt.ylabel('Demand (Mentions in Job Postings)')
    plt.xticks(rotation=45, ha='right')
else:
    plt.text(0.5, 0.5, 'No Skill Gaps Detected!', fontsize=12, ha='center')
plt.savefig('skill_gap_bar.png')
plt.show()

# Step 7: Visualization 3 - Skill Roadmap
plt.figure(figsize=(12, 6))
plt.plot([0, 1], [0, 0], 'k-', lw=2, label='Your Current Skills')  # Base line
for i, skill in enumerate(user_skills):
    plt.text(0.5, i * 0.1 + 0.1, skill, color='green', fontsize=10, ha='center')
if missing_skills:
    plt.plot([1, 2], [0, 0], 'k--', lw=2, label='Path to Target Job')
    for i, skill in enumerate(missing_skills):
        plt.text(1.5, i * 0.1 + 0.1, skill, color='red', fontsize=10, ha='center')
plt.title(f'Your Skill Roadmap to {target_job}', fontsize=14)
plt.legend()
plt.axis('off')
plt.savefig('skill_roadmap.png')
plt.show()