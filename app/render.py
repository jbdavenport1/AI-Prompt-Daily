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
        if not items:
            return "<p>No headlines available today.</p>"

        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            url = escape(item.get("url", "#"))
            summary = escape(item.get("summary", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #ddd;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">
                    <a href="{url}" style="text-decoration:none;color:#111;">{title}</a>
                </h3>
                <p style="margin:0;color:#444;line-height:1.5;">{summary}</p>
            </div>
            """)

        return "\n".join(blocks)

    def render_prompts(items):
        if not items:
            return "<p>No prompts available today.</p>"

        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            category = escape(item.get("category", "General"))
            tool = escape(item.get("tool", "ChatGPT"))
            prompt_text = escape(item.get("prompt_text", ""))
            why_it_works = escape(item.get("why_it_works", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #ddd;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">{title}</h3>
                <p style="margin:0 0 8px 0;color:#666;">
                    <strong>Category:</strong> {category}
                    &nbsp;|&nbsp;
                    <strong>Tool:</strong> {tool}
                </p>
                <p style="margin:0 0 8px 0;white-space:pre-wrap;color:#222;"><strong>Prompt:</strong><br>{prompt_text}</p>
                <p style="margin:0;color:#444;line-height:1.5;"><strong>Why it works:</strong> {why_it_works}</p>
            </div>
            """)

        return "\n".join(blocks)

    def render_skills(items):
        if not items:
            return "<p>No skills available today.</p>"

        blocks = []
        for item in items:
            title = escape(item.get("title", "Untitled"))
            lesson_text = escape(item.get("lesson_text", ""))
            example_prompt = escape(item.get("example_prompt", ""))

            blocks.append(f"""
            <div style="margin-bottom:20px;padding:16px;border:1px solid #ddd;border-radius:10px;">
                <h3 style="margin:0 0 8px 0;font-size:18px;">{title}</h3>
                <p style="margin:0 0 8px 0;color:#444;line-height:1.5;">{lesson_text}</p>
                <p style="margin:0;white-space:pre-wrap;color:#222;"><strong>Example prompt:</strong><br>{example_prompt}</p>
            </div>
            """)

        return "\n".join(blocks)

    html = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>The Daily Prompt</title>
    </head>
    <body style="margin:0;padding:0;background:#f6f6f6;font-family:Arial,sans-serif;color:#111;">
        <div style="max-width:800px;margin:0 auto;padding:32px 20px;">
            <div style="background:white;padding:32px;border-radius:14px;border:1px solid #ddd;">
                <h1 style="margin-top:0;margin-bottom:8px;font-size:32px;">The Daily Prompt</h1>
                <p style="margin-top:0;color:#555;font-size:16px;">
                    The daily AI briefing for ambitious professionals who want to win at work and in life.
                </p>

                {section_title("Top AI Headlines")}
                {render_headlines(headlines)}

                {section_title("Today’s Prompts")}
                {render_prompts(prompts)}

                {section_title("Skill Builder")}
                {render_skills(skills)}
            </div>
        </div>
    </body>
    </html>
    """

    return html








