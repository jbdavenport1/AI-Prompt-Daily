import csv


def load_skills(path="data/seed_skills.csv"):
    skills = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            skills.append(row)

    return skills
