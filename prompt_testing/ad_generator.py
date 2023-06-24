from dotenv import load_dotenv
from dataclasses import dataclass
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class GenAds:
    """
    Class for generating ads using openAI gpt.
    """

    objective = "Generate an engaging facebook ad description."
    model = "text-davinci-003"

    name: str
    description: str
    link: str
    parameters: str

    def generate(self, n, max_words, temp=1.0):
        "Generate ad with gpt."

        self.__construct_prompt()

        response = {}

        try:
            response = openai.Completion.create(
                model=GenAds.model,
                prompt=self.prompt,
                temperature=temp,
                max_tokens=len(self.prompt) + max_words,
                top_p=1,
                n=n,
                frequency_penalty=0,
                presence_penalty=0
            )
        except Exception:
            self.ads = None
        else:
            self.ads = response.get('choices')

    def __construct_prompt(self):
        "Construct prompt to be used by gpt."

        self.prompt = f"""
        Objective: {GenAds.objective}
        Variables: product_name, product_description, product_link
        Parameters: {self.parameters}
        input:
            product_name: {self.name}
            product_description: {self.description}
            product_link: {self.link}

        output:
        """
        return self.prompt

    def __str__(self):
        """Show Ad"""
        text_ads = ""
        if self.ads:
            for ad in self.ads:
                text_ads += str(ad['text']) + '\n'
                # print(str(ad['text']))
            return text_ads.encode('utf-8').decode('utf-8')
        else:
            return "Ads is not yet generated."
