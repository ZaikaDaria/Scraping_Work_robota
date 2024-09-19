import requests
from bs4 import BeautifulSoup
from resume import Resume
from utils import extract_salary


def parse_robota_ua_resume(page: int = 1):
    base_url = f"https://robota.ua/candidates/all/ukraine?page={page}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    resumes = []
    resume_cards = soup.find_all('div', class_='santa-p-20 santa-box-border ng-star-inserted')

    for resume in resume_cards:
        job_position_tag = resume.find('p', class_='santa-typo-regular-bold')
        job_position = job_position_tag.text.strip() if job_position_tag else "N/A"
        name_tag = resume.find('p', class_='santa-typo-secondary')
        name = name_tag.text.strip() if name_tag else "Anonymous"
        location_tag = resume.find('p', class_='santa-typo-secondary santa-truncate')
        location = location_tag.text.strip() if location_tag else "N/A"
        salary_tag = resume.find('p', class_='santa-typo-secondary', string=lambda t: 'грн' in t)
        salary = extract_salary(salary_tag)

        resume_obj = Resume(name, job_position, 0, [], location, salary, "N/A")
        resumes.append(resume_obj)

    return resumes


def parse_work_ua_resume(page: int = 1):
    base_url = f"https://www.work.ua/resumes/?page={page}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    resumes = []
    resume_cards = soup.find_all("div", class_="resume-link")

    for resume in resume_cards:
        job_position_tag = resume.find("h2", class_="mt-0").find("a")
        job_position = job_position_tag.text.strip() if job_position_tag else "N/A"
        personal_info_tag = resume.find("p", class_="mt-xs mb-0")
        personal_info_text = personal_info_tag.text.strip().split(", ") if personal_info_tag else []
        name = personal_info_text[0] if len(personal_info_text) > 0 else "N/A"
        location = personal_info_text[2] if len(personal_info_text) > 2 else "N/A"
        salary_tag = resume.find("p", class_="h5 strong-600 mt-xs mb-0 nowrap")
        salary = extract_salary(salary_tag)
        resume_link = job_position_tag["href"] if job_position_tag else "N/A"

        resume_obj = Resume(name, job_position, 0, [], location, salary, resume_link)
        resumes.append(resume_obj)

    return resumes
