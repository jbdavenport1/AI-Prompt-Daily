import csv


def load_prompts(path="data/seed_prompts.csv"):
    prompts = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append(row)

    return prompts


def get_prompt_slice(count=3, offset=0, path="data/seed_prompts.csv"):
    prompts = load_prompts(path)

    if not prompts:
        return []

    total = len(prompts)
    selected = []

    for i in range(count):
        index = (offset + i) % total
        selected.append(prompts[index])

    return selected
