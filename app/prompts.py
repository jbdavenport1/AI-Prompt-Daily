import csv


def load_prompts(path="data/seed_prompts.csv"):
    prompts = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append(row)

    return prompts
