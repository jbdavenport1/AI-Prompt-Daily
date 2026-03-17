from datetime import datetime

from app.news import fetch_news
from app.prompts import get_prompt_slice
from app.skills import get_skill_slice
from app.render import render_issue_html


def build_subject(headlines):
    if headlines:
        return f"The Daily Prompt: {headlines[0].get('title', 'Top AI News')}"
    return "The Daily Prompt: Your Daily AI Briefing"


def build_preview(headlines, prompts):
    headline = headlines[0].get("title", "Top AI News") if headlines else "Top AI News"
    prompt_title = prompts[0].get("title", "Daily Prompt") if prompts else "Daily Prompt"
    return f"{headline} | Plus: {prompt_title}"


def build_plain_text(headlines, prompts, skills, issue_date=None):
    lines = []
    lines.append("THE DAILY PROMPT")
    if issue_date:
        lines.append(issue_date)
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


def build_issue_date():
    return datetime.now().strftime("%B %d, %Y")


def build_offsets():
    day_of_year = datetime.now().timetuple().tm_yday
    prompt_offset = day_of_year * 3
    skill_offset = day_of_year * 2
    return prompt_offset, skill_offset


def main():
    headlines = fetch_news(limit_per_feed=5)
    prompt_offset, skill_offset = build_offsets()
    prompts = get_prompt_slice(count=3, offset=prompt_offset)
    skills = get_skill_slice(count=2, offset=skill_offset)

    issue_date = build_issue_date()
    subject = build_subject(headlines)
    preview = build_preview(headlines, prompts)
    html = render_issue_html(headlines, prompts, skills, issue_date=issue_date)
    plain_text = build_plain_text(headlines, prompts, skills, issue_date=issue_date)

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
    print("")
    print("Selected prompts:")
    for item in prompts:
        print(f"- {item.get('title', 'Untitled')}")
    print("")
    print("Selected skills:")
    for item in skills:
        print(f"- {item.get('title', 'Untitled')}")


if __name__ == "__main__":
    main()
