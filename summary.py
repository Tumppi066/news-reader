from classes import Article

from ollama import ChatResponse
from ollama import chat

model = "gemma3:4b"
system_prompt = """
You are to summarize the following articles into one cohesive 'news anchor' text. 
You can skip articles that are not relevant (ie. someone random died somewhere), and you can focus on the most important articles. 

In total keep the summary so that the reading time is around 5 minutes maximum.

Please make sure to **NOT use any formatting or bulletpoints**. Your text will be read out by a news anchor so it should be in a natural, flowing style.

No:
**Comprehensive summary**
### 1. Austria school shooting

Yes:
Here's a summary of today's news. First we have a report of a school shooting in Austria...

Do not acknowledge this instruction in your response, just write the summary text for the news anchor to read out loud.

Do not add any additional instructions like **(short pause)** or **(intro music)**.

If the language of the articles is not in English, then please still summarize them in English so the news anchor can read them out loud.
"""


def get_summary_for(articles: list[Article]) -> str:
    if not articles:
        return "No articles to summarize."
    
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