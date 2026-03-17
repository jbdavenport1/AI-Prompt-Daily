from app.news import fetch_news
from app.prompts import load_prompts
from app.skills import load_skills
from app.render import render_issue_html


def main():
    headlines = fetch_news(limit_per_feed=5)
    prompts = load_prompts()[:3]
    skills = load_skills()[:2]

    html = render_issue_html(headlines, prompts, skills)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Newsletter written to output.html")


if __name__ == "__main__":
    main()
