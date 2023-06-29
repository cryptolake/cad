from dotenv import load_dotenv
import openai
load_dotenv()
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

from .ad_generator import construct_prompt, generate_ad
