from llama_index.core import PromptTemplate
from llm_factory.get_llm import get_ollama_llm

def get_chat_title(model, user_query):
    llm = get_ollama_llm(model)  # ✅ fixed
    title_prompt_template = (
        "You are helpful assistant that generate short, clear and catchy titles.\n\n"
        "Task:\n- Read the given user query.\n- Create a concise title (max 7 words).\n"
        "- The title should summarize intent of the query.\n"
        "- Avoid unnecessary words, punctuation or fillers.\n"
        "- Keep it professional and easy to understand.\n\n"
        "User Query:\n{user_query}\n\n"
        "Output:\nTitle:"
    )
    title_prompt = PromptTemplate(title_prompt_template).format(user_query=user_query)
    title = llm.complete(prompt=title_prompt).text.strip()
    return title