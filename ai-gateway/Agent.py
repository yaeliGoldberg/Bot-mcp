from Prompt import prompt_builder
from Gateway import gateway


def agent(data: dict):
    products = data.get("products", [])
    level = data.get("level", "easy")

    # שלב 1 – בניית פרומפט
    prompt = prompt_builder(products, level)

    # שלב 2 – שליחה ל-Gateway
    response = gateway(prompt)

    return response
