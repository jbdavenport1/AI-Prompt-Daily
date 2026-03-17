import csv


def load_skills(path="data/seed_skills.csv"):
    skills = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            skills.append(row)

    return skills


def get_skill_slice(count=2, offset=0, path="data/seed_skills.csv"):
    skills = load_skills(path)

    if not skills:
        return []

    total = len(skills)
    selected = []

    for i in range(count):
        index = (offset + i) % total
        selected.append(skills[index])

    return selected
