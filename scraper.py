from typing import List
import requests
from bs4 import BeautifulSoup


# Data structure for holding resume information
class Resume:
    def __init__(
        self,
        name: str,
        job_position: str,
        experience: int,
        skills: List[str],
        location: str,
        salary: int,
        resume_link: str,
    ):
        self.name = name
        self.job_position = job_position
        self.experience = experience
        self.skills = skills
        self.location = location
        self.salary = salary
        self.resume_link = resume_link

    def __repr__(self):
        return f"<Resume {self.name}, {self.job_position}, {self.experience} years>"


# Utility function to extract salary from HTML content
def extract_salary(salary_tag) -> int:
    if salary_tag:
        salary_str = salary_tag.text.strip().replace(" ", "").replace("грн", "").strip()
        return int(salary_str) if salary_str.isdigit() else 0
    return 0


# Updated scraping function for work.ua
def scrape_work_ua(max_pages: int = 5) -> List[Resume]:
    base_url = "https://www.work.ua/resumes/"
    resumes = []
    page = 1

    while page <= max_pages:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all resume cards in the page
        resume_cards = soup.find_all("div", class_="resume-link")
        if not resume_cards:
            break  # Stop if no more resumes are found (last page)

        for resume in resume_cards:
            # Extract job position
            job_position_tag = resume.find("h2", class_="mt-0").find("a")
            job_position = job_position_tag.text.strip() if job_position_tag else "N/A"

            # Extract name, age, and location
            personal_info_tag = resume.find("p", class_="mt-xs mb-0")
            if personal_info_tag:
                personal_info_text = personal_info_tag.text.strip().split(", ")
                name = personal_info_text[0]
                age = personal_info_text[1] if len(personal_info_text) > 1 else "N/A"
                location = (
                    personal_info_text[2] if len(personal_info_text) > 2 else "N/A"
                )
            else:
                name = "N/A"
                age = "N/A"
                location = "N/A"

            # Extract salary if available
            salary_tag = resume.find("p", class_="h5 strong-600 mt-xs mb-0 nowrap")
            salary = extract_salary(salary_tag)

            # Extract resume link
            resume_link = job_position_tag["href"] if job_position_tag else "N/A"

            # Since the experience and skills weren't visible in the provided HTML,
            # let's assume these are placeholders until you provide further details
            experience = 0  # Placeholder
            skills = []  # Placeholder

            resume_obj = Resume(
                name, job_position, experience, skills, location, salary, resume_link
            )
            resumes.append(resume_obj)

        page += 1

    return resumes


# Example usage:
if __name__ == "__main__":
    max_pages_to_scrape = 3  # Adjust as needed

    # Fetch resumes and print them
    resumes = scrape_work_ua(max_pages=max_pages_to_scrape)

    # Output the fetched resumes
    for resume in resumes:
        print(resume)
