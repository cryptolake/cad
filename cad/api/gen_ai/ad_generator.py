from . import openai


objective = "Generate an engaging facebook ad description."
model = "text-davinci-003"


def construct_prompt(name, description, link, parameters):
    "Construct prompt to be used by gpt."

    prompt = f"""
    Objective: {objective}
    Parameters: {parameters}
    input:
        product_name: {name}
        product_description: {description}
        product_link: {link}

    output:
    """
    return prompt

def generate_ad(name, description, link,
             parameters, n, max_words, temp=1.0):
    "Generate ad with gpt."

    prompt = construct_prompt(name, description,
                              link, parameters)

    response = {}

    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_tokens=len(prompt) + max_words,
            top_p=1,
            n=n,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        print(e)
        return None
    else:
        ads = [{"text": ad.get('text')} for ad in response['choices']]

        return ads

