from html import escape


def render_issue_html(headlines, prompts, skills):
    """
    Build a simple HTML newsletter from three content sections:
    - headlines: list of dicts with title, url, summary
    - prompts: list of dicts with title, category, tool, prompt_text, why_it_works
    - skills: list of dicts with title, lesson_text, example_prompt
    """

    def section_title(text):
        return f"""
        <h2 style="margin-top:32px;margin-bottom:12px;font-size:22px;">
            {escape(text)}
        </h2>
        """

    def render_headlines(items):
        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            url = escape(item.get("url", "#"))
            summary = escape(item.get("summary", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #e5e7eb;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">
                    <a href="{url}" style="color:#111827;text-decoration:none;">{title}</a>
                </h3>
                <p style="margin:0;color:#374151;line-height:1.5;">{summary}</p>
            </div>
            """)
        return "\n".join(blocks)

    def render_prompts(items):
        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            category = escape(item.get("category", "General"))
            tool = escape(item.get("tool", "ChatGPT"))
            prompt_text = escape(item.get("prompt_text", ""))
            why_it_works = escape(item.get("why_it_works", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #e5e7eb;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">{title}</h3>
                <p style="margin:0 0 8px 0;color:#6b7280;">
                    <strong>Category:</strong> {category}
                    &nbsp;|&nbsp;
                    <strong>Tool:</strong> {tool}
                </p>
                <p style="margin:0 0 8px 0;white-space:pre-wrap;color:#111827;"><strong>Prompt:</strong><br>{prompt_text}</p>
                <p style="margin:0;color:#374151;"><strong>Why it works:</strong> {why_it_works}</p>
            </div>
            """)
        return "\n".join(blocks)

    def render_skills(items):
        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            lesson_text = escape(item.get("lesson_text", ""))
            example_prompt = escape(item.get("example_prompt", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #e5e7eb;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">{title}</h3>
                <p style="margin:0 0 8px 0;color:#374151;line-height:1.5;">{lesson_text}</p>
                <p style="margin:0;white-space:pre-wrap;color:#111827;"><strong>Example prompt:</strong><br>{example_prompt}</p>
            </div>
            """)
        return "\n".join(blocks)

    headlines_html = render_headlines(headlines)
    prompts_html = render_prompts(prompts)
    skills_html = render_skills(skills)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Daily Prompt</title>
    </head>
    <body style="margin:0;padding:0;background:#f9fafb;font-family:Arial,Helvetica,sans-serif;color:#111827;">
        <div style="max-width:760px;margin:0 auto;padding:32px 20px;">
            <div style="background:white;border:1px solid #e5e7eb;border-radius:14px;padding:32px;">
                <h1 style="margin-top:0;margin-bottom:8px;font-size:32px;">The Daily Prompt</h1>
                <p style="margin-top:0;margin-bottom:24px;color:#4b5563;font-size:16px;">
                    The daily AI briefing for ambitious professionals who want to win at work and in life.
                </p>

                {section_title("Top AI Headlines")}
                {headlines_html}

                {section_title("Prompts That Save Time")}
                {prompts_html}

                {section_title("AI Skill Builder")}
                {skills_html}
            </div>
        </div>
    </body>
    </html>
    """
