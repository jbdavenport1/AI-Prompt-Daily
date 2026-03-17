from app.news import fetch_news
from app.prompts import load_prompts
from app.skills import load_skills
from app.render import render_issue_html


def build_subject():
    return "The Daily Prompt: AI news, prompts, and skills"


def build_preview():
    return "Today’s top AI headlines, 3 useful prompts, and 2 quick skill builders."


def build_plain_text(headlines, prompts, skills):
    lines = []

    lines.append("The Daily Prompt")
    lines.append("The daily AI briefing for ambitious professionals who want to win at work and in life.")
    lines.append("")

    lines.append("TOP AI HEADLINES")
    lines.append("")
    for item in headlines:
        lines.append(f"- {item.get('title', 'Untitled')}")
        lines.append(f"  {item.get('url', '')}")
        summary = item.get("summary", "")
        if summary:
            lines.append(f"  {summary}")
        lines.append("")

    lines.append("TODAY'S PROMPTS")
    lines.append("")
    for item in prompts:
        lines.append(f"- {item.get('title', 'Untitled')}")
        lines.append(f"  Category: {item.get('category', 'General')}")
        lines.append(f"  Tool: {item.get('tool', 'ChatGPT')}")
        lines.append(f"  Prompt: {item.get('prompt_text', '')}")
        lines.append(f"  Why it works: {item.get('why_it_works', '')}")
        lines.append("")

    lines.append("SKILL BUILDER")
    lines.append("")
    for item in skills:
        lines.append(f"- {item.get('title', 'Untitled')}")
        lines.append(f"  Lesson: {item.get('lesson_text', '')}")
        lines.append(f"  Example prompt: {item.get('example_prompt', '')}")
        lines.append("")

    return "\n".join(lines)


def main():
    headlines = fetch_news(limit_per_feed=5)
    prompts = load_prompts()[:3]
    skills = load_skills()[:2]

    subject = build_subject()
    preview = build_preview()
    html = render_issue_html(headlines, prompts, skills)
    plain_text = build_plain_text(headlines, prompts, skills)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("subject.txt", "w", encoding="utf-8") as f:
        f.write(subject)

    with open("preview.txt", "w", encoding="utf-8") as f:
        f.write(preview)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)

    print("Newsletter written to output.html")
    print("Plain text written to output.txt")
    print("Subject written to subject.txt")
    print("Preview written to preview.txt")


if __name__ == "__main__":
    main()
