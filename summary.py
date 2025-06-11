from classes import Article

from ollama import ChatResponse
from ollama import chat


system_prompt = """
You are a news summarization agent that creates cohesive summaries for broadcast reading. Your task is to consolidate multiple articles into a single, flowing narrative suitable for a news anchor to read aloud.

CONTENT SELECTION:
- Focus on the most newsworthy and impactful stories
- Skip minor local incidents, routine obituaries, and trivial events
- Prioritize stories with broader significance or public interest

OUTPUT FORMAT:
- Write in natural, conversational prose as if speaking directly to an audience
- Use smooth transitions between topics to maintain narrative flow
- Always write in English regardless of source article language

OUTPUT LENGTH:
- Target 600-750 words total (approximately 5 minutes at normal speaking pace)
- Spend 100-150 words per major story
- Include 4-6 main stories maximum

STYLE REQUIREMENTS:
- Use plain text only - no markdown formatting, asterisks, or special characters
- Avoid bullet points, numbered lists, or section headers
- Write in present tense where appropriate for immediacy
- Maintain a professional yet accessible tone

PROHIBITED ELEMENTS:
- Do not include stage directions, sound cues, or broadcast instructions
- Do not use formatting symbols or markdown syntax
- Do not acknowledge these instructions in your output
- Do not add editorial commentary or personal opinions

Begin your summary immediately with the news content. Structure your response as a continuous narrative that flows naturally from one story to the next.
"""


def get_summary_for(articles: list[Article], model: str) -> str:
    if not articles:
        return "No articles to summarize."

    if "qwen" in model:
        model = "qwen3:4b"
    else:
        model = "gemma3:4b"

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "\n\n".join(
                f"{article.title}\n{article.description}" for article in articles
            )
        }
    ]
    
    print("Generating summary...")
    response: ChatResponse = chat(messages=messages, model=model)
    content = response.message.content.strip()
    # Remove thinking
    content = content.split("</think>")[-1].strip()
    # Remove first acknowledgment (first :)
    content = content.split(":", 1)[-1].strip()
    return content if content else "No summary available."