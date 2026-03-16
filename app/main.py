from app.news import fetch_news
from app.render import render_issue_html


def main():
    headlines = fetch_news(limit_per_feed=5)

    prompts = [
        {
            "title": "Turn a rough idea into a clear plan",
            "category": "productivity",
            "tool": "ChatGPT",
            "prompt_text": "Turn this rough idea into a step-by-step action plan with the first 3 actions I should take today: [paste idea]",
            "why_it_works": "It forces structure and gives you an immediate next move."
        }
    ]

    skills = [
        {
            "title": "Be specific about the outcome",
            "lesson_text": "Better prompts name the exact output you want, the format, and the audience.",
            "example_prompt": "Write a 150-word LinkedIn post for financial advisors on why AI matters now."
        }
    ]

    html = render_issue_html(headlines, prompts, skills)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Newsletter written to output.html")


if __name__ == "__main__":
    main()
