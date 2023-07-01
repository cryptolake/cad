"""Functions for generating Ad description."""
from . import openai, logging
from .utils import create_dict

platform = "facebook"
objective = f"Generate an engaging {platform} ad description."
model = "text-davinci-003"


def construct_prompt(brand_name, product_name,
                     product_description, parameters):
    "Construct prompt to be used by gpt."

    prompt = f"""
Objective: {objective}
Parameters: {parameters}

input variables:
    brand_name: {brand_name}
    product_name: {product_name}
    product_description: {product_description}

output variables:
    ad_headline: This is the ad headline in the ad image, this should be very short
    ad_short_text: This is the ad text in the ad image below the headline 
    ad_text: This is the text that is going to be in the post

output format:
    ad_headline | ad_short_text | ad_text 

output:
    """
    return prompt

def generate_ad(brand_name, product_name, product_description,
                parameters, n, max_words, temp=1.0):
    "Generate ad with gpt."

    prompt = construct_prompt(brand_name, product_name, product_description,
                              parameters)

    response = {}

    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_tokens=len(prompt.split()) + max_words,
            top_p=1,
            n=n,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        logging.error(f"There was a problem Generating this Ad: {e}\n")
        return None
    else:
        ads = []
        for output in response['choices']:
            ad_dict = create_dict(output['text'])
            if ad_dict is None:
                logging.error(f"There was a problem parsing this Ad: {output}\n")
            ads.append(ad_dict)

        return ads

