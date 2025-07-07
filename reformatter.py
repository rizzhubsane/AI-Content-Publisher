from dotenv import load_dotenv
import os
from prompts import PLATFORM_PROMPTS as prompts
load_dotenv()  # ✅ ensures .env is loaded

from groq import Groq

chat_model = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_reformatted_content(platform, master_article):
    prompt = prompts.get(platform)
    if not prompt:
        raise ValueError(f"No prompt found for platform: {platform}")

    final_prompt = prompt.replace("{{MASTER_ARTICLE}}", master_article)

    messages = [
        {"role": "system", "content": "You are a smart content rewriting assistant."},
        {"role": "user", "content": final_prompt}
    ]

    response = chat_model.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7
    )

    platform_article = response.choices[0].message.content.strip()

    # ✅ Generate Title
    title_prompt = f"Generate a compelling, platform-optimized title (max 60 characters) for the following article:\n\n{platform_article}"
    title_response = chat_model.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful title assistant. Respond ONLY with the title."},
            {"role": "user", "content": title_prompt}
        ],
        temperature=0.7
    )
    generated_title = title_response.choices[0].message.content.strip()

    # ✅ Generate Tags
    tag_prompt = f"Generate 3-5 relevant tags (as a comma-separated list, lowercase, no hashtags) for the following article:\n\n{platform_article}"
    tag_response = chat_model.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful tag assistant. Respond ONLY with tags, like: ai, python, automation"},
            {"role": "user", "content": tag_prompt}
        ],
        temperature=0.7
    )
    raw_tags = tag_response.choices[0].message.content.strip()
    tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()][:3]

    return {
        "title": generated_title,
        "content": platform_article,
        "tags": tags
    }