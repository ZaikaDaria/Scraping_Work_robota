from resume import Resume
from typing import List


def extract_salary(salary_tag) -> int:
    if salary_tag:
        salary_str = salary_tag.text.strip().replace(" ", "").replace("грн", "").strip()
        return int(salary_str) if salary_str.isdigit() else 0
    return 0


def score_resume(resume: Resume, target_job: str, min_experience: int, required_skills: List[str]) -> int:
    score = 0
    if target_job.lower() in resume.job_position.lower():
        score += 5  # Job position match
    if resume.experience >= min_experience:
        score += 3  # Experience match
    skill_matches = sum(1 for skill in required_skills if skill.lower() in [s.lower() for s in resume.skills])
    score += skill_matches  # Skill match score
    return score


def sort_resumes(resumes: List[Resume], target_job: str, min_experience: int, required_skills: List[str]) -> List[
    Resume]:
    return sorted(
        resumes,
        key=lambda resume: score_resume(resume, target_job, min_experience, required_skills),
        reverse=True
    )
