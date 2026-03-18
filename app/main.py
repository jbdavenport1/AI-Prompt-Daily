from datetime import datetime
from pathlib import Path
import json
import shutil

from app.news import fetch_news
from app.prompts import get_prompt_slice
from app.skills import get_skill_slice
from app.render import render_issue_html


def build_offsets():
    day_of_year = datetime.now().timetuple().tm_yday
    prompt_offset = day_of_year * 3
    skill_offset = day_of_year * 2
    return prompt_offset, skill_offset


def build_issue_date():
    return datetime.now().strftime("%B %d, %Y")


def build_issue_slug(issue_date: str) -> str:
    return issue_date.lower().replace(", ", "-").replace(" ", "-")


def build_subject(headlines):
    if headlines and len(headlines) > 0:
        return f"The Daily Prompt | {headlines[0]['title']}"
    return "The Daily Prompt"


def build_preview(headlines, prompts):
    parts = []

    if headlines and len(headlines) > 0:
        parts.append(headlines[0]["title"])

    if prompts and len(prompts) > 0:
        parts.append(f"Plus: {prompts[0]['title']}")

    preview = " | ".join(parts)

    if not preview:
        preview = "Daily AI headlines, practical prompts, and skill builders."

    return preview[:180]


def build_plain_text(headlines, prompts, skills, issue_date=""):
    lines = []

    lines.append("The Daily Prompt")
    lines.append("The daily AI briefing for ambitious professionals who want to win at work and in life.")

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

    return "\n".join(lines).strip() + "\n"


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_meta_file(
    path: Path,
    issue_date: str,
    issue_slug: str,
    subject: str,
    preview: str,
    headlines: list,
    prompts: list,
    skills: list,
) -> None:
    meta = {
        "issue_date": issue_date,
        "issue_slug": issue_slug,
        "subject": subject,
        "preview": preview,
        "headline_titles": [item["title"] for item in headlines],
        "prompt_titles": [item["title"] for item in prompts],
        "skill_titles": [item["title"] for item in skills],
    }

    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def main():
    headlines = fetch_news(limit_per_feed=5)
    prompt_offset, skill_offset = build_offsets()
    prompts = get_prompt_slice(count=3, offset=prompt_offset)
    skills = get_skill_slice(count=2, offset=skill_offset)

    issue_date = build_issue_date()
    issue_slug = build_issue_slug(issue_date)
    subject = build_subject(headlines)
    preview = build_preview(headlines, prompts)

    html = render_issue_html(
        headlines,
        prompts,
        skills,
        issue_date=issue_date,
    )

    plain_text = build_plain_text(
        headlines,
        prompts,
        skills,
        issue_date=issue_date,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_root = Path("output")
    run_dir = output_root / timestamp
    latest_dir = output_root / "latest"

    run_dir.mkdir(parents=True, exist_ok=True)

    write_text_file(run_dir / "issue.html", html)
    write_text_file(run_dir / "issue.txt", plain_text)
    write_text_file(run_dir / "subject.txt", subject)
    write_text_file(run_dir / "preview.txt", preview)
    write_meta_file(
        run_dir / "meta.json",
        issue_date,
        issue_slug,
        subject,
        preview,
        headlines,
        prompts,
        skills,
    )

    if latest_dir.exists():
        shutil.rmtree(latest_dir)

    latest_dir.mkdir(parents=True, exist_ok=True)

    write_text_file(latest_dir / "issue.html", html)
    write_text_file(latest_dir / "issue.txt", plain_text)
    write_text_file(latest_dir / "subject.txt", subject)
    write_text_file(latest_dir / "preview.txt", preview)
    write_meta_file(
        latest_dir / "meta.json",
        issue_date,
        issue_slug,
        subject,
        preview,
        headlines,
        prompts,
        skills,
    )

    print(f"Issue date: {issue_date}")
    print(f"Subject: {subject}")
    print(f"Preview: {preview}")

    print("\nSelected prompts:")
    for prompt in prompts:
        print(f"- {prompt['title']}")

    print("\nSelected skills:")
    for skill in skills:
        print(f"- {skill['title']}")

    print(f"\nSaved run to: {run_dir}")
    print(f"Updated latest at: {latest_dir}")


if __name__ == "__main__":
    main()
