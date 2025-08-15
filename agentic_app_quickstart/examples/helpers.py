from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
import sys

load_dotenv()

def validate_api_config():
    """validate api configuration and provide helpful error messages"""
    api_key = os.getenv("OPENAI_API_KEY")
    api_endpoint = os.getenv("OPENAI_API_ENDPOINT")
    
    if not api_key:
        print("error: OPENAI_API_KEY environment variable is not set")
        print("please add OPENAI_API_KEY=your_api_key_here to your .env file")
        return False
    
    if not api_endpoint:
        print("error: OPENAI_API_ENDPOINT environment variable is not set")
        print("please add OPENAI_API_ENDPOINT=your_endpoint_here to your .env file")
        return False
    
    api_key = api_key.strip().rstrip('%').rstrip('"').rstrip("'")
    
    if not api_key.startswith(('sk-', 'prx_live_', 'prx_test_')):
        print("warning: api key format doesn't match expected patterns")
        print("expected formats: sk-... (openai), prx_live_... (proxy), prx_test_... (proxy)")
    
    if not api_endpoint.startswith(('http://', 'https://')):
        print("error: api endpoint must start with http:// or https://")
        return False
    
    return True

def get_client():
    """get openai client with validation"""
    if not validate_api_config():
        print("\nplease fix the configuration issues above and try again")
        sys.exit(1)
    
    api_key = os.getenv("OPENAI_API_KEY").strip().rstrip('%').rstrip('"').rstrip("'")
    api_endpoint = os.getenv("OPENAI_API_ENDPOINT").strip().rstrip('"').rstrip("'")
    
    try:
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=api_endpoint
        )
        return client
    except Exception as e:
        print(f"error creating openai client: {e}")
        sys.exit(1)

def get_model():
    """get openai model with validation"""
    try:
        model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=get_client()
        )
        return model
    except Exception as e:
        print(f"error creating model: {e}")
        print("please check your api configuration and try again")
        sys.exit(1)