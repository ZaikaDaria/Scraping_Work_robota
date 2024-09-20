from typing import List


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
