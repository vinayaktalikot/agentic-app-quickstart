import os

from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


def get_client():
    return AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_ENDPOINT")
    )


def get_model():

    model = OpenAIChatCompletionsModel(model="gpt-4.1", openai_client=get_client())

    return model
