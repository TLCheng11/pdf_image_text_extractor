from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.callbacks import get_openai_callback

load_dotenv()
model = os.getenv("LLM_MODEL")

def translate_text(target_language: str, rules: str, source_text: str):
    chat = ChatOpenAI(model_name=model, temperature=0.8)

    system_template = "You are a professional translator for a law firm, translate the input into {target_language}. Follow these rules when translating: {rules}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "{source_text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    with get_openai_callback() as cb:
        response = chain.run(
            {"target_language": target_language, "rules": rules, "source_text": source_text}
        )

        return {"response": response, "cb": cb}
